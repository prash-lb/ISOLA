from upemtk import *
from random import randint


def dessine_plateau(plateau, taille_case):
    """
    Permet d'afficher le plateau visuellement et afficher les noms des collonnes ainsi que les lignes.
    """
    lettre = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U",
              "V", "W", "X", "Y", "Z"]
    cree_fenetre(((len(plateau[0]) + 1) * taille_case) + taille_case, ((len(plateau)) + 1) * taille_case + taille_case)
    rectangle(0, 0, (len(plateau[0]) + 1) * taille_case + taille_case, (len(plateau) + 1) * taille_case + taille_case,
              remplissage="#992e43")

    for largueur_plateau in range(1, len(plateau) + 1):
        texte(25, (largueur_plateau * taille_case) + 25, lettre[largueur_plateau - 1])
        for longueur_plateau in range(1, (len(plateau[largueur_plateau - 1])) + 1):
            rectangle(longueur_plateau * taille_case, (largueur_plateau * taille_case),
                      (longueur_plateau + 1) * taille_case,
                      (largueur_plateau + 1) * taille_case, epaisseur=3, remplissage="#992e43")

    for collonne in range(1, len(plateau[0]) + 1):
        texte((taille_case * collonne) + 25, 20, str(collonne))

    mise_a_jour()


def pion(color, joueur, lst_joueur, plateau):
    """
    Permet d'afficher les pion dans la fenetre ainsi que sur la liste plateau
    """
    plateau[(lst_joueur[1]) - 1][(lst_joueur[0]) - 1] = 0
    cercle((lst_joueur[0] * taille_case) + (taille_case / 2), (lst_joueur[1] * taille_case) + (taille_case / 2),
           taille_case / 2, remplissage=color, tag=joueur)
    plateau[(lst_joueur[1]) - 1][(lst_joueur[0]) - 1] = 1


def verfication_pion_joueur(lst_joueur1, lst_joueur2,
                            plateau, tag_joueur, couleur_pion):
    """
    Va vérifier si le joueur 1 et le joueur 2 ont les mêmes coordonnées dés le début de la partie
    >>>lst_joueur1 = [5,5]
       lst_joueur2 = [5,5]
       plateau = [[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0]]
       verification_pion_ia(lst_joueur1, lst_joueur2, plateau)
       lst_joueur2 = [randint(1, len(plateau[0])), randint(1, len(plateau[0]))]
       lst_joueur1 = [5,5]
    """
    while lst_joueur1 == lst_joueur2:
        lst_joueur2 = [randint(1, len(plateau[0])), randint(1, len(plateau[0]))]
        pion(couleur_pion, tag_joueur, lst_joueur2, plateau)
    return lst_joueur1, lst_joueur2


def recuper_liste_meilleur_case(case_libre, plateau):
    """
    recevant une liste des case accesible et renvoyant parmie ces cases accessibles les meilleurs cases permettant
    le plus de possibilite de deplacement .
    >>>recuper_liste_meilleur_case([[3, 5], [4, 5], [5, 5], [5, 6]],plateau)
    [[3, 5], [5, 5]]
    """
    lst_case = []
    lst_possibiliter = []
    for case in case_libre:
        lst_prochaine_case_libre = case_alentour_adjacent(case, plateau)
        nb_possibiliter = len(verification_deplacement_pion(lst_prochaine_case_libre, plateau))
        lst_possibiliter.append(nb_possibiliter)
    max_possibiliter = max(lst_possibiliter)
    lst_possibiliter_max = [i for i, element in enumerate(lst_possibiliter) if element == max_possibiliter]
    for i in lst_possibiliter_max:
        lst_case.append(case_libre[i])
    return lst_case


