from __future__ import annotations

import tkinter as tk
from tkinter import messagebox
from typing import Dict, Optional

from config import DATA_DIR, PANIC_THRESHOLD
from Models import ReportModel, RumourModel, UserModel
from Models.rumour_model import STATUS_NORMAL, STATUS_PANIC
from Views import LoginView, RumourDetailView, RumourListView, SummaryView


class AppController:
    """Main controller for the Rumour Tracking System application."""

    def __init__(self, root: tk.Tk) -> None:
        """Initialize the application controller."""
        self.root = root
        self.rumour_model = RumourModel(DATA_DIR / "rumours.json")
        self.report_model = ReportModel(DATA_DIR / "reports.json")
        self.user_model = UserModel(DATA_DIR / "users.json")

        # Current user state
        self.current_user_id: Optional[str] = None
        self.current_user: Optional[Dict] = None

        # Views
        self.login_view = LoginView(root, self)
        self.list_view = RumourListView(root, self)
        self.detail_view = RumourDetailView(root, self)
        self.summary_view = SummaryView(root, self)

        for view in (self.login_view, self.list_view, self.detail_view, self.summary_view):
            view.grid(row=0, column=0, sticky="nsew")

        # Set login callback and show login screen
        self.login_view.after_login = self.show_list_view
        self.login_view.tkraise()

    def show_list_view(self) -> None:
        """Display the rumour list view."""
        rumours = self.rumour_model.get_all()
        report_counts = self.report_model.get_report_counts()
        sorted_rumours = sorted(
            rumours,
            key=lambda r: (report_counts.get(r.get("rumourId"), 0), r.get("credibilityScore", 0)),
            reverse=True,
        )
        self.list_view.set_data(sorted_rumours, report_counts)
        self.list_view.tkraise()

    def show_detail_view(self, rumour_id: Optional[str]) -> None:
        """Display the rumour detail view."""
        report_counts = self.report_model.get_report_counts()
        rumour = self.rumour_model.get_by_id(rumour_id) if rumour_id else None
        self.detail_view.set_rumour(rumour, report_counts)
        self.detail_view.tkraise()

    def show_summary_view(self) -> None:
        """Display the summary view."""
        report_counts = self.report_model.get_report_counts()
        rumours = self.rumour_model.get_all()
        panic_rumours = [r for r in rumours if r.get("status") == STATUS_PANIC]
        verified_true_rumours = [r for r in rumours if r.get("verified") is True]
        verified_false_rumours = [r for r in rumours if r.get("verified") is False]
        self.summary_view.set_data(panic_rumours, verified_true_rumours, verified_false_rumours, report_counts)
        self.summary_view.tkraise()

    def submit_report(self, rumour_id: str, report_type: str, description: str) -> None:
        """Submit a report for a rumour."""
        if not self.current_user_id:
            messagebox.showerror("Error", "Please login first")
            return

        rumour = self.rumour_model.get_by_id(rumour_id)
        if not rumour:
            messagebox.showerror("Error", "Rumour not found")
            return

        if self.rumour_model.is_verified(rumour):
            messagebox.showwarning("Warning", "Verified rumours cannot be reported")
            return

        if self.report_model.has_report(self.current_user_id, rumour_id):
            messagebox.showwarning("Warning", "You already reported this rumour")
            return

        if not report_type:
            messagebox.showwarning("Warning", "Report type is required")
            return

        self.report_model.add_report(self.current_user_id, rumour_id, report_type, description)
        report_counts = self.report_model.get_report_counts()
        if report_counts.get(rumour_id, 0) >= PANIC_THRESHOLD:
            self.rumour_model.update_status(rumour_id, STATUS_PANIC)

        messagebox.showinfo("Success", "Report submitted")
        self.show_detail_view(rumour_id)

    def verify_rumour(self, rumour_id: str, decision: str) -> None:
        """Verify a rumour as an inspector."""
        if not self.current_user_id:
            messagebox.showerror("Error", "Please login first")
            return

        if not self.user_model.is_inspector(self.current_user_id):
            messagebox.showwarning("Warning", "Only inspectors can verify rumours")
            return

        if decision not in {"true", "false"}:
            messagebox.showwarning("Warning", "Select a verification result")
            return

        rumour = self.rumour_model.get_by_id(rumour_id)
        if not rumour:
            messagebox.showerror("Error", "Rumour not found")
            return

        # Update verified fields only (don't change status)
        verified_result = decision == "true"
        if not self.rumour_model.update_verified(rumour_id, verified_result, self.current_user_id):
            messagebox.showerror("Error", "Failed to verify rumour")
            return

        messagebox.showinfo("Success", "Rumour verified")
        self.show_detail_view(rumour_id)

    def get_status_label(self, rumour: Dict) -> str:
        """Get human-readable status label."""
        status = rumour.get("status", STATUS_NORMAL)
        if status == STATUS_PANIC:
            return "panic"
        if status == STATUS_NORMAL:
            return "ปกติ"
        return str(status)

    def is_rumour_verified(self, rumour: Dict) -> bool:
        """Check if a rumour has been verified (for use by views)."""
        return self.rumour_model.is_verified(rumour)

    def set_current_user(self, user_id: str, user: Dict) -> None:
        """Set the current logged-in user."""
        self.current_user_id = user_id
        self.current_user = user
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

