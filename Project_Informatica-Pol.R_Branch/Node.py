import math

class Node:
    def __init__(self, name, x, y, neighbors=None):
        self.name = str(name)
        self.x = float(x)
        self.y = float(y)
        self.neighbors = neighbors if neighbors else []


def AddNeighbor(n1, n2):
    if n2 not in n1.neighbors:
        n1.neighbors.append(n2)
        return True
    return False


def Distance(n1, n2):
    return math.sqrt((n2.x - n1.x) ** 2 + (n2.y - n1.y) ** 2)

