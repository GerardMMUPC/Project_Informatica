# Necessitem els nodes i els segments
from Node import Node # Importem class Node
from Segment import Segment # Importem class Segment

class Graph():
    def __init__(self):
        self.nodes = [] # Llista per guardar nodes
        self.segments = [] # Llista per guardar segments

    def AddNode (self, n): # self = g
        # Check condition: Node in graph
            for node in self.nodes:
                if node.value == n.value: # Si trobem el node a n
                    return False
            else: # Duplicat no trobat
                self.nodes.append(n)
                return True # Node afegit

    def AddSegment (self, nameOriginNode, nameDestinationNode):
        foundOriginNode = False # No hem trobat els nodes encara
        foundDestinationNode = False

        origin_node = 0
        destination_node = 0

        # Recorregut de tots els nodes del gràfic:
        for node in self.nodes:
            # Trobem el node d'origen
            if node.name == nameOriginNode:
                foundOriginNode = True
                origin_node = node # Guardem node d'origen.
            # Trobem el node de destinació
            if node.name == nameDestinationNode:
                foundDestinationNode = True
                destination_node = node #Guardem node destinació.
        # Si no els trobem:
        if not foundOriginNode or not foundDestinationNode:
            return False

        # Si trobem ambdós, creem un segment entre ells.
        segment = Segment(
            segmentname = f"{origin_node.name}-{destination_node.name}",
            origin = float(origin_node.name),
            destination = float(destination_node.name),
        )

        self.segments.append(segment) #Afegim segment a llista de segments

        #Afegim node destinació a la llista de node d'origen
        origin_node.add_neighbor(destination_node)

        return True # Segment afegit