def deplacement_pion(couleur, joueur_tag, joueur, plateau, ia, cavalier):
    """
    Permet le déplacement des pions en fonction du mode
    >>>joueur2 = [4,4]
    >>>plateau = [[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0]]
    >>>deplacement_pion("red", "joueur2", joueur2, plateau, False,False)
    case_libre_joueur = [[5,4],[3,4],[4,5],[4,3],[5,5],[5,3],[3,5],[3,3]]
    """

    if cavalier:
        case_libre_joueur = case_alentour_cavalier(joueur, plateau)
    else:
        case_libre_joueur = case_alentour_adjacent(joueur, plateau)

    case_libre = verification_deplacement_pion(case_libre_joueur, plateau)
    affichage_case_deplacement_possible(case_libre)
    if case_libre == []:
        return False, True
    if ia:
        case_libre_ia = recuper_liste_meilleur_case(case_libre, plateau)
        position = randint(0, len(case_libre_ia) - 1)
        nv_x, nv_y = case_libre_ia[position][0], case_libre_ia[position][1]
        nv_deplacement = [[nv_x, nv_y]]
    else:
        x, y = attend_clic_gauche()
        nv_x, nv_y = x // taille_case, y // taille_case
        nv_deplacement = [[nv_x, nv_y]]
    efface("case_libre")

    if nv_deplacement[0] in case_libre:
        plateau[(joueur[1]) - 1][(joueur[0] - 1)] = 0
        joueur[0], joueur[1] = nv_x, nv_y
        efface(joueur_tag)
        pion(couleur, joueur_tag, joueur, plateau)
        plateau[(nv_y) - 1][(nv_x) - 1] = 1
        mise_a_jour()
        return False, False
    return True, False


def verification_deplacement_pion(case_libre_joueur,
                                  plateau):
    """
    Vérifie les cases accesible pour le joueur, les case vide.Recois une liste des case autour du joueur et
    renvoi une liste des case vide
    >>>verification_deplacement_pion([[3, 4], [3, 5], [3, 6], [4, 4], [4, 6], [5, 4], [5, 5], [5, 6]],plateau)
    [[3, 5], [3, 6], [4, 4], [4, 6], [5, 4], [5, 5], [5, 6]]
    """

    nv_case_libre_joueur = []
    for case in range(len(case_libre_joueur)):
        if plateau[(case_libre_joueur[case][1]) - 1][(case_libre_joueur[case][0]) - 1] == 0:
            nv_case_libre_joueur.append(case_libre_joueur[case])
    return nv_case_libre_joueur


def affichage_case_deplacement_possible(nv_case_libre_joueur):
    """
    Affiche les cases où les joueurs peuvents se déplacer en vert
    """
    for i in nv_case_libre_joueur:
        rectangle(i[0] * taille_case, i[1] * taille_case, (i[0] + 1) * taille_case,
                  (i[1] + 1) * taille_case, remplissage="green", tag="case_libre")
    mise_a_jour()


def case_alentour_adjacent(joueur, plateau):
    """
    cree une liste des case accessibles par le joueur en retirant les cases prise par un joueur ainsi que les cases noirs

    >>>joueur1 = [4,4]
    >>>plateau = [[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0]]
    >>>case_alentour_adjacent(joueur1, plateau)
    case_libre=[[5,4],[3,4],[4,5],[4,3],[5,5],[5,3],[3,5],[3,3]]
    """
    case_libre = []
    pos_x = joueur[0]
    pos_y = joueur[1]
    for i in range(pos_x - 1, pos_x + 2):
        for j in range(pos_y - 1, pos_y + 2):
            if i < 1 or i > len(plateau[0]) or j < 1 or j > len(plateau) or (i == pos_x and j == pos_y):
                continue
            case_libre.append([i, j])

    return case_libre


