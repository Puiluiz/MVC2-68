import tkinter as tk

from config import WINDOW_HEIGHT, WINDOW_TITLE, WINDOW_WIDTH
from Controllers.app_controller import AppController


def main() -> None:
    """Initialize and run the Rumour Tracking System application."""
    root = tk.Tk()
    root.title(WINDOW_TITLE)
    root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
    root.rowconfigure(0, weight=1)
    root.columnconfigure(0, weight=1)

    AppController(root)
    root.mainloop()


if __name__ == "__main__":
    main()
