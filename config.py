"""ตั้งค่าทางเทคนิค สำหรับแอปพลิเคชันระบบตติดตามข่าวลือ"""
from pathlib import Path

# ตั้งค่าไดเรกทอรี่ (เส้นทางไฟล์ข้อมูล)
BASE_DIR = Path(__file__).resolve().parent  # โฟลเดอร์หลักโปรเจค
DATA_DIR = BASE_DIR / "Data"                # โฟลเดอร์เก็บไฟล์ JSON

# ตั้งค่าหน้าต่างแอปพลิเคชัน
WINDOW_WIDTH = 820
WINDOW_HEIGHT = 720
WINDOW_TITLE = "Rumour Tracking System"
