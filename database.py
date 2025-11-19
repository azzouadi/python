#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
database.py - Gestion de la base SQLite pour SysWatch.
"""

from __future__ import annotations

import sqlite3
import json
import datetime
from typing import List, Dict, Any

from models import SystemMetrics


class MetricsDatabase:
    """
    Classe permettant la gestion de la base SQLite SysWatch.
    """

    def __init__(self, path: str = "syswatch.db") -> None:
        self.path = path
        self._init_schema()

    def _get_connection(self) -> sqlite3.Connection:
        """Retourne une connexion SQLite prête à l'emploi."""
        conn = sqlite3.connect(self.path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_schema(self) -> None:
        """Création des tables si elles n'existent pas."""
        conn = self._get_connection()
        with conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS metrics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    hostname TEXT NOT NULL,
                    cpu_percent REAL NOT NULL,
                    memory_percent REAL NOT NULL,
                    memory_total INTEGER NOT NULL,
                    memory_available INTEGER NOT NULL,
                    disk_usage TEXT
                )
                """
            )
            conn.execute(
                """
                CREATE INDEX IF NOT EXISTS idx_metrics_ts_host
                ON metrics(timestamp, hostname)
                """
            )
        conn.close()

    def save(self, metrics: SystemMetrics) -> None:
        """Enregistre un objet SystemMetrics dans la base."""
        data = metrics.to_dict()
        ts_str = metrics.timestamp.isoformat(timespec="seconds")

        disk_usage = data.get("disk_usage")
        if isinstance(disk_usage, (dict, list)):
            disk_usage_json = json.dumps(disk_usage)
        else:
            disk_usage_json = str(disk_usage)

        conn = self._get_connection()
        with conn:
            conn.execute(
                """
                INSERT INTO metrics (
                    timestamp, hostname,
                    cpu_percent, memory_percent,
                    memory_total, memory_available,
                    disk_usage
                )
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    ts_str,
                    data.get("hostname"),
                    data.get("cpu_percent"),
                    data.get("memory_percent"),
                    data.get("memory_total"),
                    data.get("memory_available"),
                    disk_usage_json,
                ),
            )
        conn.close()

    def get_latest(self, hostname: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Retourne les dernières lignes pour un hostname donné."""
        conn = self._get_connection()
        cur = conn.cursor()
        cur.execute(
            """
            SELECT
                timestamp, hostname,
                cpu_percent, memory_percent,
                memory_total, memory_available,
                disk_usage
            FROM metrics
            WHERE hostname = ?
            ORDER BY timestamp DESC
            LIMIT ?
            """,
            (hostname, limit),
        )
        rows = cur.fetchall()
        conn.close()
        return [dict(r) for r in rows]

    def get_statistics(self, hostname: str, hours: int = 24) -> Dict[str, Any]:
        """Retourne des statistiques (moyenne, min, max) sur une période donnée."""
        conn = self._get_connection()
        cur = conn.cursor()

        since_dt = datetime.datetime.now() - datetime.timedelta(hours=hours)
        since_str = since_dt.isoformat(timespec="seconds")

        cur.execute(
            """
            SELECT
                COUNT(*) AS count,
                AVG(cpu_percent) AS cpu_avg,
                MIN(cpu_percent) AS cpu_min,
                MAX(cpu_percent) AS cpu_max,
                AVG(memory_percent) AS mem_avg,
                MIN(memory_percent) AS mem_min,
                MAX(memory_percent) AS mem_max
            FROM metrics
            WHERE hostname = ?
              AND timestamp >= ?
            """,
            (hostname, since_str),
        )
        row = cur.fetchone()
        conn.close()

        if not row or row["count"] == 0:
            return {}

        return {
            "count": row["count"],
            "cpu": {
                "avg": row["cpu_avg"],
                "min": row["cpu_min"],
                "max": row["cpu_max"],
            },
            "memory": {
                "avg": row["mem_avg"],
                "min": row["mem_min"],
                "max": row["mem_max"],
            },
            "since": since_str,
        }

    def cleanup_old(self, days: int = 30) -> int:
        """Supprime les données plus anciennes que X jours."""
        conn = self._get_connection()
        cutoff_dt = datetime.datetime.now() - datetime.timedelta(days=days)
        cutoff_str = cutoff_dt.isoformat(timespec="seconds")

        with conn:
            cur = conn.execute(
                "DELETE FROM metrics WHERE timestamp < ?", (cutoff_str,)
            )
            deleted = cur.rowcount

        conn.close()
        return deleted

    def close(self) -> None:
        """
        Méthode volontairement vide.
        Chaque requête utilise sa propre connexion, donc rien à fermer ici.
        """
        pass