def case_alentour_cavalier(joueur, plateau):
    """
    cree une liste des case accessible par le joueur a la mainier d'un cavalier
    en retirant les cases prise par un joueur ainsi que les cases noir

    >>>joueur1 = [4,4]
       plateau = [[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0]]
       case_alentour_adjacent(joueur1, plateau)
       case_libre=[[5,6],[4,6],[5,2],[6,2],[6,5],[6,3],[2,5],[2,3]]
    """

    case_libre = []
    pos_x = joueur[0]
    pos_y = joueur[1]
    for y in range(-2, 4, 4):
        for x in range(-1, 2, 2):
            posit_x = pos_x + x
            posit_y = pos_y + y
            if posit_x < 1 or posit_x > len(plateau[0]) or posit_y < 1 or posit_y > len(plateau) or (
                    posit_x == pos_x and posit_y == pos_y):
                continue
            case_libre.append([pos_x + x, pos_y + y])
    for y in range(-1, 2, 2):
        for x in range(-2, 4, 4):
            posit_x = pos_x + x
            posit_y = pos_y + y
            if posit_x < 1 or posit_x > len(plateau[0]) or posit_y < 1 or posit_y > len(plateau) or (
                    posit_x == pos_x and posit_y == pos_y):
                continue
            case_libre.append([pos_x + x, pos_y + y])
    return case_libre


def case_noir(plateau, ia, joueur_adverse):
    """
    Fonction posant une case noir sur le plateau sur la case selectionner et renvoyant un False une fois la case
    noir poser.
    >>>case_noir(plateau,False,[3,3])
    True
    """
    if ia:
        case_libre_joueur_adverse = case_alentour_adjacent(joueur_adverse, plateau)
        case_noir_ia = verification_deplacement_pion(case_libre_joueur_adverse, plateau)
        liste_meilleur_case_noir = recuper_liste_meilleur_case(case_noir_ia, plateau)
        if len(case_noir_ia) > 0:
            case_ia = randint(0, len(liste_meilleur_case_noir) - 1)
            case_noir_x, case_noir_y = liste_meilleur_case_noir[case_ia][0], liste_meilleur_case_noir[case_ia][1]


        else:
            return False
    else:
        x, y = attend_clic_gauche()
        case_noir_x, case_noir_y = x // taille_case, y // taille_case
    if case_noir_x <= len(plateau[0]) and case_noir_y <= len(plateau):
        if plateau[(case_noir_y) - 1][(case_noir_x) - 1] == 0 and case_noir_x > 0 and case_noir_y > 0:
            plateau[(case_noir_y) - 1][(case_noir_x) - 1] = 2
            rectangle(case_noir_x * taille_case, case_noir_y * taille_case, (case_noir_x + 1) * taille_case,
                      (case_noir_y + 1) * taille_case, remplissage="black")
            return False
    return True


def dimension_plateau(dimension):
    """
    Créé une liste avec des sous liste dans lequel chaque sous liste equivaut à une ligne d'un tableau et chaque element
     d'une sous liste equivaut a une collonne du plateau

    >>>dimension_plateau([6,6])
    [[0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]]

    """

    plateau = []
    for _ in range(dimension[0]):
        ligne_plateau = []
        for _ in range(dimension[1]):
            ligne_plateau.append(0)
        plateau.append(ligne_plateau)
    return plateau


def defaite(vainqueur, joueur):
    """"
    renvoie False lorsque vainquer vaut True et renvoi aussi le nom du perdant

    >>> defaite(True,"joueur1")
    False,"joueur1"
    """
    if vainqueur:
        return False, joueur
    return True, joueur


def button(coordonne_button, x_souris, y_souris):
    """
    Vérifie si on appuie sur l'un des bouton ou non
    >>> button((100, 125, 150, 175), 120, 140)
    True
    """
    if x_souris > coordonne_button[0] and x_souris < coordonne_button[2] and y_souris > coordonne_button[
        1] and y_souris < coordonne_button[3]:
        return True
    return False


