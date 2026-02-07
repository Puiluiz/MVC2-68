from __future__ import annotations

import tkinter as tk
from tkinter import messagebox, ttk
from typing import TYPE_CHECKING, Callable, Optional

if TYPE_CHECKING:
    from Controllers.app_controller import AppController


class LoginView(tk.Frame):
    """View for user login interface."""

    def __init__(self, parent: tk.Widget, controller: AppController) -> None:
        """Initialize the login view."""
        super().__init__(parent)
        self.controller = controller
        self.after_login: Optional[Callable[[], None]] = None

        title = tk.Label(self, text="Rumour Tracking System", font=("Segoe UI", 18, "bold"))
        title.pack(pady=30)

        subtitle = tk.Label(self, text="Login", font=("Segoe UI", 12, "italic"), fg="gray") 
        subtitle.pack(pady=(0, 30))

        input_frame = tk.Frame(self)
        input_frame.pack(pady=20)

        tk.Label(input_frame, text="User ID:", font=("Segoe UI", 11)).grid(row=0, column=0, padx=15, pady=15, sticky="w")
        self.user_id_entry = tk.Entry(input_frame, width=30, font=("Segoe UI", 11))
        self.user_id_entry.grid(row=0, column=1, padx=15, pady=15)
        self.user_id_entry.bind("<Return>", lambda e: self._login())

        button_frame = tk.Frame(self)
        button_frame.pack(pady=20)

        login_btn = ttk.Button(button_frame, text="Login", command=self._login, width=20)
        login_btn.pack(side=tk.LEFT, padx=5)

        info_frame = tk.LabelFrame(self, text="Demo Users", font=("Segoe UI", 11, "bold"))
        info_frame.pack(fill=tk.X, padx=20, pady=20)

        info_text = tk.Label(
            info_frame,
            text=(
                "Regular User: U0001, U0003, U0005, etc.\n"
                "Inspector: U0002, U0004, U0007, U0010, etc.\n\n"
                "Enter any User ID to login"
            ),
            justify=tk.LEFT,
            font=("Segoe UI", 9),
        )
        info_text.pack(anchor="w", padx=10, pady=10)

    def _login(self) -> None:
        """Handle login button click."""
        # ดึง user ID จากช่องกรอก
        user_id = self.user_id_entry.get().strip()
        if not user_id:
            messagebox.showwarning("Warning", "Please enter User ID")
            return

        # ขอให้ controller ตรวจสอบ user ID
        user = self.controller.validate_user(user_id)
        if not user:
            messagebox.showerror("Error", f"User ID {user_id} not found")
            return

        # ตั้งผู้ใช้ปัจจุบัน แล้วเรียก callback function
        self.controller.set_current_user(user_id, user)
        if self.after_login:
            self.after_login()
