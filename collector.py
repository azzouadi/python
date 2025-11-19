import platform
import psutil
from datetime import datetime


def collecter_info_systeme():
    """
    Collecte les informations générales du système.

    Retourne:
        dict: {
            'os': ...,
            'version': ...,
            'architecture': ...,
            'hostname': ...
        }
    """
    info = {
        "os": platform.system(),
        "version": platform.release(),
        "architecture": platform.machine(),
        "hostname": platform.node(),
    }
    return info


def collecter_cpu():
    """
    Collecte les informations CPU.

    Retourne:
        dict: {
            'coeurs_physiques': int,
            'coeurs_logiques': int,
            'utilisation': float
        }
    """
    data = {
        "coeurs_physiques": psutil.cpu_count(logical=False),
        "coeurs_logiques": psutil.cpu_count(logical=True),
        "utilisation": psutil.cpu_percent(interval=1),  # mesure sur 1s
    }
    return data


def collecter_memoire():
    """
    Collecte les informations mémoire (RAM).

    Retourne:
        dict: {
            'total': int (octets),
            'disponible': int (octets),
            'pourcentage': float
        }
    """
    mem = psutil.virtual_memory()

    data = {
        "total": mem.total,
        "disponible": mem.available,
        "pourcentage": mem.percent,
    }
    return data


def collecter_disques():
    """
    Collecte les informations sur les disques.

    Retourne:
        list[dict]: une liste de dictionnaires, un par partition :
            {
                'point_montage': str,
                'total': int (octets),
                'utilise': int (octets),
                'pourcentage': float
            }
    Les partitions inaccessibles (permissions) sont ignorées.
    """
    resultats = []

    partitions = psutil.disk_partitions()
    for part in partitions:
        try:
            usage = psutil.disk_usage(part.mountpoint)
            data_part = {
                "point_montage": part.mountpoint,
                "total": usage.total,
                "utilise": usage.used,
                "pourcentage": usage.percent,
            }
            resultats.append(data_part)
        except PermissionError:
            # On ignore simplement les partitions auxquelles on n'a pas accès
            continue

    return resultats


def collecter_tout():
    """
    Collecte toutes les métriques et les regroupe dans un seul dictionnaire.

    Retourne:
        dict: {
            'timestamp': str,
            'systeme': {...},
            'cpu': {...},
            'memoire': {...},
            'disques': [...]
        }
    """
    donnees = {
        "timestamp": datetime.now().isoformat(),  # ex: "2025-11-19T10:23:45.123456"
        "systeme": collecter_info_systeme(),
        "cpu": collecter_cpu(),
        "memoire": collecter_memoire(),
        "disques": collecter_disques(),
    }
    return donnees