def menu_accueil():
    """
    Va afficher notre menu d'acceuil et qui va activer les mode de jeu selectionnés
    :return: 0,1,2,3,4
    """
    rectangle(0, 0, 600, 450, remplissage="#133337")
    texte(190, 50, "MODES DE JEU", "blue")
    rectangle(200, 120, 400, 170, 'black', 'medium aquamarine')
    texte(220, 130, " 2 JOUEUR")
    rectangle(200, 320, 400, 370, 'black', '#E51944')
    texte(280, 330, "IA")
    rectangle(200, 220, 400, 270, 'black', '#E00D0D')
    texte(220, 230, "CAVALIER")
    rectangle(450, 330, 590, 370, 'black', '#4c830d')
    texte(450, 330, "QUITTER")
    x_souris, y_souris = attend_clic_gauche()
    ia = button([200, 320, 400, 370], x_souris, y_souris)
    mode_2_joueur = button([200, 120, 400, 170], x_souris, y_souris)
    cavalier = button([200, 220, 400, 270], x_souris, y_souris)
    quitter = button([450, 330, 590, 370], x_souris, y_souris)
    if ia:
        return 1
    elif mode_2_joueur:
        return 2
    elif cavalier:
        return 3
    elif quitter:
        return 4
    else:
        return 0


def menu_rejouer(vainqueur, mode):
    """
    Va afficher notre menu rejouer et qui va permettre de rejouer ou de retourner  au menu d'acceuil
    """
    ferme_fenetre()
    cree_fenetre(600, 450)
    rectangle(0, 0, 600, 450, remplissage="#01a0d6")
    texte(150, 100, str(vainqueur) + (" A PERDU"), taille=30, couleur="#07004b")
    rectangle(240, 200, 400, 240, 'black', 'green')
    texte(240, 200, " REJOUER")
    rectangle(240, 300, 400, 340, 'black', '#E00D0D')
    texte(250, 300, "RETOUR")
    x_souris, y_souris = attend_clic_gauche()
    rejouer_menu_de_fin = button((240, 200, 400, 240), x_souris, y_souris)
    quitter_menu_fin = button((240, 300, 400, 340), x_souris, y_souris)
    if rejouer_menu_de_fin:
        return mode
    elif quitter_menu_fin:
        return 0
    ferme_fenetre()


def menu_dimension(hauteur_tableau, longueur_tableau):
    """
    menu affichant la configuration du plateau, la hauteur ainsi que la longueur du tableau,renvoyant la hauteur ainsi
    que la longueur
    >>> menu_dimension(6,6)
    10,10
    """
    configue_dimension_tableau = True

    cree_fenetre(500, 500)

    while configue_dimension_tableau:
        rectangle(0, 0, 500, 500, remplissage="#133337")
        rectangle(225, 125, 275, 175, remplissage="white")
        # button configuration hauteur
        texte(50, 50, "Nombre de case en collonne")
        texte(235, 135, hauteur_tableau)
        rectangle(100, 125, 150, 175, remplissage="red")
        rectangle(110, 150, 140, 155, remplissage="black")
        rectangle(350, 125, 400, 175, remplissage="green")
        rectangle(360, 150, 390, 155, remplissage="black")
        rectangle(373, 135, 376, 165, remplissage="black")
        texte(50, 260, "Nombre de case en ligne")
        rectangle(225, 325, 275, 375, remplissage="white")
        texte(235, 335, longueur_tableau)
        rectangle(100, 325, 150, 375, remplissage="red")
        rectangle(110, 350, 140, 355, remplissage="black")
        rectangle(350, 325, 400, 375, remplissage="green")
        rectangle(360, 350, 390, 355, remplissage="black")
        rectangle(373, 335, 376, 365, remplissage="black")
        rectangle(180, 425, 300, 465, remplissage="purple")
        texte(190, 425, "JOUER")
        x_souris, y_souris = attend_clic_gauche()
        if button((180, 425, 300, 465), x_souris, y_souris):
            configue_dimension_tableau = False
        elif button((100, 125, 150, 175), x_souris, y_souris):
            hauteur_tableau -= 1
        elif button((350, 125, 400, 175), x_souris, y_souris):
            hauteur_tableau += 1
        elif button((100, 325, 150, 375), x_souris, y_souris):
            longueur_tableau -= 1
        elif button((350, 325, 400, 375), x_souris, y_souris):
            longueur_tableau += 1

    return longueur_tableau, hauteur_tableau


