# field_detector
Detect football fields limit for RoboCup's robot

## Installation

Start by cloning the repository:
    
        git clone https://github.com/GuiFornes/field_detector.git 

Follow the option below that matches your case. We recommend using a virtual environment:

1. [Installation with a virtual environment](#virtual)
2. [Installation without virtual environment](#nonvirtual)
3. [Installation with windows](#windows)


### <a name="virtual"></a> Installation with a virtual environment

1. Creating a virtual environment

        python3 -m venv venv 

2. Activating the virtual environment

        source ./venv/bin/activate

3. Installing dependencies

        pip install -r requirements.txt

### <a name="nonvirtual"></a> Installation without virtual environment 
_This option is not recommended due to the risk of library non-compatibilities or version issues_

1. Installing dependencies

        pip install -r requirements.txt



##  <a name="usage"></a> Usage

1. Run the script to detect the field limits in one image

        python3 main.py <path_to_image>

2. Run the script to detect the field limits in a video

        python3 main.py <path_to_folder>

3. Run the test script to evaluate the method precision with pre-masked images

        python3 test.py 

## Project structure

    .
    ├── README.md
    ├── requirements.txt
    ├── .gitignore
    ├── main.py
    ├── main_live_video.py
    ├── field_detector.py
    ├── test.py
    ├── data
    │   ├── ...
    ├── mask-field
    │   ├── ...

### Project files
Le fichier `field_detector.py` contient une classe du même nom qui est composée de toutes les fonctions nécessaires au traitement de l'image fournie.

Le fichier `main.py` est celui à lancer pour exécuter le projet. Il peut se lancer au choix sur une vidéo pour afficher le rendu en temps réel, ou sur une simple image pour étudier le processus plus en détail.

Les dossiers `data` et `mask-field` contiennent respectivement les images à traiter et des masques solutions exemples pour certaines d'entre-elles

### Test file

Le fichier `test.py` execute le projet sur une liste d'images exemple au masque prédéfini pour comparer les résultats.
il affiche par la même occasion les masques résultats les moins précis.

Quelques illustrations des éléments qui peuvent perturber notre perception du terrain :
L'image en haut à gauche est l'originale, en bas à gauche post pré-traitement, en haut à droite le masque obtenu et en bas à droite le masque cible fourni dans le sujet.

![Alt text](./images/erreur1.png?raw=true "Title")
Figure 1 : Erreur venant d'un élément extérieur (ici une personne)

![Alt text](./images/erreur_flou.png?raw=true "Title")
Figure 2 : Erreur venant du flou de l'image (l'angle du terrain est mal perçu)

![Alt text](./images/erreur_ligne.png?raw=true "Title")
Figure 3 : Erreur venant des lignes du terrain (le terrain à l'intérieur de la cage n'est pas détecté)
