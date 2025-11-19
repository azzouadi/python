import platform   # Infos sur le système (OS, version, architecture, etc.)
import psutil     # Metrics système (CPU, RAM, disques)
import sys        # Pour la version de Python


def afficher_infos_systeme():
    """
    Affiche les informations générales du système.
    """
    print("=== Système ===")
    print(f"OS: {platform.system()}")
    print(f"Version: {platform.release()}")
    print(f"Architecture: {platform.machine()}")
    print(f"Hostname: {platform.node()}")
    print(f"Python: {sys.version.split()[0]}")
    print()  # ligne vide


def afficher_cpu():
    """
    Affiche les informations CPU :
    - coeurs physiques
    - coeurs logiques
    - pourcentage d'utilisation
    """
    print("=== CPU ===")
    coeurs_physiques = psutil.cpu_count(logical=False)
    coeurs_logiques = psutil.cpu_count(logical=True)
    utilisation = psutil.cpu_percent(interval=1)  # mesure sur 1 seconde

    print(f"Coeurs physiques: {coeurs_physiques}")
    print(f"Coeurs logiques: {coeurs_logiques}")
    print(f"Utilisation: {utilisation:.1f}%")
    print()  # ligne vide


def afficher_memoire():
    """
    Affiche les informations mémoire (RAM) :
    - total en Go
    - disponible en Go
    - pourcentage d'utilisation
    """
    print("=== Mémoire ===")
    mem = psutil.virtual_memory()

    # Conversion octets -> Go (1 Go = 1024^3 octets)
    total_go = mem.total / (1024 ** 3)
    disponible_go = mem.available / (1024 ** 3)

    print(f"Total: {total_go:.2f} GB")
    print(f"Disponible: {disponible_go:.2f} GB")
    print(f"Utilisation: {mem.percent:.1f}%")
    print() 


def afficher_disques():
    """
    Affiche les informations sur les disques :
    - point de montage
    - pourcentage d'utilisation

    Les partitions inaccessibles (permissions) sont ignorées.
    """
    print("=== Disques ===")
    partitions = psutil.disk_partitions()

    for part in partitions:
        try:
            usage = psutil.disk_usage(part.mountpoint)
            print(f"{part.mountpoint} : {usage.percent:.1f}% utilisé")
        except PermissionError:
            # Certaines partitions système peuvent être protégées
            # On les ignore juste.
            continue
    print()  # ligne vide


def main():
    """
    Point d'entrée principal du script SysWatch v1.
    Appelle les différentes fonctions d'affichage.
    """
    print("=== SysWatch PARTIE 1 ===\n")

    afficher_infos_systeme()
    afficher_cpu()
    afficher_memoire()
    afficher_disques()


if __name__ == "__main__":
    main()
