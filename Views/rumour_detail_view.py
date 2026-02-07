from __future__ import annotations

import tkinter as tk
from tkinter import ttk
from typing import TYPE_CHECKING, Dict, Optional

from config import REPORT_TYPES

if TYPE_CHECKING:
    from Controllers.app_controller import AppController


class RumourDetailView(tk.Frame):
    """View for displaying and interacting with rumour details."""

    def __init__(self, parent: tk.Widget, controller: AppController) -> None:
        """Initialize the rumour detail view."""
        super().__init__(parent)
        self.controller = controller
        self.rumour: Optional[Dict] = None
        self.report_counts: Dict[str, int] = {}

        # Header with navigation
        header_frame = tk.Frame(self, bg="#f0f0f0")
        header_frame.pack(fill=tk.X, padx=0, pady=0)
        
        title = tk.Label(header_frame, text="Rumour Details", font=("Segoe UI", 16, "bold"), bg="#f0f0f0")
        title.pack(side=tk.LEFT, padx=15, pady=12)
        
        nav_frame = tk.Frame(header_frame, bg="#f0f0f0")
        nav_frame.pack(side=tk.RIGHT, padx=15, pady=12)
        ttk.Button(nav_frame, text="Summary", command=self.controller.show_summary_view).pack(side=tk.LEFT, padx=5)
        ttk.Button(nav_frame, text="Back", command=self.controller.show_list_view).pack(side=tk.LEFT, padx=5)
        ttk.Button(nav_frame, text="Logout", command=self.controller.logout).pack(side=tk.LEFT, padx=5)

        # Main content area
        main_frame = tk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=12, pady=12)

        self.detail_frame = tk.LabelFrame(main_frame, text="Details", font=("Segoe UI", 11, "bold"))
        self.detail_frame.pack(fill=tk.X, padx=0, pady=(0, 10))

        self.detail_text = tk.Label(self.detail_frame, text="Select a rumour from the list", justify=tk.LEFT, font=("Segoe UI", 10))
        self.detail_text.pack(anchor="w", padx=12, pady=12)

        # Create frames but don't pack them yet - will be managed in set_rumour
        self.report_frame = tk.LabelFrame(main_frame, text="Report Rumour", font=("Segoe UI", 11, "bold"))

        self.report_type_combo = self._combobox_field(self.report_frame, "Type:", 0)

        self.verify_frame = tk.LabelFrame(main_frame, text="Verify Rumour (Inspector Only)", font=("Segoe UI", 11, "bold"))

        tk.Label(self.verify_frame, text="Result:", font=("Segoe UI", 10)).grid(row=0, column=0, padx=12, pady=10, sticky="w")
        decision_frame = tk.Frame(self.verify_frame)
        decision_frame.grid(row=0, column=1, sticky="w", pady=10)
        self.verify_choice = tk.StringVar(value="")
        ttk.Radiobutton(decision_frame, text="True", variable=self.verify_choice, value="true").pack(
            side=tk.LEFT, padx=10
        )
        ttk.Radiobutton(decision_frame, text="False", variable=self.verify_choice, value="false").pack(
            side=tk.LEFT, padx=10
        )

        verify_btn = ttk.Button(self.verify_frame, text="Confirm Verification", command=self._verify_rumour)
        verify_btn.grid(row=1, column=0, columnspan=2, sticky="w", padx=12, pady=(0, 10))

    def _entry_field(self, parent: tk.Widget, label: str, row: int) -> tk.Entry:
        """Create a labeled entry field (helper method)."""
        tk.Label(parent, text=label).grid(row=row, column=0, padx=5, pady=3, sticky="w")
        entry = tk.Entry(parent, width=40)
        entry.grid(row=row, column=1, padx=5, pady=3, sticky="w")
        return entry

    def _combobox_field(self, parent: tk.Widget, label: str, row: int) -> ttk.Combobox:
        """Create a labeled combobox field (helper method)."""
        tk.Label(parent, text=label, font=("Segoe UI", 10)).grid(row=row, column=0, padx=12, pady=10, sticky="w")
        combo = ttk.Combobox(parent, values=REPORT_TYPES, width=35, state="readonly", font=("Segoe UI", 10))
        combo.grid(row=row, column=1, padx=12, pady=10, sticky="w")
        combo.bind("<<ComboboxSelected>>", lambda e: self._on_report_type_changed(e))
        return combo

    def _on_report_type_changed(self, event: tk.Event) -> None:
        """Handle report type selection."""
        if self.report_type_combo.get():
            self._submit_report()

    def set_rumour(self, rumour: Optional[Dict], report_counts: Dict[str, int]) -> None:
        """Set the rumour to display and update UI accordingly."""
        self.rumour = rumour
        self.report_counts = report_counts

        # Clear previous entry values
        self.report_type_combo.set("")
        self.verify_choice.set("")

        # Unpack all frames first
        self.report_frame.pack_forget()
        self.verify_frame.pack_forget()

        if not rumour:
            # No rumour selected
            self.detail_text.config(text="Select a rumour from the list")
            return

        # View existing rumour mode
        rumour_id = rumour.get("rumourId", "-")
        title = rumour.get("title", "-")
        source = rumour.get("source", "-")
        created = rumour.get("createdDate", "-")
        credibility = rumour.get("credibilityScore", 0)
        status = self.controller.get_status_label(rumour)
        report_count = report_counts.get(rumour_id, 0)
        verified = rumour.get("verified")
        verified_by = rumour.get("verifiedBy")
        verified_date = rumour.get("verifiedDate")

        detail = (
            f"ID: {rumour_id}\n"
            f"Title: {title}\n"
            f"Source: {source}\n"
            f"Created: {created}\n"
            f"Credibility: {credibility}\n"
            f"Reports: {report_count}\n"
            f"Status: {status}"
        )

        if verified is not None:
            verified_status = "True" if verified else "False"
            verified_info = f"\nVerified: {verified_status} (by {verified_by} on {verified_date})"
            detail += verified_info

        self.detail_text.config(text=detail)

        # Show report frame if not verified (ask controller)
        is_verified = self.controller.is_rumour_verified(rumour)
        if not is_verified:
            self.report_frame.pack(fill=tk.X, padx=0, pady=(0, 10))

        # Show verify frame if user is inspector (ask controller)
        if self.controller.is_inspector():
            self.verify_frame.pack(fill=tk.X, padx=0, pady=(0, 10))

    def _submit_report(self) -> None:
        """Handle report submission."""
        if not self.rumour:
            return
        self.controller.submit_report(
            self.rumour.get("rumourId", ""),
            self.report_type_combo.get(),
            "",
        )

    def _verify_rumour(self) -> None:
        """Handle rumour verification."""
        if not self.rumour:
            return
        self.controller.verify_rumour(
            self.rumour.get("rumourId", ""),
            self.verify_choice.get(),
        )

