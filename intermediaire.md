# Compte rendu intermédaire du projet d'outils d'imagerie pour la robotique

## Contexte
Ce projet se place dans le cadre joint de notre parcours en spécialité robotique de 3e année à l'Enseirb-Matmeca, ainsi
que dans le contexte de la RoboCup et notamment le traitement des images des caméras embarquées sur les robots.

Notre projet consiste à développer des outils de traitement d'image pour la détection de terrain de football.

## Explication de la méthode

![Alt text](./activite.svg?raw=true "Title")

Prenons en entrée une image BGR en provenance de la caméra du robot.
Une première partie du traitement servira à préparer l'image pour la détection qui suivra. 
Pour ce faire nous appliquons successivement un flou gaussien, puis une égalisation d'histogramme sur le canal Y après 
une conversion préalable en espace HSV (pour ne pas altérer la couleur en appliquant cette égalisation sur les 3 canaux de BGR)

Ensuite nous effectuons un seuillage. Avant ca, l'image obtenue est passée en HSV afin de pouvoir réaliser un seuillage efficace sur la couleur verte, suivi d'une dilatation et d'une érosion pour éliminer les petits artefacts.

En résulte alors un masque binaire, contenant différentes composantes connexes. Nous allons donc cherché à ne conserver 
que la plus grande pour obtenir le masque final.

Enfin, pour avoir un rendu visuel, le mask est appliqué bit à bit sur l'image originale.

![Alt text](./montage.png?raw=true "Title")

## Analyse et test des résultats 

Le fichier `test.py` permet de tester la méthode sur une liste d'images données.
Pour évaluer nos résultats, nous nous sommes basés sur les masques de référence fournies avec le sujet (`mask-field/log1/*`).
L'évaluation est pour l'instant une simple différence pixel à pixel, pour obtenir un pourcentage d'erreur. 
Le script renvoie la moyenne de ces erreurs.


## Architecture du projet
Le fichier `field_detector.py` contient une classe du même nom qui est composée de toutes les fonctions nécessaires au traitement de l'image fournie.
Le fichier `main.py` est celui à lancer pour exécuter le projet. Il peut se lancer au choix sur une vidéo pour afficher le rendu en temps réel, ou sur une simple image pour étudier le processus plus en détail.

## Parenthèse machine learning
En parallèle de cela, nous avons mené des recherches sur les différents types d'algorithmes de traitement d'image par intelligence artificielle. 
Le choix le plus adapté serait une IA de segmentation de type R-CNN ou MASK R-CNN, mais la complexité de la mise en oeuvre en plus des problèmes liés à la taille de la base de données nous ont fait abandonner cette piste pour ce projet.


## Suite du projet
Il nous faudra par la suite continuer d'améliorer notre détection pure du terrain de foot.
Il faudrait aussi réfléchir à traiter plus en détail le cas des lignes blanches du terrain.
Enfin nous pourrions imaginer une segmentation du terrain en fonction des lignes pour séparer les 2 cotés et labéliser les différentes parties.
