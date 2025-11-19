import argparse
import json
import time

from models import SystemCollector
from database import MetricsDatabase


def afficher_stats(db: MetricsDatabase, hostname: str, heures: int = 24) -> None:
    """
    Affiche les statistiques pour un host sur une période donnée.
    """
    stats = db.get_statistics(hostname, heures)
    if not stats:
        print("⚠️ Aucune donnée pour ce host / cette période.")
        return

    print(f"=== Statistiques pour {hostname} sur {heures}h ===")
    print(f"Nombre de mesures : {stats['nb']}")
    print("--- CPU (%) ---")
    print(f"  Moyenne : {stats['cpu_moy']:.2f}")
    print(f"  Min     : {stats['cpu_min']:.2f}")
    print(f"  Max     : {stats['cpu_max']:.2f}")
    print("--- RAM (%) ---")
    print(f"  Moyenne : {stats['mem_moy']:.2f}")
    print(f"  Min     : {stats['mem_min']:.2f}")
    print(f"  Max     : {stats['mem_max']:.2f}")


def exporter_json_recent(db: MetricsDatabase, hostname: str, fichier: str) -> None:
    """
    Exporte les dernières métriques d'un host en JSON.
    """
    rows = db.get_latest(hostname, limit=100)
    with open(fichier, "w", encoding="utf-8") as f:
        json.dump(rows, f, indent=2)
    print(f"✅ Export JSON effectué dans {fichier}")


def parser_arguments():
    parser = argparse.ArgumentParser(description="SysWatch final (POO + SQLite)")
    parser.add_argument(
        "--collect",
        action="store_true",
        help="mode collecte continue",
    )
    parser.add_argument(
        "--interval",
        type=int,
        default=60,
        help="intervalle entre collectes (secondes, défaut 60)",
    )
    parser.add_argument(
        "--stats",
        action="store_true",
        help="afficher les statistiques",
    )
    parser.add_argument(
        "--hours",
        type=int,
        default=24,
        help="période en heures pour les stats (défaut 24)",
    )
    parser.add_argument(
        "--export",
        metavar="FICHIER",
        help="exporter les dernières métriques en JSON",
    )
    parser.add_argument(
        "--cleanup",
        type=int,
        metavar="JOURS",
        help="supprimer les données plus anciennes que JOURS",
    )
    return parser.parse_args()


def boucle_collecte(collector: SystemCollector, db: MetricsDatabase, interval: int):
    """
    Boucle de collecte continue :
    - collecter
    - afficher
    - sauvegarder
    """
    try:
        while True:
            metrics = collector.collect()
            print(metrics)  # utilise __str__
            db.save(metrics)
            time.sleep(interval)
    except KeyboardInterrupt:
        print("\n🛑 Collecte interrompue par l'utilisateur.")


def main():
    args = parser_arguments()

    collector = SystemCollector()
    hostname = collector.hostname
    db = MetricsDatabase()

    try:
        # Nettoyage si demandé
        if args.cleanup is not None:
            nb = db.cleanup_old(args.cleanup)
            print(f"🧹 {nb} entrées anciennes supprimées.")

        # Export JSON si demandé
        if args.export:
            exporter_json_recent(db, hostname, args.export)

        # Affichage des stats si demandé
        if args.stats:
            afficher_stats(db, hostname, args.hours)

        # Mode collecte continue
        if args.collect:
            boucle_collecte(collector, db, args.interval)
        elif not (args.stats or args.export or args.cleanup):
            # Si aucune option : une seule collecte + sauvegarde
            metrics = collector.collect()
            print(metrics)
            db.save(metrics)

    finally:
        db.close()


if __name__ == "__main__":
    main()
