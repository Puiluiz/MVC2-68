from __future__ import annotations

import tkinter as tk
from tkinter import messagebox
from typing import Dict, Optional

from business_rules import (
    PANIC_THRESHOLD,
    REPORT_TYPES,
    STATUS_NORMAL,
    STATUS_PANIC,
    can_accept_report,
    can_verify_rumour,
    filter_rumours_by_status,
    filter_rumours_by_verified,
    get_status_display,
    should_trigger_panic,
)
from config import DATA_DIR
from Models import ReportModel, RumourModel, UserModel
from Views import LoginView, RumourDetailView, RumourListView, SummaryView


class AppController:
    """Main controller for the Rumour Tracking System application."""

    def __init__(self, root: tk.Tk) -> None:
        """Initialize the application controller."""
        self.root = root
        # โหลด Models จากไฟล์ JSON
        self.rumour_model = RumourModel(DATA_DIR / "rumours.json")
        self.report_model = ReportModel(DATA_DIR / "reports.json")
        self.user_model = UserModel(DATA_DIR / "users.json")

        # เก็บข้อมูลผู้ใช้ปัจจุบัน
        self.current_user_id: Optional[str] = None
        self.current_user: Optional[Dict] = None

        # สร้าง Views 
        self.login_view = LoginView(root, self)
        self.list_view = RumourListView(root, self)
        self.detail_view = RumourDetailView(root, self)
        self.summary_view = SummaryView(root, self)

        for view in (self.login_view, self.list_view, self.detail_view, self.summary_view):
            view.grid(row=0, column=0, sticky="nsew")

        self.login_view.after_login = self.show_list_view
        self.login_view.tkraise()

    def show_list_view(self) -> None:
        """Display the rumour list view."""
        # ดึงข่าวลือทั้งหมด และจำนวนรายงาน
        rumours = self.rumour_model.get_all()
        report_counts = self.report_model.get_report_counts()
        # เรียงลำดับตามจำนวนรายงาน และ credibility score (น้อยไปมาก)
        sorted_rumours = sorted(
            rumours,
            key=lambda r: (report_counts.get(r.get("rumourId"), 0), r.get("credibilityScore", 0)),
            reverse=True,
        )
        self.list_view.set_data(sorted_rumours, report_counts)
        self.list_view.tkraise()  # แสดง list view หน้าจอ

    def show_detail_view(self, rumour_id: Optional[str]) -> None:
        """Display the rumour detail view."""
        report_counts = self.report_model.get_report_counts()
        rumour = self.rumour_model.get_by_id(rumour_id) if rumour_id else None
        self.detail_view.set_rumour(rumour, report_counts)
        self.detail_view.tkraise()

    def show_summary_view(self) -> None:
        """Display the summary view."""
        # ดึงจำนวนรายงานและข่าวลือทั้งหมด
        report_counts = self.report_model.get_report_counts()
        rumours = self.rumour_model.get_all()
        # แยกข่าวลือตามประเภท: ฉุกเฉิน, ยืนยันจริง, ยืนยันเท็จ
        panic_rumours = filter_rumours_by_status(rumours, STATUS_PANIC)
        verified_true_rumours = filter_rumours_by_verified(rumours, True)
        verified_false_rumours = filter_rumours_by_verified(rumours, False)
        self.summary_view.set_data(panic_rumours, verified_true_rumours, verified_false_rumours, report_counts)
        self.summary_view.tkraise()  # แสดง summary view หน้าจอ

    def submit_report(self, rumour_id: str, report_type: str, description: str) -> None:
        """Submit a report for a rumour."""
        # ตรวจสอบว่าผู้ใช้ได้เข้าสู่ระบบแล้วหรือไม่
        if not self.current_user_id:
            messagebox.showerror("Error", "Please login first")
            return

        # ตรวจสอบความถูกต้องของ rumour_id
        rumour = self.validate_rumour_id(rumour_id)
        if not rumour:
            messagebox.showerror("Error", "Rumour not found")
            return

        # ตรวจสอบว่าข่าวลือสามารถรับรายงาน
        is_verified = self.rumour_model.is_verified(rumour)
        user_reported = self.report_model.has_report(self.current_user_id, rumour_id)
        if not can_accept_report(rumour, user_reported, is_verified):
            if is_verified:
                messagebox.showwarning("Warning", "Verified rumours cannot be reported")
            else:
                messagebox.showwarning("Warning", "You already reported this rumour")
            return

        if not report_type:
            messagebox.showwarning("Warning", "Report type is required")
            return

        # บันทึกรายงาน
        self.report_model.add_report(self.current_user_id, rumour_id, report_type, description)
        report_counts = self.report_model.get_report_counts()
        # ตรวจสอบว่าควรเปลี่ยนสถานะเป็น panic หรือไม่
        if should_trigger_panic(report_counts.get(rumour_id, 0)):
            self.rumour_model.update_status(rumour_id, STATUS_PANIC)

        messagebox.showinfo("Success", "Report submitted")
        self.show_detail_view(rumour_id)

    def verify_rumour(self, rumour_id: str, decision: str) -> None:
        """Verify a rumour as an inspector."""
        # ตรวจสอบว่า user ได้เข้าสู่ระบบหรือไม่
        if not self.current_user_id:
            messagebox.showerror("Error", "Please login first")
            return

        # ตรวจสอบว่าผู้ใช้สามารถยืนยันข่าวลือได้หรือไม่
        if not can_verify_rumour({}, self.is_inspector()):
            messagebox.showwarning("Warning", "Only inspectors can verify rumours")
            return

        # ตรวจสอบว่าเลือกผลลัพธ์หรือไม่
        if decision not in {"true", "false"}:
            messagebox.showwarning("Warning", "Select a verification result")
            return

        # ตรวจสอบความถูกต้องของ rumour_id
        rumour = self.validate_rumour_id(rumour_id)
        if not rumour:
            messagebox.showerror("Error", "Rumour not found")
            return

        # อัปเดตผลยืนยัน
        verified_result = decision == "true"
        if not self.rumour_model.update_verified(rumour_id, verified_result, self.current_user_id):
            messagebox.showerror("Error", "Failed to verify rumour")
            return

        messagebox.showinfo("Success", "Rumour verified")
        self.show_detail_view(rumour_id)

    def get_status_label(self, rumour: Dict) -> str:
        """Get human-readable status label."""
        status = rumour.get("status", STATUS_NORMAL)
        return get_status_display(status)

    def is_rumour_verified(self, rumour: Dict) -> bool:
        """Check if a rumour has been verified (for use by views)."""
        return self.rumour_model.is_verified(rumour)

    def validate_rumour_id(self, rumour_id: str) -> Optional[Dict]:
        """Validate rumour ID and return rumour data, or None if not found."""
        return self.rumour_model.get_by_id(rumour_id)

    def can_show_report_frame(self, rumour: Dict) -> bool:
        """Check if report frame should be shown for this rumour."""
        # แสดงการรายงานเฉพาะข่าวที่ยังไม่ได้ยืนยัน
        return not self.is_rumour_verified(rumour)

    def can_show_verify_frame(self) -> bool:
        """Check if verify frame should be shown (only for inspectors)."""
        # แสดงการยืนยันเฉพาะผู้ตรวจสอบ
        return self.is_inspector()

    def set_current_user(self, user_id: str, user: Dict) -> None:
        """Set the current logged-in user."""
        # บันทึกผู้ใช้ปัจจุบัน
        self.current_user_id = user_id
        self.current_user = user
        # ดึงชื่อและบทบาท แล้วแสดงในชื่อหน้าต่าง
        name = user.get("name", user_id)
        role = user.get("role", "User")
        self.root.title(f"Rumour Tracking System - {name} ({role})")

    def is_inspector(self) -> bool:
        """Check if current user is an inspector."""
        if not self.current_user_id:
            return False
        return self.user_model.is_inspector(self.current_user_id)

    def validate_user(self, user_id: str) -> Optional[Dict]:
        """Validate and return user by ID, or None if not found."""
        return self.user_model.get_by_id(user_id)

    def logout(self) -> None:
        """Logout current user and return to login screen."""
        self.current_user_id = None
        self.current_user = None
        self.root.title("Rumour Tracking System")
        self.login_view.tkraise()

