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
            #Vérification de la position des murs
            for l, mh in enumerate(murs['horizontaux']):
                muh = murs['horizontaux'].copy()
                del muh[l]
                for mhp in muh:
                    if mh[1] == mhp[1] and (mh[0] == mhp[0] or mh[0] == mhp[0] - 1 or mh[0] == mhp[0] + 1):
                        raise QuoridorError('Position de murs invalide')
                if mh[0] < 1 or mh[0] > 8 or mh[1] < 2 or mh[1] > 9:
                    raise QuoridorError('Position de murs invalide')
            for o, mv in enumerate(murs['verticaux']):
                muv = murs['verticaux'].copy()
                del muv[o]
                for mvp in muv:
                    if mv[0] == mvp[0] and (mv[1] == mvp[1] or mv[1] == mvp[1] - 1 or mv[1] == mvp[1] + 1):
                        raise QuoridorError('Position de murs invalide')
                if mv[0] < 2 or mv[0] > 9 or mv[1] < 1 or mv[1] > 8:
                    raise QuoridorError('Position de murs invalide')
        
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

    #def déplacer_jeton(self, joueur, position):
       
    def état_partie(self):
        return self.jeu

    #def jouer_coup(self, joueur):

    #def partie_terminée(self):
   
    def placer_mur(self, njoueur, position, orientation):
        #Vérifie le numéro du joueur
        if njoueur != 1 and njoueur != 2:
            raise QuoridorError('le numéro du joueur est autre que 1 ou 2')
        #Identifie le joueur
        joueur = self.joueurs[njoueur - 1]
        #Vérifie qu'il reste des murs à placer pour le joueur désigné
        if joueur['murs'] == 0:
            raise QuoridorError('le joueur a déjà placé tous ses murs')
        #Vérifie que la place est libre pour le mur
        for m in self.murs[orientation]:
            if m[0] == position[0] and m[1] == position[1]:
                raise QuoridorError('un mur occupe déjà cette position')
            if orientation == 'horizontaux':
                if m[1] == position[1] and (m[0] == position[0] or m[0] == position[0] - 1 or m[0] == position[0] + 1):
                    raise QuoridorError('un mur occupe déjà cette position')
            if orientation == 'verticaux':
                if m[0] == position[0] and (m[1] == position[1] or m[1] == position[1] - 1 or m[1] == position[1] + 1):
                    raise QuoridorError('un mur occupe déjà cette position')
        #Vérifie que la position est valide
        if orientation == 'horizontaux':
            if position[0] < 1 or position[0] > 8 or position[1] < 2 or position[1] > 9:
                raise QuoridorError('la position est invalide pour cette orientation')
        if orientation == 'verticaux':
            if position[0] < 2 or position[0] > 9 or position[1] < 1 or position[1] > 8:
                raise QuoridorError('la position est invalide pour cette orientation')
        #Place le mur et enlève un mur au joueur qui place le mur
        joueur['murs'] -= 1
        self.jeu['murs'][orientation].append(position)

test = Quoridor(({"nom": "idul", "murs": 7, "pos": [5, 6]},
        {"nom": "automate", "murs": 3, "pos": [5, 7]}),{
        "horizontaux": [[4, 4], [2, 6], [3, 8], [5, 8], [7, 8]],
        "verticaux": [[6, 2], [4, 4], [2, 5], [7, 5], [7, 7]]
    })
print(test)
Quoridor.placer_mur(test, 2, (3, 7), 'horizontaux')
print(test)
print(Quoridor.état_partie(test))