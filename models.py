#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
models.py - Objets et collecte des métriques SysWatch (POO)
"""

from __future__ import annotations

import platform
import json
import psutil
from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Any


@dataclass
class SystemMetrics:
    """
    Représente un ensemble de métriques système.
    """

    timestamp: datetime
    hostname: str
    cpu_percent: float
    memory_total: int
    memory_available: int
    memory_percent: float
    disk_usage: Dict[str, Any]

    def to_dict(self) -> dict:
        """Convertit l'objet en dict pour la base SQLite."""
        return {
            "timestamp": self.timestamp.isoformat(),
            "hostname": self.hostname,
            "cpu_percent": self.cpu_percent,
            "memory_total": self.memory_total,
            "memory_available": self.memory_available,
            "memory_percent": self.memory_percent,
            "disk_usage": json.dumps(self.disk_usage),
        }

    def __str__(self) -> str:
        """Affichage lisible d'une ligne de métriques."""
        ts = self.timestamp.strftime("%Y-%m-%d %H:%M:%S")
        return (
            f"[{ts}] {self.hostname} | "
            f"CPU: {self.cpu_percent:.1f}% | "
            f"RAM: {self.memory_percent:.1f}%"
        )


class SystemCollector:
    """
    Collecteur de métriques basé sur psutil.
    """

    def __init__(self, hostname: str = None):
        self.hostname = hostname or platform.node()

    def collect(self) -> SystemMetrics:
        """Retourne un objet SystemMetrics contenant toutes les métriques."""
        now = datetime.now()

        cpu_percent = psutil.cpu_percent(interval=1)

        mem = psutil.virtual_memory()
        memory_total = mem.total
        memory_available = mem.available
        memory_percent = mem.percent

        disk_data = {}
        for part in psutil.disk_partitions():
            try:
                usage = psutil.disk_usage(part.mountpoint)
                disk_data[part.mountpoint] = {
                    "total": usage.total,
                    "used": usage.used,
                    "percent": usage.percent,
                }
            except PermissionError:
                continue

        return SystemMetrics(
            timestamp=now,
            hostname=self.hostname,
            cpu_percent=cpu_percent,
            memory_total=memory_total,
            memory_available=memory_available,
            memory_percent=memory_percent,
            disk_usage=disk_data,
        )
