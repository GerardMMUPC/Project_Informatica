from Path import Path
from Node import Node
from Graph import Graph, AddNode, AddSegment


def TestPath():
    # Create some nodes
    n1 = Node("A", 0, 0)
    n2 = Node("B", 3, 4)
    n3 = Node("C", 6, 0)

    # Test basic path functionality
    path = Path()
    path.AddNodeToPath(n1)
    path.AddNodeToPath(n2)
    path.AddNodeToPath(n3)

    print("Testing ContainsNode:")
    print(f"Contains A: {path.ContainsNode(n1)} (Expected: True)")
    print(f"Contains B: {path.ContainsNode(n2)} (Expected: True)")
    print(f"Contains C: {path.ContainsNode(n3)} (Expected: True)")
    print(f"Contains D: {path.ContainsNode(Node('D', 0, 0))} (Expected: False)")

    print("\nTesting CostToNode:")
    print(f"Cost to A: {path.CostToNode(n1):.2f} (Expected: 0.00)")
    print(f"Cost to B: {path.CostToNode(n2):.2f} (Expected: 5.00)")
    print(f"Cost to C: {path.CostToNode(n3):.2f} (Expected: 9.00)")

    # Test plotting
    print("\nCreating graph for plotting test...")
    g = Graph()
    AddNode(g, n1)
    AddNode(g, n2)
    AddNode(g, n3)
    AddSegment(g, "A", "B")
    AddSegment(g, "B", "C")

    print("Plotting path...")
    path.PlotPath(g)


if __name__ == "__main__":
    TestPath()