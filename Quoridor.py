import networkx as nx


class QuoridorError(Exception):
    def __init__(self, message):
        self.message = message
    def __str__(self):
        return str(self.message)



class Quoridor:
    def __init__(self, joueurs, murs=None):
        #Vérification de l'itérabilité de joueurs
        try:
            j = iter(joueurs)
        except TypeError as te:
            raise QuoridorError("joueurs n'est pas itérable")
        
        #Vérification que joueurs contient 2 éléments
        if len(joueurs) != 2:
            raise QuoridorError("L'itérable joueurs ne contient pas deux éléments")
        
        #Vérification que murs, si présent, est un dictionnaire
        if isinstance(murs, dict) is False and murs != None:
            raise QuoridorError("murs ce doit d'être un dictionnaire")
        
        #Création des dictionnaires joueur
        joueur = []
        for jou in joueurs:
            if isinstance(jou, str):
                joueur.append({'nom': jou, 'murs': 10, 'pos': (5,1)})
            if isinstance(jou, dict):
                joueur.append(jou)

        #Création de l'état de jeu et des dictionnaires murs
        if murs == None:
            jeu = {'joueurs': [joueur[0], joueur[1]], 'murs': {'horizontaux':[], 'verticaux': []}}
            murs = {'murs': {'horizontaux':[], 'verticaux': []}}
        else:
            jeu = {'joueurs': [joueur[0], joueur[1]], 'murs': murs}
            nmurs = len(murs['horizontaux']) + len(murs['verticaux']) + joueur[0]['murs'] + joueur[1]['murs']
            #Vérification du nombre de murs
            if nmurs != 20:
                raise QuoridorError('Nombre de murs invalide')
            #Vérification du nombre de murs
            if joueur[0]['murs'] > 10 or joueur[1]['murs'] > 10 or joueur[0]['murs'] < 0 or joueur[1]['murs'] < 0:
                raise QuoridorError('Nombre de murs invalides')
        
        #Vérification de la position des joueurs
        if joueur[0]['pos'][0] > 9 or joueur[1]['pos'][0] > 9 or joueur[0]['pos'][1] > 9 or joueur[1]['pos'][1] > 9:
            raise QuoridorError('Position invalide pour un joueur')
        if joueur[0]['pos'][0] < 0 or joueur[1]['pos'][0] < 0 or joueur[0]['pos'][1] < 0  or joueur[1]['pos'][1] < 0:
            raise QuoridorError('Position invalide pour un joueur')
        self.murs = murs
        self.jeu = jeu
        self.joueurs = joueur
    
    def __str__(self):
        nom = [self.jeu['joueurs'][0]['nom'], self.jeu['joueurs'][1]['nom']]
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
        damier = f'Légende: 1={nom[0]}, 2={nom[1]}' + '\n' + '   -----------------------------------'
        for li in reversed(table):
            if nl == 1:
                damier += '\n' + f'{nl} |' + ''.join((li)) + '|'
            else:
                damier += '\n' + f'{nl} |' + ''.join((li)) + '|' + '\n' + ''.join(let[nl - 1])
            nl -= 1
        damier += '\n' + '--|-----------------------------------'
        damier += '\n' + '  | 1   2   3   4   5   6   7   8   9'
        return damier

    def déplacer_jeton(self, joueur, position):
        # Le numero du joeur est autre que 1 ou 2.
        if joueur not in [1, 2]:
            raise QuoridorError('le numéro du joueur est autre que 1 ou 2.')
        # La position n'est pas entre 1 et 10 en x et y.
        if position[0] not in range(1, 10) or position[0] not in range(1, 10):
            raise QuoridorError('la position est invalide (en dehors du damier).')
        # Crée un graphe avec networkx et verifie si la position est disponible
        graphe = construire_graphe([joueur['pos'] for joueur in self.joueurs], self.murs['horizontaux'], self.murs['verticaux'])
        if position not in list(graphe.successors(((tuple(self.joueurs[joueur - 1]['pos']))))):
            raise QuoridorError("la position est invalide pour l'état actuel du jeu.")

    
    def état_partie(self):
        return self.jeu

    #def jouer_coup(self, joueur):

    #def partie_terminée(self):

  
    #def placer_mur(self, joueur: int, position: tuple, orientation: str):

def construire_graphe(joueurs, murs_horizontaux, murs_verticaux):
    """
    Crée le graphe des déplacements admissibles pour les joueurs.

    :param joueurs: une liste des positions (x,y) des joueurs.
    :param murs_horizontaux: une liste des positions (x,y) des murs horizontaux.
    :param murs_verticaux: une liste des positions (x,y) des murs verticaux.
    :returns: le graphe bidirectionnel (en networkX) des déplacements admissibles.
    """
    graphe = nx.DiGraph()

    # pour chaque colonne du damier
    for x in range(1, 10):
        # pour chaque ligne du damier
        for y in range(1, 10):
            # ajouter les arcs de tous les déplacements possibles pour cette tuile
            if x > 1:
                graphe.add_edge((x, y), (x-1, y))
            if x < 9:
                graphe.add_edge((x, y), (x+1, y))
            if y > 1:
                graphe.add_edge((x, y), (x, y-1))
            if y < 9:
                graphe.add_edge((x, y), (x, y+1))

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


###Programme###

test = Quoridor(({"nom": "idul", "murs": 7, "pos": [5, 6]},
        {"nom": "automate", "murs": 3, "pos": [5, 7]}),{
        "horizontaux": [[4, 4], [2, 6], [3, 8], [5, 8], [7, 8]],
        "verticaux": [[6, 2], [4, 4], [2, 5], [7, 5], [7, 7]]
    })
test.déplacer_jeton(2, (5,5))
print(test)