taille_case = 75
main = True
hauteur_tableau = 6
longueur_tableau = 6
cree_fenetre(600, 450)
while main:
    mode = menu_accueil()
    while mode >= 1:
        if mode == 4:
            main = False
            break
        ferme_fenetre()
        plateau = dimension_plateau(menu_dimension(hauteur_tableau, longueur_tableau))
        ferme_fenetre()
        tour_joueur = True
        tour_deplacement = True
        pose_case_noir = True
        rejouer = True
        vainqueur = False
        # pion
        dessine_plateau(plateau, taille_case)
        joueur1 = [randint(1, len(plateau[0])), randint(1, len(plateau))]
        pion("yellow", "joueur1", joueur1, plateau)
        if mode == 1:
            robot = [randint(1, len(plateau[0])), randint(1, len(plateau))]
            pion("grey", "ia", robot, plateau)
            joueur1, robot = verfication_pion_joueur(joueur1, robot, plateau, "ia", "grey")
        elif mode == 3 or mode == 2:
            joueur2 = [randint(1, len(plateau[0])), randint(1, len(plateau))]
            joueur1, joueur2 = verfication_pion_joueur(joueur1, joueur2, plateau, "joueur2", "red")
            pion("red", "joueur2", joueur2, plateau)

        while rejouer:
            # joueur 1
            while tour_joueur:
                while tour_deplacement:
                    if mode == 3:
                        tour_deplacement, vainqueur = deplacement_pion("yellow", "joueur1", joueur1, plateau, False,
                                                                       True)
                    else:
                        tour_deplacement, vainqueur = deplacement_pion("yellow", "joueur1", joueur1, plateau, False,
                                                                       False)
                if vainqueur:
                    tour_joueur = not tour_joueur
                    continue
                while pose_case_noir:
                    pose_case_noir = case_noir(plateau, False, None)
                tour_joueur = not tour_joueur

            rejouer, vainqueur_manche = defaite(vainqueur, "JOUEUR 1")
            # joueur adverse
            tour_deplacement = True
            pose_case_noir = True
            if rejouer:
                # joueur IA
                if mode == 1:
                    while not tour_joueur:
                        while tour_deplacement:
                            tour_deplacement, vainqueur = deplacement_pion("grey", "ia", robot, plateau, True, False)
                        if vainqueur:
                            tour_joueur = not tour_joueur
                            continue

                        while pose_case_noir:
                            pose_case_noir = case_noir(plateau, True, joueur1)
                        tour_joueur = not tour_joueur

                    rejouer, vainqueur_manche = defaite(vainqueur, "ia")
                else:
                    rejouer, vainqueur_manche = defaite(vainqueur, "JOUEUR 1")
                # JOUEUR 2
                while not tour_joueur:
                    while tour_deplacement:
                        if mode == 3:
                            tour_deplacement, vainqueur = deplacement_pion("red", "joueur2", joueur2, plateau, False,
                                                                           True)
                        else:
                            tour_deplacement, vainqueur = deplacement_pion("red", "joueur2", joueur2, plateau, False,
                                                                           False)
                    if vainqueur:
                        tour_joueur = not tour_joueur
                        continue
                    while pose_case_noir:
                        pose_case_noir = case_noir(plateau, False, None)
                    tour_joueur = not tour_joueur
                rejouer, vainqueur_manche = defaite(vainqueur, "JOUEUR 2")
                tour_deplacement = True
                pose_case_noir = True
        mode = menu_rejouer(vainqueur_manche, mode)
ferme_fenetre()