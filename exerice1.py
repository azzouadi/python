#Exercice 1
def saluer_personne(nom, heure):
    """Retourne un message de salutation selon l'heure donnée."""
    if 6 <= heure < 12:
        return f"Bonjour {nom} !"
    elif 12 <= heure < 18:
        return f"Bon après-midi {nom} !"
    elif 18 <= heure < 24:
        return f"Bonsoir {nom} !"
    else:
        return f"Bonne nuit {nom} !"


print(saluer_personne("Azzouz", 10))
print(saluer_personne("Azzouz", 15))
print(saluer_personne("Azzouz", 20))
print(saluer_personne("Azzouz", 2))


