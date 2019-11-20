class QuoridorError(Exception):
    def __init__(self, message):
        self.message = message
    def __str__(self):
        return str(self.message)



class Quoridor:
    def __init__(self, joueurs, murs=None):
        if iter(joueurs) is False:
            raise QuoridorError("joueurs n'est pas itérable")
        if len(joueurs) != 2:
            raise QuoridorError("L'itérable joueurs ne contient pas deux éléments")
        if isinstance(joueurs[0], str):
            joueur1 = {'nom': joueurs[0], 'murs': 10, 'pos': (5,1)}
        if isinstance(joueurs[1], str):
            joueur2 = {'nom': joueurs[1], 'murs': 10, 'pos': (5,9)}
        if isinstance(joueurs[0], dict):
            joueur1 = joueurs[0]
        if isinstance(joueurs[1], dict):
            joueur2 = joueurs[1]
        if murs == None:
            jeu = {'joueurs': [joueur1, joueur2], 'murs': {'horizontaux':[], 'verticaux': []}}
        if murs != None:
            jeu = {'joueurs': [joueur1, joueur2], 'murs': murs}
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