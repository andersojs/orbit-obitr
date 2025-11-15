from __future__ import annotations

import json
import threading
from copy import deepcopy
from pathlib import Path
from typing import Any, Dict, List, Optional


class RsoStore:
    """Thread-safe JSON-backed store for resident space objects."""

    def __init__(self, path: Path):
        self.path = path
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._lock = threading.Lock()
        if not self.path.exists():
            self._write([])

    def seed(self, records: List[Dict[str, Any]]) -> None:
        """Populate the store if it is empty."""
        with self._lock:
            current = self._read()
            if current:
                return
            self._write(deepcopy(records))

    def list_all(self) -> List[Dict[str, Any]]:
        with self._lock:
            data = deepcopy(self._read())
        return sorted(data, key=lambda r: r.get("display_name", "").lower())

    def get(self, satcat_number: str) -> Optional[Dict[str, Any]]:
        satcat = str(satcat_number)
        with self._lock:
            for record in self._read():
                if record.get("satcat_number") == satcat:
                    return deepcopy(record)
        return None

    def create(self, record: Dict[str, Any]) -> Dict[str, Any]:
        satcat = record.get("satcat_number")
        if satcat is None:
            raise ValueError("satcat_number is required")

        with self._lock:
            data = self._read()
            if any(existing.get("satcat_number") == satcat for existing in data):
                raise ValueError(f"An RSO with SatCat {satcat} already exists.")
            data.append(deepcopy(record))
            self._write(data)
        return deepcopy(record)

    def replace(self, satcat_number: str, record: Dict[str, Any]) -> Dict[str, Any]:
        satcat = str(satcat_number)
        with self._lock:
            data = self._read()
            replaced = False
            for idx, existing in enumerate(data):
                if existing.get("satcat_number") == satcat:
                    data[idx] = deepcopy(record)
                    replaced = True
                    break
            if not replaced:
                raise KeyError(f"RSO with SatCat {satcat} was not found.")
            self._write(data)
        return deepcopy(record)

    def delete(self, satcat_number: str) -> None:
        satcat = str(satcat_number)
        with self._lock:
            data = self._read()
            new_data = [deepcopy(record) for record in data if record.get("satcat_number") != satcat]
            if len(new_data) == len(data):
                raise KeyError(f"RSO with SatCat {satcat} was not found.")
            self._write(new_data)

    def _read(self) -> List[Dict[str, Any]]:
        with self.path.open("r", encoding="utf-8") as fp:
            try:
                return json.load(fp)
            except json.JSONDecodeError:
                return []

    def _write(self, data: List[Dict[str, Any]]) -> None:
        with self.path.open("w", encoding="utf-8") as fp:
            json.dump(data, fp, indent=2, sort_keys=True)
