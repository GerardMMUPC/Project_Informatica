import Node
from Segment import Segment

class Graph():
    def __init__(self):
        self.nodes = []
        self.segments = []

    def AddNode (self, n): # self = g
        # Check condition: Node in graph
            for Node in self.nodes:
                if Node.value == n.value:
                    return False
            else:
                self.nodes.append(n)
                return True

    def AddSegment (self, nameOriginNode, nameDestinationNode):
        foundOriginNode = False
        foundDestinationNode = False

        origin_node = 0
        destination_node = 0

        for Node in self.nodes:

            if Node.name == nameOriginNode:
                foundOriginNode = True
                origin_node = Node

            if Node.name == nameDestinationNode:
                foundDestinationNode = True
                destination_node = Node

        if not foundOriginNode or not foundDestinationNode:
            return False


        seg = Segment(
            f"{origin_node.name}-{destination_node.name}",
            origin_node.name,
            destination_node.name
        )

        self.segments.append(seg)


        origin_node.AddNeighbor(destination_node)

        return True

    def GetClosest(self, x, y):
        for Node in self.nodes:
            min_cost = min()

