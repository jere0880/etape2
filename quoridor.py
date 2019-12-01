"""Étape2 du projet quoridor"""
import networkx as nx


class QuoridorError(Exception):
    """Classe qui indique qu'il y a une erreur quoridor"""


class Quoridor:
    """Classe qui créer un jeu quoridor"""
    def __init__(self, joueurs, murs=None):
        """Initialisation de la classe Quoridor"""
        #Vérification de l'itérabilité de joueurs
        if isinstance(joueurs, (int, float)):
            raise QuoridorError("joueurs n'est pas itérable")
        #Vérification que joueurs contient 2 éléments
        if len(joueurs) != 2:
            raise QuoridorError("L'itérable joueurs ne contient pas deux éléments")
        #Vérification que murs, si présent, est un dictionnaire
        if isinstance(murs, dict) is False and murs is not None:
            raise QuoridorError("murs ce doit d'être un dictionnaire")
        #Création des dictionnaires joueur
        joueur = []
        jeu = {}
        création_dictionnaire_joueur(joueurs, joueur, jeu)
        #Création de l'état de jeu et des dictionnaires murs
        if murs is None:
            jeu['joueurs'] = [joueur[0], joueur[1]]
            jeu['murs'] = {'horizontaux':[], 'verticaux': []}
            murs = {'horizontaux':[], 'verticaux': []}
        else:
            jeu['joueurs'], jeu['murs'] = [joueur[0], joueur[1]], murs
            nmurs = (len(murs['horizontaux'])
                     + len(murs['verticaux']) + joueur[0]['murs'] + joueur[1]['murs'])
            #Vérification du nombre de murs
            if nmurs != 20:
                raise QuoridorError('Nombre de murs invalide')
            #Vérification du nombre de murs
            if (joueur[0]['murs'] > 10 or joueur[1]['murs'] > 10
                    or joueur[0]['murs'] < 0 or joueur[1]['murs'] < 0):
                raise QuoridorError('Nombre de murs invalides')
            #Vérification de la position des murs
            self.murs = murs
            self.verifier_murs()
        #Vérification de la position des joueurs
        if (joueur[0]['pos'][0] not in range(1, 10)
                or joueur[1]['pos'][0] not in range(1, 10)
                or joueur[0]['pos'][1] not in range(1, 10)
                or joueur[1]['pos'][1] not in range(1, 10)):
            raise QuoridorError('Position invalide pour un joueur')
        self.jeu = jeu
        self.nom = [self.jeu['joueurs'][0]['nom'], self.jeu['joueurs'][1]['nom']]
    def __str__(self):
        """Méthode qui retourn l'état de jeu sous forme de damier ascii"""
        table = []
        let = [['  |', '    ', '    ', '    ', '    ', '    ', '    ', '    ', '    ', '   |'],
               ['  |', '    ', '    ', '    ', '    ', '    ', '    ', '    ', '    ', '   |'],
               ['  |', '    ', '    ', '    ', '    ', '    ', '    ', '    ', '    ', '   |'],
               ['  |', '    ', '    ', '    ', '    ', '    ', '    ', '    ', '    ', '   |'],
               ['  |', '    ', '    ', '    ', '    ', '    ', '    ', '    ', '    ', '   |'],
               ['  |', '    ', '    ', '    ', '    ', '    ', '    ', '    ', '    ', '   |'],
               ['  |', '    ', '    ', '    ', '    ', '    ', '    ', '    ', '    ', '   |'],
               ['  |', '    ', '    ', '    ', '    ', '    ', '    ', '    ', '    ', '   |'],
               ['  |', '    ', '    ', '    ', '    ', '    ', '    ', '    ', '    ', '   |']]
        while len(table) < 9:
            table.append([[' ', '.', ' ', ' '], [' ', '.', ' ', ' '],
                          [' ', '.', ' ', ' '], [' ', '.', ' ', ' '],
                          [' ', '.', ' ', ' '], [' ', '.', ' ', ' '],
                          [' ', '.', ' ', ' '], [' ', '.', ' ', ' '], [' ', '.', ' ']])
        nj = 1
        for joueur in self.jeu['joueurs']:
            table[joueur['pos'][1] - 1][joueur['pos'][0] - 1][1] = str(nj)
            nj += 1
        for mur in self.jeu['murs']['horizontaux']:
            let[mur[1] - 1][mur[0]] = '----'
            let[mur[1] - 1][mur[0] + 1] = '--- '
            if mur[0] == 8:
                let[mur[1] - 1][mur[0]] = '----'
                let[mur[1] - 1][mur[0] + 1] = '---|'
        for m in self.jeu['murs']['verticaux']:
            table[m[1] - 1][m[0] - 2][3] = '|'
            table[m[1]][m[0] - 2][3] = '|'
            if let[m[1]][m[0] - 1] == '--- ':
                let[m[1]][m[0] - 1] = '---|'
            else:
                let[m[1]][m[0] - 1] = '   |'
        nl = 9
        for index, line in enumerate(table):
            for index2, variable in enumerate(line):
                table[index][index2] = ''.join(variable)
        damier = (f'Légende: 1={self.nom[0]}, 2={self.nom[1]}'
                  + '\n' + '   -----------------------------------')
        for li in reversed(table):
            if nl == 1:
                damier += '\n' + f'{nl} |' + ''.join((li)) + '|'
            else:
                damier += '\n' + f'{nl} |' + ''.join((li)) + '|' + '\n' + ''.join(let[nl - 1])
            nl -= 1
        damier += '\n' + '--|-----------------------------------'
        damier += '\n' + '  | 1   2   3   4   5   6   7   8   9'
        return damier
    def verifier_murs(self):
        """Méthode qui vérifie que la position des murs est valide"""
        mur = self.murs
        for index3, mh in enumerate(mur['horizontaux']):
            if mh[0] not in range(1, 9) or mh[1] not in range(2, 10):
                raise QuoridorError('Position de murs invalide')
            muh = mur['horizontaux'].copy()
            del muh[index3]
            for mhp in muh:
                if (mh[1] == mhp[1] and (mh[0] == mhp[0] or mh[0] == mhp[0] + 1)):
                    raise QuoridorError('Position de murs invalide')
            for murv in mur['verticaux']:
                if mh[0] == murv[0] - 1 and mh[1] == murv[1] + 1:
                    raise QuoridorError('un mur occupe déjà cette position')
        for index4, mv in enumerate(mur['verticaux']):
            if mv[0] not in range(2, 10) or mv[1] not in range(1, 9):
                raise QuoridorError('Position de murs invalide')
            muv = mur['verticaux'].copy()
            del muv[index4]
            for mvp in muv:
                if (mv[0] == mvp[0] and (mv[1] == mvp[1] or mv[1] == mvp[1] + 1)):
                    raise QuoridorError('Position de murs invalide')
            for murh in mur['horizontaux']:
                if murh[0] == mv[0] + 1 and murh[1] == mv[1] - 1:
                    raise QuoridorError('un mur occupe déjà cette position')
    def déplacer_jeton(self, joueur, position):
        """Méthode qui déplace le jeton"""
        # Le numero du joueur est autre que 1 ou 2.
        if joueur not in [1, 2]:
            raise QuoridorError('le numéro du joueur est autre que 1 ou 2.')
        # La position n'est pas entre 1 et 10 en x et y.
        if position[0] not in range(1, 10) or position[1] not in range(1, 10):
            raise QuoridorError('la position est invalide (en dehors du damier).')
        # Crée un graphe avec networkx et verifie si la position est disponible
        graphe = construire_graphe([joueur['pos'] for joueur in self.jeu['joueurs']],
                                   self.jeu['murs']['horizontaux'],
                                   self.jeu['murs']['verticaux'])
        if position not in list(graphe.successors(((
                tuple(self.jeu['joueurs'][joueur - 1]['pos']))))):
            raise QuoridorError("la position est invalide pour l'état actuel du jeu.")
        if position[1] == 9 and joueur == 1:
            self.jeu["gagnant"] = self.jeu['joueurs'][0]["nom"]
        if position[1] == 1 and joueur == 2:
            self.jeu["gagnant"] = self.jeu['joueurs'][1]["nom"]
        self.jeu['joueurs'][joueur - 1]["pos"] = position
    def état_partie(self):
        """Méthode qui retourne l'état de jeu sous forme de dictionnaire"""
        return self.jeu
    def final_jouer_coup(self, joueur, joueur2, graphe, pos1, pos2):
        """Méthode qui exécute la fin de la méthode jouer_coup"""
        for deplacement in nx.shortest_path(graphe, pos2, f'B{joueur2}')[1:]:
            # Si shortest path est en x = murv
            if deplacement[1] == pos2[1]:
                # Si deplacement vers la gauche, murv a gauche
                if deplacement[0] == pos2[0] - 1:
                    try:
                        self.placer_mur(joueur, tuple(map(sum,
                                                          zip(pos2,
                                                              (0, -1 * (2 - joueur2))))),
                                        'verticaux')
                        return
                    # Si on ne peut pas placer de mur à cet  endroit, on deplace notre pion
                    except QuoridorError:
                        try:
                            self.placer_mur(joueur, tuple(map(sum,
                                                              zip(pos2,
                                                                  (0, 1 - joueur2)))), 'verticaux')
                            return
                        except QuoridorError:
                            pos2 = deplacement
                            continue
                # murv a droite
                else:
                    try:
                        self.placer_mur(joueur, tuple(map(sum,
                                                          zip(pos2,
                                                              (1, -1 *(2 - joueur2))))),
                                        'verticaux')
                        return
                    except QuoridorError:
                        try:
                            self.placer_mur(joueur, tuple(map(sum,
                                                              zip(pos2,
                                                                  (1, 1 - joueur2)))), 'verticaux')
                            return
                        except QuoridorError:
                            pos2 = deplacement
                            continue
            # Si shortest path est en y = murh
            if deplacement[0] == pos2[0]:
                # Mur h devant le joueur si deplacement vers  l'objectif
                if deplacement[1] == pos2[1] + 1:
                    try:
                        self.placer_mur(joueur, tuple(map(sum,
                                                          zip(pos2,
                                                              (0, joueur - 1)))), 'horizontaux')
                        return
                    # Si on ne peut pas placer de mur à cet  endroit, on deplace notre pion
                    except QuoridorError:
                        try:
                            self.placer_mur(joueur, tuple(map(sum,
                                                              zip(pos2,
                                                                  (-1, joueur - 1)))),
                                            'horizontaux')
                            return
                        except QuoridorError:
                            pos2 = deplacement
                            continue
        # Si on ne peut pas placer de mur, on deplace le jeton
        self.déplacer_jeton(joueur, nx.shortest_path(graphe, pos1, f'B{joueur}')[1])
    def jouer_coup(self, joueur):
        """Méthode qui joue un coup automatique"""
        # Le numero du joueur est autre que 1 ou 2.
        if joueur not in [1, 2]:
            raise QuoridorError('le numéro du joueur est autre que 1 ou 2.')
        if self.partie_terminée():
            raise QuoridorError('La partie est déjà terminée.')
        # Crée un graphe  de l'état
        graphe = (construire_graphe([joueur['pos'] for joueur in self.jeu['joueurs']],
                                    self.jeu['murs']['horizontaux'],
                                    self.jeu['murs']['verticaux']))
        # Compare le joueur plus proche de la ligne d'arrivé
        joueur2 = 1
        if joueur == 1:
            joueur2 = 2
        # positions des joueurs
        pos1 = tuple(self.jeu['joueurs'][joueur - 1]['pos'])
        pos2 = tuple(self.jeu['joueurs'][joueur2 - 1]['pos'])
        # Si plus proche -> shortest path
        if (len(nx.shortest_path(graphe, pos1, f'B{joueur}'))
                <= len(nx.shortest_path(graphe, pos2, f'B{joueur2}'))):
            try:
                self.déplacer_jeton(joueur, nx.shortest_path(graphe, pos1, f'B{joueur}')[1])
                return
            except QuoridorError:
                raise QuoridorError('La partie est déjà terminée')
        # Si plus loin
        self.final_jouer_coup(joueur, joueur2, graphe, pos1, pos2)
    def partie_terminée(self):
        """Méthode qui vérifie si la partie est terminé"""
        if 'gagnant' in self.jeu:
            return self.jeu['gagnant']
        return False
    def verification_placer_mur(self, position, orientation, auorien):
        """Méthode qui vérifie que le mur qui est placé est placé dans une place libre"""
        for m in self.jeu['murs'][orientation]:
            if m[0] == position[0] and m[1] == position[1]:
                raise QuoridorError('un mur occupe déjà cette position')
            if orientation == 'horizontaux':
                if (m[1] == position[1] and (m[0] == position[0]
                                             or m[0] == position[0] - 1
                                             or m[0] == position[0] + 1)):
                    raise QuoridorError('un mur occupe déjà cette position')
            if orientation == 'verticaux':
                if (m[0] == position[0] and (m[1] == position[1]
                                             or m[1] == position[1] - 1
                                             or m[1] == position[1] + 1)):
                    raise QuoridorError('un mur occupe déjà cette position')
        for ma in self.jeu['murs'][auorien]:
            if orientation == 'horizontaux':
                if position[0] == ma[0] - 1 and position[1] == ma[1] + 1:
                    raise QuoridorError('un mur occupe déjà cette position')
            if orientation == 'verticaux':
                if position[0] == ma[0] + 1 and position[1] == ma[1] - 1:
                    raise QuoridorError('un mur occupe déjà cette position')
    def placer_mur(self, njoueur, position, orientation):
        """Méthode qui place un mur"""
        #Vérifie le numéro du joueur
        if njoueur not in [1, 2]:
            raise QuoridorError('le numéro du joueur est autre que 1 ou 2')
        #Identifie le joueur
        joueur = self.jeu['joueurs'][njoueur - 1]
        #Vérifie qu'il reste des murs à placer pour le joueur désigné
        if joueur['murs'] == 0:
            raise QuoridorError('le joueur a déjà placé tous ses murs')
        #Vérifie que la position est valide
        if orientation == 'horizontaux':
            auorien = 'verticaux'
            if position[0] < 1 or position[0] > 8 or position[1] < 2 or position[1] > 9:
                raise QuoridorError('la position est invalide pour cette orientation')
        if orientation == 'verticaux':
            auorien = 'horizontaux'
            if position[0] < 2 or position[0] > 9 or position[1] < 1 or position[1] > 8:
                raise QuoridorError('la position est invalide pour cette orientation')
        #Vérifie que la place est libre pour le mur
        self.verification_placer_mur(position, orientation, auorien)
        #Place le mur et enlève un mur au joueur qui place le mur
        joueur['murs'] -= 1
        self.jeu['murs'][orientation].append(position)
        # Vérifie que le mur placé ne bloque pas les joueurs
        graphe = construire_graphe([joueur['pos'] for joueur in self.jeu['joueurs']],
                                   self.jeu['murs']['horizontaux'],
                                   self.jeu['murs']['verticaux'])
        for i, joueur in enumerate(self.jeu['joueurs']):
            if not nx.has_path(graphe, tuple(joueur['pos']), f'B{i+1}'):
                self.jeu['murs'][orientation].pop()
                raise QuoridorError('La position du mur est invalide')
