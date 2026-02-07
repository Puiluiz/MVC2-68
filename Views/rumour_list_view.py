from __future__ import annotations

import tkinter as tk
from tkinter import ttk
from typing import TYPE_CHECKING, Dict, List, Optional

if TYPE_CHECKING:
    from Controllers.app_controller import AppController


class RumourListView(tk.Frame):
    """View for displaying the list of all rumours."""

    def __init__(self, parent: tk.Widget, controller: AppController) -> None:
        """Initialize the rumour list view."""
        super().__init__(parent)
        self.controller = controller
        self.report_counts: Dict[str, int] = {}
        self.rumours: List[Dict] = []

        # Header with title and nav buttons
        header_frame = tk.Frame(self, bg="#f0f0f0")
        header_frame.pack(fill=tk.X, padx=0, pady=0)
        
        title = tk.Label(header_frame, text="Rumour Tracking System", font=("Segoe UI", 16, "bold"), bg="#f0f0f0")
        title.pack(side=tk.LEFT, padx=15, pady=12)
        
        nav_frame = tk.Frame(header_frame, bg="#f0f0f0")
        nav_frame.pack(side=tk.RIGHT, padx=15, pady=12)
        
        ttk.Button(nav_frame, text="Summary", command=self.controller.show_summary_view).pack(side=tk.LEFT, padx=5)
        ttk.Button(nav_frame, text="Logout", command=self.controller.logout).pack(side=tk.LEFT, padx=5)
        
        # Main content area
        content_frame = tk.LabelFrame(self, text="Select a rumour to view details", font=("Segoe UI", 11, "bold"))
        content_frame.pack(fill=tk.BOTH, expand=True, padx=12, pady=12)

        container = tk.Frame(content_frame)
        container.pack(fill=tk.BOTH, expand=True, padx=0, pady=0)

        self.listbox = tk.Listbox(container, height=18, font=("Segoe UI", 10))
        scrollbar = tk.Scrollbar(container, orient=tk.VERTICAL, command=self.listbox.yview)
        self.listbox.configure(yscrollcommand=scrollbar.set)
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.listbox.bind("<Double-1>", self._on_open_detail)

        button_bar = tk.Frame(self)
        button_bar.pack(pady=12, padx=12)

        open_btn = ttk.Button(button_bar, text="View Details", command=self._on_open_detail, width=25)
        open_btn.pack(padx=5)

    def set_data(self, rumours: List[Dict], report_counts: Dict[str, int]) -> None:
        """Set rumour data to be displayed in the list."""
        self.rumours = rumours
        self.report_counts = report_counts
        self.listbox.delete(0, tk.END)
        for rumour in rumours:
            rumour_id = rumour.get("rumourId", "-")
            title = rumour.get("title", "-")
            status = self.controller.get_status_label(rumour)
            count = report_counts.get(rumour_id, 0)
            self.listbox.insert(tk.END, f"[{rumour_id}] {title} | reports: {count} | status: {status}")

    def _get_selected_rumour_id(self) -> Optional[str]:
        """Get the ID of the currently selected rumour."""
        selection = self.listbox.curselection()
        if not selection:
            return None
        index = selection[0]
        rumour = self.rumours[index]
        return rumour.get("rumourId")

    def _on_open_detail(self, event: Optional[tk.Event] = None) -> None:
        """Handle opening the detail view for selected rumour."""
        rumour_id = self._get_selected_rumour_id()
        if not rumour_id:
            return
        self.controller.show_detail_view(rumour_id)

