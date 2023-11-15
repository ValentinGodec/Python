from __future__ import annotations
import tkinter as tk

class QuadTree:
    NB_NODES : int = 4
    def __init__(self, hg: bool | QuadTree, hd: bool | QuadTree, bd: bool | QuadTree,bg: bool | QuadTree):
        """
        hg: Haut gauche du bloc
        hd: Haut droite du bloc
        bd: Bas droite du bloc
        bg: Bas Gauche du bloc
        """
        self.hg = hg
        self.hd = hd
        self.bd = bd
        self.bg = bg
        pass

    @property
    def depth(self) -> int:
        """Recursion depth of the quadtree"""
        """
        Renvoie le niveau max de profondeur du quadtree
        """
        children = [self.hg, self.hd, self.bd, self.bg]
        depths = []
        for child in children:
            if not isinstance(child, QuadTree):
                return 0
            else:
                depths.append(child.depth)
        return 1 + max(depths)

    @staticmethod
    def fromFile(filename: str) -> QuadTree:
        """ 
        Ouvre le fichier filename, contenant une liste
        """
        file = open(filename, "r")
        # eval permet de convertir la chaîne en une liste
        data = eval(file.read())  
        file.close()
        return QuadTree.fromList(data)
        
    @staticmethod
    def fromList(data: list) -> QuadTree:
        """ 
        Génère un Quadtree à partir d'une liste
        """
        # Convertit les valeurs booléennes ou de sous liste
        data_nodes = []
        for child in data:
            if isinstance(child, list):
                data_nodes.append(QuadTree.fromList(child))
            else:
                data_nodes.append(bool(child))
        hg, hd, bd, bg = data_nodes

        # Evite de retourner la reference de l'objet
        quadtree_values = [hg, hd, bd, bg]
        for i in range(len(quadtree_values)):
            if not isinstance(quadtree_values[i], QuadTree):
                quadtree_values[i] = QuadTree(quadtree_values[i], quadtree_values[i], quadtree_values[i], quadtree_values[i])
            else:
                quadtree_values[i] = quadtree_values[i]
        hg, hd, bd, bg = quadtree_values

        # Retourne l'arbre
        return QuadTree(hg, hd, bd, bg)
    
    def paint(self, indent=0):
        """ Textual representation of the QuadTree"""
        """
        Génère textuellement le Quadtree dans le terminal
        """
        # Initialise l'indentation
        print("  " * indent, end="")
        # Affiche True, False, ou Node
        if isinstance(self.hg, QuadTree):
            print("Node")
        else:
            print(self.hg)

        # Appelle de la méthode paint pour chaque quart
        if isinstance(self.hg, QuadTree):
            self.hg.paint(indent + 1)
            self.hd.paint(indent + 1)
            self.bd.paint(indent + 1)
            self.bg.paint(indent + 1)

class TkQuadTree:
    def __init__(self, master, quadtree):
        self.quadtree = quadtree
        self.canvas = tk.Canvas(master)
        self.canvas.pack()

    def paint(self, filename):
        """
        Représentation graphique du Quadtree avec Tkinter
        """
        monquadtree = QuadTree.fromFile(filename)
        # Effacer le contenu précédent du canevas
        self.canvas.delete("all")  
        
        
        
    
FILENAME = "files/quadtree.txt"
quadtree = QuadTree.fromFile(FILENAME)
quadtree.paint()

SIZE=512
root = tk.Tk()
root.title("Quadtree")
root.geometry(str(SIZE) + "x" + str(SIZE))
tk_quadtree = TkQuadTree(root, quadtree)
# Affichage graphique du Quadtree de FILENAME
tk_quadtree.paint(FILENAME)
root.mainloop()
