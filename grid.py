symboles = [' ', 'O', 'X']
VIDE = 0
JOUEUR1 = 1
JOUEUR2 = 2
NB_CELLES = 9

class grid:
    def __init__(self):
        self.cellules = [VIDE] * NB_CELLES

    def jouer(self, joueur, num_cellule):
        assert 0 <= num_cellule < NB_CELLES
        assert self.cellules[num_cellule] == VIDE
        self.cellules[num_cellule] = joueur

    def afficher(self):
        print("-------------")
        for i in range(3):
            print("|", symboles[self.cellules[i * 3]], "|", symboles[self.cellules[i * 3 + 1]], "|", symboles[self.cellules[i * 3 + 2]], "|")
            print("-------------")

    def afficher_chaine(self):
        resultat = "-------------\n"
        for i in range(3):
            resultat += f"| {symboles[self.cellules[i * 3]]} | {symboles[self.cellules[i * 3 + 1]]} | {symboles[self.cellules[i * 3 + 2]]} |\n"
            resultat += "-------------\n"
        return resultat

    def gagnant(self, joueur):
        assert joueur in (JOUEUR1, JOUEUR2)
        for y in range(3):
            if self.cellules[y * 3] == joueur and self.cellules[y * 3 + 1] == joueur and self.cellules[y * 3 + 2] == joueur:
                return True
        for x in range(3):
            if self.cellules[x] == joueur and self.cellules[3 + x] == joueur and self.cellules[6 + x] == joueur:
                return True
        if self.cellules[0] == joueur and self.cellules[4] == joueur and self.cellules[8] == joueur:
            return True
        if self.cellules[2] == joueur and self.cellules[4] == joueur and self.cellules[6] == joueur:
            return True
        return False

    def partie_terminee(self):
        if self.gagnant(JOUEUR1):
            return JOUEUR1
        if self.gagnant(JOUEUR2):
            return JOUEUR2
        if all(cellule != VIDE for cellule in self.cellules):
            return 0
        return -1