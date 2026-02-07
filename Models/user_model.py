from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, List, Optional


class UserModel:
    """Model for managing user data."""

    def __init__(self, data_path: Path) -> None:
        """Initialize the user model with data file path."""
        self._data_path = data_path
        self._users: List[Dict] = []
        self._load()

    def _load(self) -> None:
        """Load users from JSON file."""
        if not self._data_path.exists():
            self._users = []
            return
        with self._data_path.open("r", encoding="utf-8") as handle:
            self._users = json.load(handle)

    def get_by_id(self, user_id: str) -> Optional[Dict]:
        """Get a user by ID."""
        # ค้นหา user จาก ID
        for user in self._users:
            if user.get("userId") == user_id:
                return user
        return None

    def is_inspector(self, user_id: str) -> bool:
        """Check if a user is an inspector."""
        # ดึง user แล้วตรวจสอบ role
        user = self.get_by_id(user_id)
        if not user:
            return False
        # ตรวจสอบว่าเป็น inspector หรือไม่
        return user.get("role") in {"ผู้ตรวจสอบ", "inspector"}
