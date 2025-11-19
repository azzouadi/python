#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Module traitement - fonctions de statistiques pour SysWatch.
"""

import csv
from typing import Dict, Any, List


def calculer_moyennes(fichier_csv: str) -> Dict[str, Dict[str, float]]:
    """
    Calcule les statistiques (moyenne, min, max) pour le CPU et la mémoire
    à partir d'un fichier CSV d'historique.

    Args:
        fichier_csv (str): chemin du fichier CSV.

    Retourne:
        dict: {
            'cpu': {'moyenne': float, 'min': float, 'max': float},
            'memoire': {'moyenne': float, 'min': float, 'max': float}
        }

    Si le fichier est vide ou introuvable, retourne des valeurs None.
    """
    stats = {
        "cpu": {"moyenne": None, "min": None, "max": None},
        "memoire": {"moyenne": None, "min": None, "max": None},
    }

    try:
        with open(fichier_csv, mode="r", encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)
            cpu_vals = []
            mem_vals = []

            for row in reader:
                try:
                    cpu = float(row.get("cpu_percent", "").strip() or 0.0)
                    mem = float(row.get("mem_percent", "").strip() or 0.0)
                    cpu_vals.append(cpu)
                    mem_vals.append(mem)
                except ValueError:
                    # Ligne invalide, on l'ignore
                    continue

        if cpu_vals and mem_vals:
            stats["cpu"]["moyenne"] = sum(cpu_vals) / len(cpu_vals)
            stats["cpu"]["min"] = min(cpu_vals)
            stats["cpu"]["max"] = max(cpu_vals)

            stats["memoire"]["moyenne"] = sum(mem_vals) / len(mem_vals)
            stats["memoire"]["min"] = min(mem_vals)
            stats["memoire"]["max"] = max(mem_vals)

    except FileNotFoundError:
        # Fichier inexistant : on laisse les valeurs à None
        pass

    return stats


def detecter_pics(
    fichier_csv: str, seuil_cpu: float, seuil_mem: float
) -> List[Dict[str, Any]]:
    """
    Détecte les pics de charge CPU ou mémoire à partir d'un fichier CSV.

    Args:
        fichier_csv (str): chemin du fichier CSV.
        seuil_cpu (float): seuil de déclenchement pour le CPU (%).
        seuil_mem (float): seuil de déclenchement pour la mémoire (%).

    Retourne:
        list[dict]: liste de dictionnaires avec les pics détectés :
            {
                'timestamp': str,
                'hostname': str,
                'cpu_percent': float,
                'mem_percent': float
            }
    """
    pics = []

    try:
        with open(fichier_csv, mode="r", encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)

            for row in reader:
                try:
                    cpu = float(row.get("cpu_percent", "").strip() or 0.0)
                    mem = float(row.get("mem_percent", "").strip() or 0.0)
                except ValueError:
                    continue

                if cpu > seuil_cpu or mem > seuil_mem:
                    pics.append(
                        {
                            "timestamp": row.get("timestamp", ""),
                            "hostname": row.get("hostname", ""),
                            "cpu_percent": cpu,
                            "mem_percent": mem,
                        }
                    )
    except FileNotFoundError:
        # Pas de fichier = pas de pics
        return []

    return pics
