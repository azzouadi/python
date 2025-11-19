def est_mot_de_passe_valide(mot_de_passe):
    """
    Vérifie si un mot de passe est valide.

    Conditions :
    - au moins 8 caractères
    - contient au moins un chiffre
    - contient au moins une majuscule

    Retour :
        True si valide, False sinon
    """

    # Vérification de la longueur
    if len(mot_de_passe) < 8:
        return False

    # Vérification de la présence d'un chiffre
    contient_chiffre = False
    for caractere in mot_de_passe:
        if caractere.isdigit():
            contient_chiffre = True
            break

    if not contient_chiffre:
        return False

    # Vérification de la présence d'une majuscule
    contient_majuscule = False
    for caractere in mot_de_passe:
        if caractere.isupper():
            contient_majuscule = True
            break

    if not contient_majuscule:
        return False

    return True


# Tests d'exemples
print(est_mot_de_passe_valide("Password123"))   # True
print(est_mot_de_passe_valide("password123"))   # False (pas de majuscule)
