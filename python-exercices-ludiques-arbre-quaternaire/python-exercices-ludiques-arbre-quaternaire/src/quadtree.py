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

    # Définir les coordonnées du rectangle principal
        x1, y1, x2, y2 = 0, 0, 250, 250

        # Appeler la fonction pour dessiner le QuadTree
        self.paint_node(monquadtree, x1, y1, x2, y2)

    def paint_node(self, quadtree, x1, y1, x2, y2):
        """Dessine un noeud du QuadTree"""
        if isinstance(quadtree, QuadTree):
            mid_x = (x1 + x2) // 2
            mid_y = (y1 + y2) // 2

            # Dessine un rectangle représentant le noeud
            self.canvas.create_rectangle(x1, y1, x2, y2, outline="black")

            # Appelle récursivement la fonction pour chaque sous-noeud
            self.paint_node(quadtree.hg, x1, y1, mid_x, mid_y)
            self.paint_node(quadtree.hd, mid_x, y1, x2, mid_y)
            self.paint_node(quadtree.bd, mid_x, mid_y, x2, y2)
            self.paint_node(quadtree.bg, x1, mid_y, mid_x, y2)
        else:
            if quadtree:
                self.canvas.create_rectangle(x1, y1, x2, y2, fill="grey")
            else:
                self.canvas.create_rectangle(x1, y1, x2, y2, fill="white")

    
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
