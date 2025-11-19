import collector 


def octets_vers_go(octets):
    """
    Convertit un nombre d'octets en chaîne formatée en Go.

    Args:
        octets (int): taille en octets

    Retourne:
        str: texte du type "16.00 GB"
    """
    go = octets / (1024 ** 3)
    return f"{go:.2f} GB"


def afficher_systeme(data_systeme):
    """
    Affiche les informations système à partir du dict retourné par collecter_info_systeme().
    """
    print("=== Système ===")
    print(f"OS: {data_systeme['os']}")
    print(f"Version: {data_systeme['version']}")
    print(f"Architecture: {data_systeme['architecture']}")
    print(f"Hostname: {data_systeme['hostname']}")
    print()  # ligne vide


def afficher_cpu(data_cpu):
    """
    Affiche les informations CPU à partir du dict retourné par collecter_cpu().
    """
    print("=== CPU ===")
    print(f"Coeurs physiques: {data_cpu['coeurs_physiques']}")
    print(f"Coeurs logiques: {data_cpu['coeurs_logiques']}")
    print(f"Utilisation: {data_cpu['utilisation']:.1f}%")
    print()  # ligne vide


def afficher_memoire(data_memoire):
    """
    Affiche les informations mémoire à partir du dict retourné par collecter_memoire().
    """
    print("=== Mémoire ===")
    print(f"Total: {octets_vers_go(data_memoire['total'])}")
    print(f"Disponible: {octets_vers_go(data_memoire['disponible'])}")
    print(f"Utilisation: {data_memoire['pourcentage']:.1f}%")
    print()  # ligne vide


def afficher_disques(data_disques):
    """
    Affiche les informations sur les disques à partir
    de la liste retournée par collecter_disques().
    """
    print("=== Disques ===")
    if not data_disques:
        print("Aucune partition détectée.")
    else:
        for disque in data_disques:
            point = disque["point_montage"]
            pourcentage = disque["pourcentage"]
            print(f"{point} : {pourcentage:.1f}% utilisé")
    print()  # ligne vide


def main():
    """
    Point d'entrée principal de SysWatch v2.
    Utilise collector.collecter_tout() puis affiche les données.
    """
    toutes_donnees = collector.collecter_tout()

    print("=== SysWatch v2.0 ===")
    print(f"Timestamp: {toutes_donnees['timestamp']}\n")

    afficher_systeme(toutes_donnees["systeme"])
    afficher_cpu(toutes_donnees["cpu"])
    afficher_memoire(toutes_donnees["memoire"])
    afficher_disques(toutes_donnees["disques"])


if __name__ == "__main__":
    main()