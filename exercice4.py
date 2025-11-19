def afficher_liste(courses):
    """
    Affiche tous les articles de la liste de courses.
    """
    if len(courses) == 0:
        print("La liste est vide.")
    else:
        print("Liste de courses :")
        for article in courses:
            print("-", article)


def ajouter_article(courses, article):
    """
    Ajoute un article à la liste de courses.
    """
    courses.append(article)


def retirer_article(courses, article):
    """
    Retire un article de la liste si présent.
    """
    if article in courses:
        courses.remove(article)
    else:
        print(f"{article} n'est pas dans la liste.")


def compter_articles(courses):
    """
    Retourne le nombre total d'articles dans la liste.
    """
    return len(courses)



courses = []  # Liste vide au départ

# Ajouts
ajouter_article(courses, "Pommes")
ajouter_article(courses, "Lait")
ajouter_article(courses, "Pain")

# Affichage
afficher_liste(courses)

# Retrait
retirer_article(courses, "Lait")

# Affichage après retrait
afficher_liste(courses)

# Compter les articles
print("Nombre d'articles :", compter_articles(courses))
