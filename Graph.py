import matplotlib.pyplot as plt
from Node import *
from Segment import Segment

class Graph:

    def __init__(self):
        self.nodes = []
        self.segments = []

    def AddNode(self, n):

        for node in self.nodes:
            if node.name == n.name:
                return False

        self.nodes.append(n)
        return True

    def AddSegment(self, name_origin, name_destination):
        origin_node = None
        destination_node = None

        for node in self.nodes:

            if node.name == name_origin:
                origin_node = node

            if node.name == name_destination:
                destination_node = node

        if origin_node is None or destination_node is None:
            return False

        seg = Segment(f"{origin_node.name}-{destination_node.name}", origin_node, destination_node)

        self.segments.append(seg)

        origin_node.AddNeighbor(destination_node)

        return True

    def GetClosest(self, x, y):
        if not self.nodes:
            return None

        closest_node = min(self.nodes, key=lambda node: ((node.x - x) ** 2 + (node.y - y) ** 2) ** 0.5)
        return closest_node

    def Plot(self, title="Graph of nodes"):
        plt.figure(figsize=(8, 6))

        # Segments
        for segment in self.segments:
            x_values = [segment.origin.x, segment.destination.x]
            y_values = [segment.origin.y, segment.destination.y]
            plt.plot(x_values, y_values, 'k-', linewidth=1)

            # Punts Migs
            mid_x = (segment.origin.x + segment.destination.x) / 2
            mid_y = (segment.origin.y + segment.destination.y) / 2
            plt.text(mid_x, mid_y, f"{segment.cost:.2f}", fontsize=10, ha='center', color='red')

        # Nodes
        for node in self.nodes:
            plt.scatter(node.x, node.y, color='black', s=50)
            plt.text(node.x, node.y, f" {node.name}", fontsize=12, verticalalignment='bottom')

        plt.xlabel("X")
        plt.ylabel("Y")
        plt.title(title)
        plt.grid(True)
        plt.show()

    def PlotNode(self, nameOrigin, title="Graph view from node"):
        origin_node = None
        for node in self.nodes:
            if node.name == nameOrigin:
                origin_node = node
                break

        if origin_node is None:
            return False

        plt.figure(figsize=(8, 6))

        # Tots els segments
        for segment in self.segments:
            x_values = [segment.origin.x, segment.destination.x]
            y_values = [segment.origin.y, segment.destination.y]
            plt.plot(x_values, y_values, 'gray', linewidth=1)

        # Neighbors en green i segments en red
        for neighbor in origin_node.neighbors:
            plt.scatter(neighbor.x, neighbor.y, color='green', s=80)
            plt.plot([origin_node.x, neighbor.x], [origin_node.y, neighbor.y], 'r-', linewidth=2)

            # Punt mig
            mid_x = (origin_node.x + neighbor.x) / 2
            mid_y = (origin_node.y + neighbor.y) / 2

            # Corrected Distance function call
            plt.text(mid_x, mid_y, f"{origin_node.Distance(origin_node, neighbor):.2f}", fontsize=10, ha='center', color='red')

        # Origin node in blue
        plt.scatter(origin_node.x, origin_node.y, color='blue', s=100)

        # Other nodes in gray
        for node in self.nodes:
            if node not in origin_node.neighbors and node != origin_node:
                plt.scatter(node.x, node.y, color='gray', s=50)

        # Annotate node names
        for node in self.nodes:
            plt.text(node.x, node.y, f" {node.name}", fontsize=12, verticalalignment='bottom')

        plt.xlabel("X")
        plt.ylabel("Y")
        plt.title(f"{title} {nameOrigin}")  # Dynamic title from variable
        plt.grid(True)
        plt.show()

        return True
