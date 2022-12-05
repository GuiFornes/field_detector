# Compte rendu intermédaire du projet d'outils d'imagerie pour la robotique

## Contexte
Ce projet se place dans le cadre joint de notre parcours en spécialité robotique de 3e année à l'Enseirb-Matmeca, ainsi
que dans le contexte de la RoboCup et notamment le traitement des images des caméras embarquées sur les robots.

Notre projet consiste à développer des outils de traitement d'image pour la détection de terrain de football.

## Explication de la méthode

Prenons en entrée une image BGR en provenance de la caméra du robot.
Une première partie du traitement servira à préparer l'image pour la détection qui suivra. 
Pour ce faire nous appliquons successivement un flou gaussien, puis une égalisation d'histogramme sur le channel Y après 
une conversion préalable en espace YUV (pour ne pas altérer la couleur en appliquant cette égalisation sur les 3 channels de BGR)

Ensuite un seuillage, l'image obtenue est passée en HSV afin de pouvoir réaliser un seuillage efficace sur la couleur 
verte, suivi d'une dilatation et d'une érosion pour éliminer les petits artefacts.

En résulte alors un masque binaire, contenant différentes composantes connexes. Nous allons donc chercher à ne conserver 
que la plus grande pour obtenir le masque final.

Enfin, pour avoir un rendu visuel, le mask est appliqué bit à bit sur l'image originale.
![Alt text](./activite.png?raw=true "Title")

## Structure du projet
Le fichier field_detector.py contient la classe FieldDetector contient une classe du même nom

## Suite du projet

### problèmes

### idées de solutions