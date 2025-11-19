#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
SysWatch v3.0 - Export, collecte continue et statistiques.
"""

import argparse
import csv
import json
import os
import time

import collector
import traitement

HISTORIQUE_CSV = "syswatch_history.csv"
DERNIER_JSON = "syswatch_last.json"


def octets_vers_go(octets):
    """
    Convertit un nombre d'octets en gigaoctets formatés.

    Args:
        octets (int | float): taille en octets

    Retourne:
        str: taille formatée, ex: "16.00 GB"
    """
    go = octets / (1024 ** 3)
    return f"{go:.2f} GB"


def afficher_infos_systeme(data_systeme):
    """
    Affiche les informations générales du système.

    Args:
        data_systeme (dict): dictionnaire retourné par collecter_info_systeme()
    """
    print("=== Système ===")
    print(f"OS: {data_systeme.get('os')}")
    print(f"Version: {data_systeme.get('version')}")
    print(f"Architecture: {data_systeme.get('architecture')}")
    print(f"Hostname: {data_systeme.get('hostname')}")
    print()


def afficher_cpu(data_cpu):
    """
    Affiche les informations CPU.

    Args:
        data_cpu (dict): dictionnaire retourné par collecter_cpu()
    """
    print("=== CPU ===")
    print(f"Coeurs physiques: {data_cpu.get('coeurs_physiques')}")
    print(f"Coeurs logiques: {data_cpu.get('coeurs_logiques')}")
    print(f"Utilisation: {data_cpu.get('utilisation'):.2f}%")
    print()


def afficher_memoire(data_memoire):
    """
    Affiche les informations mémoire.

    Args:
        data_memoire (dict): dictionnaire retourné par collecter_memoire()
    """
    print("=== Mémoire ===")
    total = data_memoire.get("total", 0)
    disponible = data_memoire.get("disponible", 0)
    pourcentage = data_memoire.get("pourcentage", 0.0)

    print(f"Total: {octets_vers_go(total)}")
    print(f"Disponible: {octets_vers_go(disponible)}")
    print(f"Utilisation: {pourcentage:.2f}%")
    print()


def afficher_disques(data_disques):
    """
    Affiche les informations sur les disques.

    Args:
        data_disques (list[dict]): liste retournée par collecter_disques()
    """
    print("=== Disques ===")
    if not data_disques:
        print("Aucune partition accessible.")
    else:
        for disque in data_disques:
            point = disque.get("point_montage")
            pourcentage = disque.get("pourcentage", 0.0)
            print(f"{point} : {pourcentage:.2f}% utilisé")
    print()


def afficher_entete(timestamp):
    """
    Affiche l'en-tête du script avec la version et le timestamp.

    Args:
        timestamp (str): date/heure de la collecte des données
    """
    print("=== SysWatch v3.0 ===")
    print(f"Timestamp: {timestamp}")
    print()


def exporter_csv(metriques, fichier):
    """
    Exporte les métriques dans un fichier CSV (ajout si le fichier existe).

    Args:
        metriques (dict): dictionnaire retourné par collecter_tout()
        fichier (str): chemin du fichier CSV
    """
    # Préparation de la ligne à écrire
    systeme = metriques.get("systeme", {})
    cpu = metriques.get("cpu", {})
    mem = metriques.get("memoire", {})
    disques = metriques.get("disques", [])

    # On cherche la partition root "/"
    disk_root_percent = ""
    for d in disques:
        if d.get("point_montage") == "/":
            disk_root_percent = d.get("pourcentage", "")
            break

    row = {
        "timestamp": metriques.get("timestamp", ""),
        "hostname": systeme.get("hostname", ""),
        "cpu_percent": cpu.get("utilisation", 0.0),
        "mem_total_gb": mem.get("total", 0) / (1024 ** 3),
        "mem_dispo_gb": mem.get("disponible", 0) / (1024 ** 3),
        "mem_percent": mem.get("pourcentage", 0.0),
        "disk_root_percent": disk_root_percent,
    }

    file_exists = os.path.exists(fichier)
    write_header = not file_exists or os.path.getsize(fichier) == 0

    with open(fichier, mode="a", encoding="utf-8", newline="") as f:
        fieldnames = [
            "timestamp",
            "hostname",
            "cpu_percent",
            "mem_total_gb",
            "mem_dispo_gb",
            "mem_percent",
            "disk_root_percent",
        ]
        writer = csv.DictWriter(f, fieldnames=fieldnames)

        if write_header:
            writer.writeheader()

        writer.writerow(row)


def exporter_json(metriques, fichier):
    """
    Exporte les métriques complètes dans un fichier JSON lisible.

    Args:
        metriques (dict): dictionnaire retourné par collecter_tout()
        fichier (str): chemin du fichier JSON
    """
    with open(fichier, mode="w", encoding="utf-8") as f:
        json.dump(metriques, f, indent=2, ensure_ascii=False)


def collecter_en_continu(intervalle: int, nombre: int):
    """
    Collecte les métriques en continu.

    Args:
        intervalle (int): secondes entre chaque collecte.
        nombre (int): nombre de collectes (0 = infini).
    """
    compteur = 0
    try:
        while True:
            if nombre > 0 and compteur >= nombre:
                break

            metriques = collector.collecter_tout()

            # Affichage
            afficher_entete(metriques.get("timestamp"))
            afficher_infos_systeme(metriques.get("systeme", {}))
            afficher_cpu(metriques.get("cpu", {}))
            afficher_memoire(metriques.get("memoire", {}))
            afficher_disques(metriques.get("disques", []))

            # Export CSV
            exporter_csv(metriques, HISTORIQUE_CSV)

            compteur += 1

            if nombre == 0 or compteur < nombre:
                time.sleep(intervalle)

    except KeyboardInterrupt:
        print("\nArrêt de la collecte continue (Ctrl+C détecté).")


def afficher_stats(fichier_csv: str):
    """
    Affiche les statistiques de base à partir du fichier CSV.

    Args:
        fichier_csv (str): chemin du fichier CSV d'historique.
    """
    stats = traitement.calculer_moyennes(fichier_csv)

    if stats["cpu"]["moyenne"] is None:
        print("Aucune donnée disponible pour les statistiques.")
        return

    print("=== Statistiques CPU ===")
    print(f"Moyenne: {stats['cpu']['moyenne']:.2f}%")
    print(f"Min: {stats['cpu']['min']:.2f}%")
    print(f"Max: {stats['cpu']['max']:.2f}%")
    print()

    print("=== Statistiques Mémoire ===")
    print(f"Moyenne: {stats['memoire']['moyenne']:.2f}%")
    print(f"Min: {stats['memoire']['min']:.2f}%")
    print(f"Max: {stats['memoire']['max']:.2f}%")
    print()

    # On peut aussi afficher les pics (seuils choisis arbitrairement)
    pics = traitement.detecter_pics(fichier_csv, seuil_cpu=80.0, seuil_mem=80.0)
    if pics:
        print("=== Pics détectés (CPU > 80% ou RAM > 80%) ===")
        for p in pics:
            print(
                f"{p['timestamp']} - {p['hostname']} "
                f"(CPU: {p['cpu_percent']:.2f}%, RAM: {p['mem_percent']:.2f}%)"
            )
    else:
        print("Aucun pic détecté au-dessus des seuils 80% CPU / 80% RAM.")


def parse_arguments():
    """
    Analyse les arguments de la ligne de commande.

    Retourne:
        argparse.Namespace: les arguments parsés.
    """
    parser = argparse.ArgumentParser(description="SysWatch v3 - Monitoring système.")
    parser.add_argument(
        "--continu",
        action="store_true",
        help="Active la collecte continue.",
    )
    parser.add_argument(
        "--intervalle",
        type=int,
        default=10,
        help="Intervalle en secondes entre les collectes en mode continu (défaut: 10).",
    )
    parser.add_argument(
        "--nombre",
        type=int,
        default=0,
        help="Nombre de collectes en mode continu (0 = infini).",
    )
    parser.add_argument(
        "--stats",
        action="store_true",
        help="Affiche les statistiques à partir du fichier CSV d'historique.",
    )

    return parser.parse_args()


def main():
    """
    Point d'entrée principal du script SysWatch v3.0.
    """
    args = parse_arguments()

    # Mode statistiques
    if args.stats:
        afficher_stats(HISTORIQUE_CSV)
        return

    # Mode collecte continue
    if args.continu:
        collecter_en_continu(args.intervalle, args.nombre)
        return

    # Mode collecte unique (par défaut)
    metriques = collector.collecter_tout()

    afficher_entete(metriques.get("timestamp"))
    afficher_infos_systeme(metriques.get("systeme", {}))
    afficher_cpu(metriques.get("cpu", {}))
    afficher_memoire(metriques.get("memoire", {}))
    afficher_disques(metriques.get("disques", []))

    # Export des données
    exporter_csv(metriques, HISTORIQUE_CSV)
    exporter_json(metriques, DERNIER_JSON)


if __name__ == "__main__":
    main()
