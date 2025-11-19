def calculer_prix_ttc(prix_ht, taux_tva = 20):
    """
    Calcule le prix TTC à partir d'un prix HT.

    Args:
        prix_ht (float): le prix hors taxe
        taux_tva (float, optional): taux de TVA. Par défaut 20%.
    """

    prix_ttc = prix_ht * (1 + taux_tva / 100)

    return round(prix_ttc, 2)


try:
    saisie = input("Entrez le prix ht : ")

    # Conversion en float (peut déclencher une ValueError)
    prix_ht = float(saisie)

    # Appel de la fonction
    prix_ttc = calculer_prix_ttc(prix_ht)

    # Affichage du résultat
    print(f"Voici le prix ttc {prix_ttc} euros")

except TypeError:
    print("Erreur : le type de donnée est invalide.")

except ValueError as e:
    print(e)