def création_dictionnaire_joueur(joueurs, joueur, jeu):
    """Création des joueurs pour le dictionnaire de jeu et vérification
    du gagnant."""
    for index5, jou in enumerate(joueurs):
        if isinstance(jou, str) and index5 == 0:
            joueur.append({'nom': jou, 'murs': 10, 'pos': (5, 1)})
        if isinstance(jou, str) and index5 == 1:
            joueur.append({'nom': jou, 'murs': 10, 'pos': (5, 9)})
        if isinstance(jou, dict):
            joueur.append(jou)
            if jou['pos'][1] == 9 and index5 == 0:
                jeu["gagnant"] = jou["nom"]
            if jou['pos'][1] == 1 and index5 == 1:
                jeu["gagnant"] = jou["nom"]
def construire_graphe(joueurs, murs_horizontaux, murs_verticaux):
    """Crée le graphe des déplacements admissibles pour les joueurs."""
    graphe = nx.DiGraph()
    # pour chaque colonne du damier
    for x in range(1, 10):
        # pour chaque ligne du damier
        for y in range(1, 10):
            # ajouter les arcs de tous les déplacements possibles pour cette tuile
            ajout_arcs(graphe, x, y)
    # retirer tous les arcs qui croisent les murs horizontaux
    for x, y in murs_horizontaux:
        graphe.remove_edge((x, y-1), (x, y))
        graphe.remove_edge((x, y), (x, y-1))
        graphe.remove_edge((x+1, y-1), (x+1, y))
        graphe.remove_edge((x+1, y), (x+1, y-1))
    # retirer tous les arcs qui croisent les murs verticaux
    for x, y in murs_verticaux:
        graphe.remove_edge((x-1, y), (x, y))
        graphe.remove_edge((x, y), (x-1, y))
        graphe.remove_edge((x-1, y+1), (x, y+1))
        graphe.remove_edge((x, y+1), (x-1, y+1))
    # retirer tous les arcs qui pointent vers les positions des joueurs
    # et ajouter les sauts en ligne droite ou en diagonale, selon le cas
    for joueur in map(tuple, joueurs):
        for prédécesseur in list(graphe.predecessors(joueur)):
            graphe.remove_edge(prédécesseur, joueur)
            # si admissible, ajouter un lien sauteur
            successeur = (2*joueur[0]-prédécesseur[0], 2*joueur[1]-prédécesseur[1])
            if successeur in graphe.successors(joueur) and successeur not in joueurs:
                # ajouter un saut en ligne droite
                graphe.add_edge(prédécesseur, successeur)
            else:
                # ajouter les liens en diagonal
                for successeur in list(graphe.successors(joueur)):
                    if prédécesseur != successeur and successeur not in joueurs:
                        graphe.add_edge(prédécesseur, successeur)
    # ajouter les noeuds objectifs des deux joueurs
    for x in range(1, 10):
        graphe.add_edge((x, 9), 'B1')
        graphe.add_edge((x, 1), 'B2')
    return graphe

def ajout_arcs(graphe, x, y):
    """Ajoute les arcs de tous les déplacements possibles pour une tuile"""
    if x > 1:
        graphe.add_edge((x, y), (x-1, y))
    if x < 9:
        graphe.add_edge((x, y), (x+1, y))
    if y > 1:
        graphe.add_edge((x, y), (x, y-1))
    if y < 9:
        graphe.add_edge((x, y), (x, y+1))
