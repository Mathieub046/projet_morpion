# grid.py

# Définir les symboles des joueurs et les constantes
symbols = [' ', 'O', 'X']
EMPTY = 0
J1 = 1
J2 = 2
NB_CELLS = 9

class grid:
    def __init__(self):
        # Initialiser la grille avec des cases vides
        self.cells = [EMPTY] * NB_CELLS
    
    def reset(self):
        """Réinitialise la grille à son état initial"""
        self.cells = [EMPTY] * NB_CELLS

    def play(self, player, cellNum):
        """Permet à un joueur de jouer son coup"""
        assert(0 <= cellNum < NB_CELLS)
        assert(self.cells[cellNum] == EMPTY)
        self.cells[cellNum] = player

    def display(self):
        """Affiche la grille actuelle"""
        print(" -------------")
        for i in range(3):
            print(" | ", end="")
            for j in range(3):
                print(f"{symbols[self.cells[i * 3 + j]]} | ", end="")
            print("\n -------------")

    def winner(self, player):
        """Vérifie si un joueur a gagné"""
        assert(player == J1 or player == J2)
        
        # Vérification des lignes
        for y in range(3):
            if self.cells[y * 3] == player and self.cells[y * 3 + 1] == player and self.cells[y * 3 + 2] == player:
                return True
        
        # Vérification des colonnes
        for x in range(3):
            if self.cells[x] == player and self.cells[3 + x] == player and self.cells[6 + x] == player:
                return True
        
        # Vérification des diagonales
        if self.cells[0] == player and self.cells[4] == player and self.cells[8] == player:
            return True
        if self.cells[2] == player and self.cells[4] == player and self.cells[6] == player:
            return True
        
        return False

    def gameOver(self):
        """Vérifie si le jeu est terminé"""
        if self.winner(J1):
            return J1  # Joueur 1 a gagné
        if self.winner(J2):
            return J2  # Joueur 2 a gagné
        for i in range(NB_CELLS):
            if self.cells[i] == EMPTY:
                return -1  # Partie en cours
        return 0  # Match nul
