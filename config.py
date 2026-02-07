from pathlib import Path

# Directories
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "Data"

# Business Rules
PANIC_THRESHOLD = 3

# UI Configuration
WINDOW_WIDTH = 820
WINDOW_HEIGHT = 720
WINDOW_TITLE = "Rumour Tracking System"

# Report Types
REPORT_TYPES = ["ข้อมูลเท็จ", "ปลุกปั่น", "บิดเบือน"]
