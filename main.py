import tkinter as tk

from config import WINDOW_HEIGHT, WINDOW_TITLE, WINDOW_WIDTH
from Controllers.app_controller import AppController


def main() -> None:
    """Initialize and run the Rumour Tracking System application."""
    # สร้าง Tkinter root window
    root = tk.Tk()
    root.title(WINDOW_TITLE)                          # ตั้งชื่อหน้าต่าง
    root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")  # ตั้งขนาดหน้าต่าง
    root.rowconfigure(0, weight=1)                    # ทำให้ layout ยืดหยุ่น
    root.columnconfigure(0, weight=1)

    # เรียก controller หลัก ที่จัดการทั้งแอปพลิเคชัน
    AppController(root)
    # เริ่มรัน event loop
    root.mainloop()


if __name__ == "__main__":
    main()
