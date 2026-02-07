from __future__ import annotations

import json
from datetime import date
from pathlib import Path
from typing import Dict, List, Optional

# Status constants
STATUS_PANIC = "panic"
STATUS_NORMAL = "ปกติ"


class RumourModel:
    """Model for managing rumour data."""

    def __init__(self, data_path: Path) -> None:
        """Initialize the rumour model with data file path."""
        self._data_path = data_path
        self._rumours: List[Dict] = []
        self._load()

    def _load(self) -> None:
        """Load rumours from JSON file."""
        if not self._data_path.exists():
            self._rumours = []
            return
        with self._data_path.open("r", encoding="utf-8") as handle:
            self._rumours = json.load(handle)

    def save(self) -> None:
        """Save rumours to JSON file."""
        with self._data_path.open("w", encoding="utf-8") as handle:
            json.dump(self._rumours, handle, ensure_ascii=False, indent=2)

    def get_all(self) -> List[Dict]:
        """Get all rumours."""
        return list(self._rumours)

    def get_by_id(self, rumour_id: str) -> Optional[Dict]:
        """Get a rumour by ID."""
        for rumour in self._rumours:
            if rumour.get("rumourId") == rumour_id:
                return rumour
        return None

    def add_rumour(self, title: str, source: str, credibility_score: int) -> Dict:
        """Add a new rumour."""
        new_rumour = {
            "rumourId": self._next_id(),
            "title": title,
            "source": source,
            "createdDate": date.today().isoformat(),
            "credibilityScore": credibility_score,
            "status": STATUS_NORMAL,
            "verified": None,
            "verifiedBy": None,
            "verifiedDate": None,
        }
        self._rumours.append(new_rumour)
        self.save()
        return new_rumour

    def update_status(self, rumour_id: str, status: str) -> bool:
        """Update the status of a rumour."""
        rumour = self.get_by_id(rumour_id)
        if not rumour:
            return False
        rumour["status"] = status
        self.save()
        return True

    def update_verified(self, rumour_id: str, verified: bool, verified_by: str) -> bool:
        """Update verification information for a rumour."""
        rumour = self.get_by_id(rumour_id)
        if not rumour:
            return False
        rumour["verified"] = verified
        rumour["verifiedBy"] = verified_by
        rumour["verifiedDate"] = date.today().isoformat()
        self.save()
        return True

    def is_verified(self, rumour: Dict) -> bool:
        """Check if a rumour has been verified."""
        return rumour.get("verified") is not None

    def is_panic(self, rumour: Dict) -> bool:
        """Check if a rumour is in panic status."""
        return rumour.get("status") == STATUS_PANIC

    def is_normal(self, rumour: Dict) -> bool:
        """Check if a rumour is in normal status."""
        return rumour.get("status") == STATUS_NORMAL

    def _next_id(self) -> str:
        """Generate next rumour ID."""
        max_id = 10000000
        for rumour in self._rumours:
            rumour_id = rumour.get("rumourId", "")
            if rumour_id.isdigit():
                max_id = max(max_id, int(rumour_id))
        return str(max_id + 1)

