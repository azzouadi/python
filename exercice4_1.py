def afficher_liste(courses):
    if len(courses) == 0:
        print(" La liste de courses est vide")
        return
 
    print(" Liste de courses :")
    print("=" * 40)
    for i, article in enumerate(courses, 1):
        print(f"  {i}. {article}")
    print("=" * 40)
    print(f"Total : {len(courses)} article(s)")
 
 
def ajouter_article(courses, article):
    if not article or article.strip() == "":
        print("Erreur : l'article ne peut pas être vide")
        return courses
 
    if article in courses:
        print(f"  '{article}' est déjà dans la liste")
        return courses
 
    courses.append(article)
    print(f"✓ '{article}' ajouté à la liste")
    return courses
 
 
def retirer_article(courses, article):
    if article in courses:
        courses.remove(article)
        print(f" '{article}' retiré de la liste")
    else:
        print(f" '{article}' n'est pas dans la liste")
 
    return courses
 
 
def compter_articles(courses):
    return len(courses)
 
 
# Programme principal
def main():
    ma_liste_courses = []
 
    print("Bienvenue dans le gestionnaire de liste de courses !\n")
 
    # Ajouts
    ajouter_article(ma_liste_courses, "Pain")
    ajouter_article(ma_liste_courses, "Lait")
    ajouter_article(ma_liste_courses, "Œufs")
    ajouter_article(ma_liste_courses, "Beurre")
    print()
 
    afficher_liste(ma_liste_courses)
    print()
 
    ajouter_article(ma_liste_courses, "Pain")
    print()
 
    retirer_article(ma_liste_courses, "Lait")
    print()
 
    afficher_liste(ma_liste_courses)
    print()
 
    nb_articles = compter_articles(ma_liste_courses)
    print(f"Vous avez {nb_articles} article(s) dans votre liste\n")
 
    #     EXPORT FICHIER
    try:
        with open("liste_courses.txt", "w", encoding="utf-8") as f:
            f.write("Liste de courses\n")
            f.write("=" * 40 + "\n")
            for i, item in enumerate(ma_liste_courses, 1):
                f.write(f"{i}. {item}\n")
            f.write("=" * 40 + "\n")
            f.write(f"Total : {nb_articles} article(s)\n")
 
        print("Ta'liste_courses.txt' a été créer !")
 
    except Exception as e:
        print("Erreur lors de la création du fichier :", e)
 
 
if __name__ == "__main__":
    main()