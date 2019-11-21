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
        
        #Création des dictionnaire joueur
        joueur = []
        for jou in joueurs:
            if isinstance(jou, str):
                joueur.append({'nom': joueur, 'murs': 10, 'pos': (5,1)})
            if isinstance(jou, dict):
                joueur.append(jou)
        
        #Vérification du nombre de murs
        if joueurs[0]['murs'] > 10 or joueurs[1]['murs'] > 10 or joueurs[0]['murs'] < 0 or joueurs[1]['murs'] < 0:
            raise QuoridorError('Nombre de murs invalides')
        if murs == None:
            jeu = {'joueurs': [joueurs[0], joueurs[1]], 'murs': {'horizontaux':[], 'verticaux': []}}
        if murs != None:
            jeu = {'joueurs': [joueurs[0], joueurs[1]], 'murs': murs}
            nmurs = len(murs['horizontaux']) + len(murs['verticaux']) + joueurs[0]['murs'] + joueurs[1]['murs']
            if nmurs != 20:
                raise QuoridorError('Nombre de murs invalide')
        
        #Vérification de la position des joueurs
        if joueurs[0]['pos'][0] > 9 or joueurs[1]['pos'][0] > 9 or joueurs[0]['pos'][1] > 9 or joueurs[1]['pos'][1] > 9:
            raise QuoridorError('Position invalide pour un joueur')
        if joueurs[0]['pos'][0] < 0 or joueurs[1]['pos'][0] < 0 or joueurs[0]['pos'][1] < 0  or joueurs[1]['pos'][1] < 0:
            raise QuoridorError('Position invalide pour un joueur')
        self.jeu = jeu
    
    def __str__(self):
        jeu = self.jeu
        nom = [jeu['joueurs'][0]['nom'], jeu['joueurs'][1]['nom']]
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
        for joueur in jeu['joueurs']:
            table[joueur['pos'][1] - 1][joueur['pos'][0] - 1][1] = str(nj)
            nj += 1
        for mur in jeu['murs']['horizontaux']:
            let[mur[1] - 1][mur[0]] = '----'
            let[mur[1] - 1][mur[0] + 1] = '--- '
            if mur[0] == 8:
                let[mur[1] - 1][mur[0]] = '----'
                let[mur[1] - 1][mur[0] + 1] = '---|'
        for m in jeu['murs']['verticaux']:
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
       
    #def état_partie(self):

    #def jouer_coup(self, joueur):

    #def partie_terminée(self):
   
    #def placer_mur(self, joueur: int, position: tuple, orientation: str):

test = Quoridor(({"nom": "idul", "murs": 7, "pos": [5, 6]},
        {"nom": "automate", "murs": 3, "pos": [5, 7]}),{
        "horizontaux": [[4, 4], [2, 6], [3, 8], [5, 8], [7, 8]],
        "verticaux": [[6, 2], [4, 4], [2, 5], [7, 5], [7, 7]]
    })
print(test)