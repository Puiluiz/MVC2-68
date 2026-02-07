from __future__ import annotations

import tkinter as tk
from tkinter import ttk
from typing import TYPE_CHECKING, Dict, List

if TYPE_CHECKING:
    from Controllers.app_controller import AppController


class SummaryView(tk.Frame):
    """View for displaying categorized summary of rumours."""

    def __init__(self, parent: tk.Widget, controller: AppController) -> None:
        """Initialize the summary view."""
        super().__init__(parent)
        self.controller = controller

        # Header with navigation
        header_frame = tk.Frame(self, bg="#f0f0f0")
        header_frame.pack(fill=tk.X, padx=0, pady=0)
        
        title = tk.Label(header_frame, text="Summary", font=("Segoe UI", 16, "bold"), bg="#f0f0f0")
        title.pack(side=tk.LEFT, padx=15, pady=12)
        
        nav_frame = tk.Frame(header_frame, bg="#f0f0f0")
        nav_frame.pack(side=tk.RIGHT, padx=15, pady=12)
        ttk.Button(nav_frame, text="Back to List", command=self.controller.show_list_view).pack(side=tk.LEFT, padx=5)
        ttk.Button(nav_frame, text="Logout", command=self.controller.logout).pack(side=tk.LEFT, padx=5)

        # Main content area
        content_frame = tk.Frame(self)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=12, pady=12)

        self.panic_frame = tk.LabelFrame(content_frame, text="Panic Rumours", font=("Segoe UI", 11, "bold"))
        self.panic_frame.pack(fill=tk.BOTH, expand=True, padx=0, pady=(0, 10))
        self.panic_list = tk.Listbox(self.panic_frame, height=6, font=("Segoe UI", 10))
        self.panic_list.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.verified_true_frame = tk.LabelFrame(content_frame, text="Verified True", font=("Segoe UI", 11, "bold"))
        self.verified_true_frame.pack(fill=tk.BOTH, expand=True, padx=0, pady=(0, 10))
        self.verified_true_list = tk.Listbox(self.verified_true_frame, height=6, font=("Segoe UI", 10))
        self.verified_true_list.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.verified_false_frame = tk.LabelFrame(content_frame, text="Verified False", font=("Segoe UI", 11, "bold"))
        self.verified_false_frame.pack(fill=tk.BOTH, expand=True, padx=0)
        self.verified_false_list = tk.Listbox(self.verified_false_frame, height=6, font=("Segoe UI", 10))
        self.verified_false_list.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    def set_data(
        self,
        panic_rumours: List[Dict],
        verified_true_rumours: List[Dict],
        verified_false_rumours: List[Dict],
        report_counts: Dict[str, int],
    ) -> None:
        """Set data for all three summary categories."""
        # ล้างรายการทั้ง 3 หมวด
        self.panic_list.delete(0, tk.END)
        self.verified_true_list.delete(0, tk.END)
        self.verified_false_list.delete(0, tk.END)

        # แสดงข่าวลือที่ฉุกเฉิน
        for rumour in panic_rumours:
            rumour_id = rumour.get("rumourId", "-")
            title = rumour.get("title", "-")
            count = report_counts.get(rumour_id, 0)
            self.panic_list.insert(tk.END, f"[{rumour_id}] {title} | reports: {count}")

        # แสดงข่าวลือที่ยืนยันว่าจริง
        for rumour in verified_true_rumours:
            rumour_id = rumour.get("rumourId", "-")
            title = rumour.get("title", "-")
            count = report_counts.get(rumour_id, 0)
            self.verified_true_list.insert(tk.END, f"[{rumour_id}] {title} | reports: {count}")

        # แสดงข่าวลือที่ยืนยันว่าเท็จ
        for rumour in verified_false_rumours:
            rumour_id = rumour.get("rumourId", "-")
            title = rumour.get("title", "-")
            count = report_counts.get(rumour_id, 0)
            self.verified_false_list.insert(tk.END, f"[{rumour_id}] {title} | reports: {count}")

