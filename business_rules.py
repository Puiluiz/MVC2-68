"""ระบบธุรกิจกฎเกณฑ์และตรรกะสำหรับระบบตติดตามข่าวลือ"""

from typing import Dict, List, Optional

# กฎการประกาศสถานะ
PANIC_THRESHOLD = 2  # จำนวนรายงานขั้นต่ำที่ทำให้เปลี่ยนสถานะเป็น panic

# ประเภทการรายงาน
REPORT_TYPES = [
    "ข้อมูลเท็จ",
    "ปลุกปั่น",
    "บิดเบือน",
]

# ค่าสถานะของข่าวลือ
STATUS_PANIC = "panic"
STATUS_NORMAL = "ปกติ"


# ฟังก์ชั่น Business Logic
def should_trigger_panic(report_count: int) -> bool:
    """ตรวจสอบว่าควรเปลี่ยนสถานะเป็น panic หรือไม่"""
    return report_count >= PANIC_THRESHOLD


def is_panic_status(status: str) -> bool:
    """ตรวจสอบว่าสถานะเป็น panic หรือไม่"""
    return status == STATUS_PANIC


def is_normal_status(status: str) -> bool:
    """ตรวจสอบว่าสถานะเป็นปกติหรือไม่"""
    return status == STATUS_NORMAL


def get_status_display(status: str) -> str:
    """แปลง status ให้เป็นรูปแบบการแสดงผล"""
    if is_panic_status(status):
        return "panic"
    if is_normal_status(status):
        return "ปกติ"
    return str(status)


def can_accept_report(rumour: Dict, user_reported: bool, is_verified: bool) -> bool:
    """ตรวจสอบว่าข่าวลือสามารถรับรายงานใหม่ได้หรือไม่"""
    # ไม่สามารถรายงานข่าวลือที่ยืนยันแล้ว
    if is_verified:
        return False
    # ไม่สามารถรายงานข่าวลือซ้ำจากผู้ใช้เดียวกัน
    if user_reported:
        return False
    return True


def can_verify_rumour(rumour: Dict, is_inspector: bool) -> bool:
    """ตรวจสอบว่าผู้ใช้สามารถยืนยันข่าวลือได้หรือไม่"""
    # เฉพาะ Inspector เท่านั้น
    if not is_inspector:
        return False
    return True


def filter_rumours_by_status(rumours: List[Dict], status: str) -> List[Dict]:
    """กรองข่าวลือตามสถานะ"""
    return [r for r in rumours if r.get("status") == status]


def filter_rumours_by_verified(rumours: List[Dict], verified: Optional[bool]) -> List[Dict]:
    """กรองข่าวลือตามสถานะของการยืนยัน"""
    return [r for r in rumours if r.get("verified") is verified]
