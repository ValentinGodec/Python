
import sys, os
sys.path.append(os.path.realpath(os.path.dirname(__file__)+"/.."))

from src import QuadTree, TkQuadTree

def test_single():
    filename = "files/quadtree_easy.txt"
    q = QuadTree.fromFile(filename)
    assert q.depth == 1

def test_sample():
    filename = "files/quadtree.txt"
    q = QuadTree.fromFile(filename)
    assert q.depth == 4

def test_boolean_values():
    # Teste le cas où la liste contient uniquement des valeurs booléennes
    boolean_list = [True, False, False, True]
    q = QuadTree.fromList(boolean_list)
    assert q.depth == 1

def test_lists():
    # Teste le cas où la liste contient des sous-listes
    nested_list = [[[1, 0, 0, 1], [0, 1, 1, 1], 0, 0], 0, [0, 0, 1, 1], [1, 0, 0, 0]]
    q = QuadTree.fromList(nested_list)
    assert q.depth == 3

def test_mixed_types():
    # Teste le cas où la liste contient des types de données mélangés
    mixed_list = ["a", [True, False, True, True], 3, [0, 1, 1, 0]]
    q = QuadTree.fromList(mixed_list)
    assert q.depth == 2






