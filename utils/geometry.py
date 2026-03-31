import numpy as np

def is_triangle(p1, p2, p3, tol=3):
    d1 = np.linalg.norm(p1-p2)
    d2 = np.linalg.norm(p2-p3)
    d3 = np.linalg.norm(p1-p3)
    return abs(d1-d2)<tol and abs(d2-d3)<tol

def find_triangles(players):
    names = list(players.keys())
    triangles = []

    for i in range(len(names)):
        for j in range(i+1, len(names)):
            for k in range(j+1, len(names)):
                if is_triangle(players[names[i]], players[names[j]], players[names[k]]):
                    triangles.append((names[i], names[j], names[k]))
    
    return triangles