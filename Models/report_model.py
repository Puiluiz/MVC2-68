from __future__ import annotations

import json
from datetime import date
from pathlib import Path
from typing import Dict, List


class ReportModel:
    """Model for managing report data."""

    def __init__(self, data_path: Path) -> None:
        """Initialize the report model with data file path."""
        self._data_path = data_path
        self._reports: List[Dict] = []
        self._load()

    def _load(self) -> None:
        """Load reports from JSON file."""
        if not self._data_path.exists():
            self._reports = []
            return
        with self._data_path.open("r", encoding="utf-8") as handle:
            self._reports = json.load(handle)

    def save(self) -> None:
        """Save reports to JSON file."""
        with self._data_path.open("w", encoding="utf-8") as handle:
            json.dump(self._reports, handle, ensure_ascii=False, indent=2)

    def get_all(self) -> List[Dict]:
        """Get all reports."""
        return list(self._reports)

    def get_report_counts(self) -> Dict[str, int]:
        """Get report counts for each rumour."""
        # นับจำนวนรายงานสำหรับแต่ละข่าวลือ
        counts: Dict[str, int] = {}
        for report in self._reports:
            rumour_id = report.get("rumourId")
            counts[rumour_id] = counts.get(rumour_id, 0) + 1
        return counts

    def has_report(self, reporter_id: str, rumour_id: str) -> bool:
        """Check if a user has already reported a specific rumour."""
        # ตรวจสอบว่า user คนนี้เคยรายงานข่าวลือนี้หรือไม่
        for report in self._reports:
            if report.get("reporterId") == reporter_id and report.get("rumourId") == rumour_id:
                return True
        return False

    def add_report(self, reporter_id: str, rumour_id: str, report_type: str, description: str) -> Dict:
        """Add a new report."""
        # สร้างรายงานใหม่พร้อมรายละเอียด
        new_report = {
            "reportId": self._next_id(),          # สร้าง ID อัตโนมัติ
            "reporterId": reporter_id,            # ID ของผู้รายงาน
            "rumourId": rumour_id,                # ID ของข่าวลือ
            "reportDate": date.today().isoformat(),
            "reportType": report_type,            # ประเภทรายงาน
            "description": description,           # รายละเอียดเพิ่มเติม
        }
        self._reports.append(new_report)
        self.save()
        return new_report

    def _next_id(self) -> str:
        """Generate the next report ID."""
        # หา ID ที่ใหญ่ที่สุด แล้วสร้าง ID ถัดไป เช่น R0001, R0002, ...
        max_id = 0
        for report in self._reports:
            report_id = report.get("reportId", "")
            if report_id.startswith("R") and report_id[1:].isdigit():
                max_id = max(max_id, int(report_id[1:]))
        return f"R{max_id + 1:04d}"
