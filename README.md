Partie 1 – Apprentissages fondamentaux

Avant de développer SysWatch, j’ai réalisé quatre exercices visant à comprendre les bases de Python.

    
    
    Exercice 1 : Fonction de salutation

Objectif : créer une fonction qui renvoie un message différent en fonction de l’heure.

Compétences acquises :

conditions if / elif / else

formats de chaînes (f-strings)

gestion de paramètres dans une fonction

    
    
    Exercice 2 : Calcul du prix TTC

Objectif : demander un prix HT, appliquer une TVA et retourner le prix TTC.

Compétences acquises :

saisie utilisateur avec input()

conversions (float())

arrondi (round())

gestion d’erreurs try / except

    
    
    Exercice 3 : Validation de mot de passe

Objectif : vérifier qu’un mot de passe contient :

au moins 8 caractères

au moins une majuscule

au moins un chiffre

Compétences acquises :

boucles for

méthodes de chaînes (isdigit(), isupper())

logique booléenne

fonctions retournant True ou False

    
    
    Exercice 4 : Liste de courses + sauvegarde fichier

Objectif : gérer une liste (ajouter, retirer, afficher, compter) et la sauvegarder dans un fichier .txt.

Compétences acquises :

manipulation de listes Python

ouverture/écriture de fichiers (fonction open())

modularisation simple (plusieurs fonctions pour un même programme)



    
    SysWatch v1 – Première version (collecte + affichage)

Cette version introduit :

l’utilisation du module platform

l’utilisation du module psutil (CPU, RAM, disques)

des fonctions d’affichage simples

Objectif : découvrir comment récupérer des informations système en Python.

    
    
    SysWatch v2 – Organisation modulaire

Séparation du code en plusieurs fichiers :

collector.py → collecte des métriques

syswatch_v2.py → affichage et logique utilisateur

Compétences acquises :

architecture modulaire

import de modules personnalisés

structuration propre d’un projet Python

    
    
    SysWatch v3 – Export, statistiques et CLI

Ajout de fonctionnalités avancées :

     Export des données

export CSV

export JSON

accumulation des données dans le temps

     Statistiques

CPU / RAM : moyenne, min, max

détection de pics (> 80%)

    Mode collecte continue

intervalle paramétrable

nombre de collectes configurable

interruption propre (Ctrl+C)

    CLI (arguments dans le terminal)

Exemples :

python syswatch_v3.py --continu --intervalle 30
python syswatch_v3.py --stats


Compétences acquises :

manipulation de fichiers CSV/JSON

module argparse

automatisation de scripts Python

gestion d’une boucle de monitoring

    
    
    SysWatch v4 – Version finale (POO + SQLite)

Cette version finalise le projet avec :


1. Programmation Orientée Objet

SystemCollector → collecte des métriques

SystemMetrics → structure de données

utilisation de @dataclass


2. Base de données SQLite

insertion des métriques

récupération des dernières valeurs

statistiques sur 24h

nettoyage automatique des anciennes données

3. Application complète en ligne de commande

Exemples :

python syswatch_v4.py --collect --interval 60
python syswatch_v4.py --stats --hours 12
python syswatch_v4.py --export syswatch.json
python syswatch_v4.py --cleanup 7

