import matplotlib.pyplot as plt
from Node import Node, Distance, AddNeighbor
from Segment import Segment


class Graph:
    def __init__(self):
        self.nodes = []
        self.segments = []


def Añadir_nodo(g, n):
    for node in g.nodes:
        if node.name == n.name:
            return False
    g.nodes.append(n)
    return True


def Añadir_segmento(g, name_origin, name_destination):
    origin_node = None
    destination_node = None

    for node in g.nodes:
        if node.name == name_origin:
            origin_node = node
        if node.name == name_destination:
            destination_node = node

    if origin_node is None or destination_node is None:
        return False

    seg = Segment(f"{origin_node.name}-{destination_node.name}", origin_node, destination_node)
    g.segments.append(seg)

    AddNeighbor(origin_node, destination_node)
    AddNeighbor(destination_node, origin_node)

    return True


def Encontrar_mas_cercano(g, x, y):
    if not g.nodes:
        return None

    closest_node = min(g.nodes, key=lambda node: ((node.x - x) ** 2 + (node.y - y) ** 2) ** 0.5)
    return closest_node


def Plot(graph, highlight_path=None, highlight_nodes=None, title="Graph", airport_nodes=None):
    fig, ax = plt.subplots(figsize=(10, 8))

    for segment in graph.segments:
        edge_color = 'gray'
        edge_alpha = 0.5
        edge_width = 1

        if highlight_nodes and segment.origin in highlight_nodes and segment.destination in highlight_nodes:
            edge_color = 'green'
            edge_alpha = 0.8
            edge_width = 1.5

        ax.annotate('',
                    xy=(segment.destination.x, segment.destination.y),
                    xytext=(segment.origin.x, segment.origin.y),
                    arrowprops=dict(
                        arrowstyle='->',
                        color=edge_color,
                        lw=edge_width,
                        alpha=edge_alpha,
                        shrinkA=10,
                        shrinkB=10
                    ))

    for node in graph.nodes:
        # Color de nodos
        if highlight_nodes and node in highlight_nodes:
            if node == highlight_nodes[0]:
                color = 'green'
                size = 200
            else:
                color = 'green'
                size = 150
        elif airport_nodes and node in airport_nodes:
            color = 'blue'  # Color diferente para aeropuertos
            size = 150
        else:
            color = 'lightgray'
            size = 100

        ax.scatter(node.x, node.y, c=color, s=size, zorder=3)
        ax.text(node.x, node.y, f" {node.name}", fontsize=10, zorder=4)

    ax.set_title(title)
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    return fig


def PlotNodo(g, nameOrigin, title="Graph view from node"):
    origin_node = None
    for node in g.nodes:
        if node.name == nameOrigin:
            origin_node = node
            break

    if origin_node is None:
        return None

    fig, ax = plt.subplots(figsize=(8, 6))

    for segment in g.segments:
        x_values = [segment.origin.x, segment.destination.x]
        y_values = [segment.origin.y, segment.destination.y]
        ax.plot(x_values, y_values, 'gray', linewidth=1)

    for neighbor in origin_node.neighbors:
        ax.scatter(neighbor.x, neighbor.y, color='green', s=80)
        ax.plot([origin_node.x, neighbor.x], [origin_node.y, neighbor.y], 'r-', linewidth=2)

        mid_x = (origin_node.x + neighbor.x) / 2
        mid_y = (origin_node.y + neighbor.y) / 2

        ax.text(mid_x, mid_y, f"{Distance(origin_node, neighbor):.2f}", fontsize=10, ha='center', color='red')

    for node in g.nodes:
        if node not in origin_node.neighbors and node != origin_node:
            ax.scatter(node.x, node.y, color='gray', s=50)

    for node in g.nodes:
        ax.text(node.x, node.y, f" {node.name}", fontsize=12, verticalalignment='bottom')

    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_title(f"{title} {nameOrigin}")
    ax.grid(True)
    fig.tight_layout()
    return fig


