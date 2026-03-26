Texas Hold'em Poker Hand Evaluator — TDD Exam
Description
Ce projet implémente un évaluateur et comparateur de mains de poker Texas Hold'em, développé en TDD (Test-Driven Development) avec Python et pytest.

Installation
Prérequis

Python 3.10+
pip

Installation des dépendances
bashpip install -r requirements.txt
Lancer les tests
bashpytest
Pour voir le détail des tests :
bashpytest -v

Structure du projet
├── poker/
│   ├── __init__.py
│   ├── card.py               # Représentation d'une carte
│   └── hand_evaluator.py     # Évaluation et comparaison de mains de 5 cartes
├── tests/
│   ├── __init__.py
│   ├── test_card.py          # Tests de la classe Card
│   ├── test_comparison.py    # Tests de comparaison et départage
│   └── test_seven_card.py    # Tests de sélection de la meilleure main sur 7 cartes
└── requirements.txt

Représentation des cartes
Une carte est représentée par :

Une valeur : 2, 3, 4, 5, 6, 7, 8, 9, 10, J, Q, K, A
Une couleur : ♠, ♥, ♦, ♣

pythonfrom poker.card import Card

card = Card('A', '♠')  # As de pique

Ordre des combinaisons (du plus fort au plus faible)
RangCombinaison9Straight Flush8Four of a Kind7Full House6Flush5Straight4Three of a Kind3Two Pair2One Pair1High Card

La quinte flush royale (10, J, Q, K, A de même couleur) est traitée comme la meilleure Straight Flush, pas comme une catégorie séparée.


Ordre du chosen5 par catégorie
Le chosen5 (les 5 cartes retournées) est toujours ordonné de façon déterministe :
CatégorieOrdre des cartes retournéesStraight FlushDe la plus haute à la plus basse (roue : 5,4,3,2,A)Four of a KindLes 4 cartes du carré d'abord, puis le kickerFull HouseLes 3 cartes du brelan d'abord, puis la paireFlushOrdre décroissant des valeursStraightDe la plus haute à la plus basse (roue : 5,4,3,2,A)Three of a KindLes 3 cartes du brelan d'abord, puis kickers décroi.Two PairPaire haute, paire basse, puis kickerOne PairLes 2 cartes de la paire, puis 3 kickers décroissantsHigh CardOrdre décroissant des valeurs

Hypothèses sur les entrées

On suppose qu'il n'y a pas de cartes dupliquées dans une même partie (pas de validation active des doublons dans le code).
Les entrées sont des instances valides de la classe Card.


Ce qui a été implémenté

✅ Représentation des cartes (card.py)
✅ Détection des 9 combinaisons sur 5 cartes (hand_evaluator.py)
✅ Classement global des combinaisons
✅ Départage (tie-break) pour toutes les catégories
✅ Ordre déterministe du chosen5
✅ Sélection de la meilleure main parmi 7 cartes (seven_card_evaluator.py)
✅ Gestion du cas de l'as bas (A,2,3,4,5 → suite à 5 haute)
✅ Rejet du wrap-around (Q,K,A,2,3 est invalide)


Ce qui n'a pas été implémenté (par manque de temps)

❌ Comparaison multi-joueurs : la fonction principale qui prend un board de 5 cartes communes + N joueurs avec leurs 2 cartes en main, et retourne le ou les gagnants avec gestion du split pot, n'a pas été implémentée.
❌ Les tests associés à la comparaison multi-joueurs (test_comparison_multiplayer.py) n'ont pas été rédigés.
❌ Les exemples du sujet (exemples A à E) n'ont pas été couverts par des tests dédiés.

Ces fonctionnalités auraient constitué l'étape finale du projet. L'architecture du code est pensée pour les accueillir facilement : il suffirait d'ajouter un module game.py qui, pour chaque joueur, appelle SevenCardEvaluator.best_hand() puis compare les résultats via HandResult.

Cas limites couverts

As bas : A,2,3,4,5 est une suite valide avec le 5 comme carte haute (wheel)
As haut : 10,J,Q,K,A est une suite valide
Wrap-around invalide : Q,K,A,2,3 n'est pas une suite valide
Plus de 5 cartes de la même couleur : on sélectionne les 5 meilleures
Meilleur kicker : parmi 7 cartes, le meilleur kicker disponible est toujours sélectionné