def Grafico_fichero(filename, seg_filename=None, aer_filename=None):
    G = Graph()
    airport_nodes = set()
    parsing_segments = False
    id_to_node = {}

    try:
        with open(filename, 'r') as fichero:
            for line in fichero:
                line = line.strip()
                if not line or line.startswith("#"):
                    if line.strip().lower() == "# segments":
                        parsing_segments = True
                    continue

                elements = line.split()

                if parsing_segments:
                    # Parse segments directly from main file
                    if len(elements) >= 2:
                        origin = elements[0]
                        dest = elements[1]
                        Añadir_segmento(G, origin, dest)
                    continue

                # Parse nodes
                if len(elements) == 4:  # Formato: número nombre lat lon
                    try:
                        number = int(elements[0])
                        name = elements[1]
                        lat = float(elements[2])
                        lon = float(elements[3])

                        node = Node(name, lon, lat)
                        node.number = number
                        Añadir_nodo(G, node)
                        id_to_node[number] = node
                    except ValueError as e:
                        print(f"Saltando línea inválida: {line} - {e}")

                elif len(elements) == 3:  # Formato alternativo: nombre x y
                    try:
                        name = elements[0]
                        x = float(elements[1])
                        y = float(elements[2])

                        node = Node(name, x, y)
                        Añadir_nodo(G, node)
                    except ValueError as e:
                        print(f"Saltando línea inválida: {line} - {e}")

    except Exception as e:
        print(f"Error leyendo el fichero principal: {e}")
        return None

    # Cargar segmentos desde archivo separado si se proporciona
    if seg_filename:
        try:
            with open(seg_filename, 'r') as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith("#"):
                        continue

                    elements = line.split()
                    if len(elements) == 3:  # Formato: origin dest distance
                        try:
                            origin = int(elements[0])
                            dest = int(elements[1])

                            if origin in id_to_node and dest in id_to_node:
                                Añadir_segmento(G, id_to_node[origin].name, id_to_node[dest].name)
                        except ValueError as e:
                            print(f"Saltando segmento inválido: {line} - {e}")
        except Exception as e:
            print(f"Error leyendo fichero de segmentos: {e}")

    # Cargar aeropuertos si se proporciona
    if aer_filename:
        try:
            with open(aer_filename, 'r') as f:
                current_airport = None
                for line in f:
                    line = line.strip()
                    if not line:
                        continue

                    if not line.endswith(('.D', '.A')):  # Es nombre de aeropuerto
                        current_airport = line
                    else:  # Es punto de navegación (SID, STAR...)
                        for node in G.nodes:
                            if node.name == line:
                                airport_nodes.add(node)
                                break
        except Exception as e:
            print(f"Error leyendo fichero de aeropuertos: {e}")

    G.airport_nodes = airport_nodes
    return G


def Encontrar_camino_mas_corto(g, origin, destination):

    from Path import Path

    current_paths = [Path([origin], 0)]
    g.shortest_path = None  # Clear any previous path

    while current_paths:
        # Buscamos el camino con el coste minimo
        current_paths.sort(key=lambda p: p.cost + Distance(p.nodes[-1], destination))
        best_path = current_paths.pop(0)
        last_node = best_path.nodes[-1]

        # Comprovamos si se ha llegado al destino
        if last_node == destination:
            g.shortest_path = best_path
            return best_path

        # Explorar Vecinos
        for neighbor in last_node.neighbors:
            if not best_path.contains_node(neighbor):
                new_path = best_path.copy()
                distance = Distance(last_node, neighbor)
                new_path.add_node(neighbor, distance)
                current_paths.append(new_path)

    # No se encuentra un camino
    g.shortest_path = None
    return None


def Encontrar_nodos_alcanzables(g, start_node):
    visited = set()
    stack = [start_node]

    while stack:
        current_node = stack.pop()
        if current_node in visited:
            continue

        visited.add(current_node)

        for segment in g.segments:
            if segment.origin == current_node:
                if segment.destination not in visited:
                    stack.append(segment.destination)

    return list(visited)
def Plot_ratón(graph, title=""):
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(6, 5))
    ax.set_title(title)
    ax.grid(True)

    node_artist_map = {}

    # Dibujar segmentos
    for seg in graph.segments:
        ax.plot([seg.origin.x, seg.destination.x],
                [seg.origin.y, seg.destination.y],
                'gray', linewidth=1)

    # Dibujar nodos
    for node in graph.nodes:
        sc = ax.scatter(node.x, node.y, color='black', picker=True)
        ax.text(node.x, node.y, f" {node.name}", fontsize=9)
        node_artist_map[sc] = node

    def on_pick(event):
        artist = event.artist
        if artist in node_artist_map:
            selected_node = node_artist_map[artist]
            neighbors = [
                seg.destination for seg in graph.segments if seg.origin == selected_node
            ] + [
                seg.origin for seg in graph.segments if seg.destination == selected_node
            ]

            ax.clear()
            ax.set_title(f"Vecinos de {selected_node.name}")
            ax.grid(True)

            # Redibujar segmentos resaltados
            for seg in graph.segments:
                is_connected = (
                    (seg.origin == selected_node and seg.destination in neighbors) or
                    (seg.destination == selected_node and seg.origin in neighbors)
                )
                color = 'red' if is_connected else 'gray'
                linewidth = 2 if is_connected else 1

                ax.plot([seg.origin.x, seg.destination.x],
                        [seg.origin.y, seg.destination.y],
                        color=color, linewidth=linewidth)

            # Redibujar nodos
            for node in graph.nodes:
                if node == selected_node:
                    color = 'red'
                elif node in neighbors:
                    color = 'green'
                else:
                    color = 'black'
                ax.scatter(node.x, node.y, color=color, picker=True)
                ax.text(node.x, node.y, f" {node.name}", fontsize=9)

            fig.canvas.draw()

    fig.canvas.mpl_connect('pick_event', on_pick)
    return fig