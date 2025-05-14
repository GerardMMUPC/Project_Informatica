from tkinter import *
from tkinter import ttk
from tkinter import filedialog, messagebox
from Graph import FileGraph, Plot, PlotNode, AddNode, AddSegment, Graph, find_shortest_path, find_reachable_nodes
from Node import Node, Distance
import matplotlib.pyplot as plt

window = Tk()
window.title("Editor de Grafos")
window.configure(bg='#f0f0f0')

frame = ttk.Frame(window, padding=10)
frame.grid(row=0, column=0, sticky="nsew")

graph = None
custom_graph = Graph()

# Funciones de los botones:

def Mostrar_Grafo_Ejemplo():
    from test_graph import CreateGraph_1
    G1 = CreateGraph_1()
    Plot(G1, title="Gráfico con nodos y segmentos")

def Mostrar_Grafo_Inventado():
    from test_graph import CreateGraph_2
    G2 = CreateGraph_2()
    Plot(G2, title="Mapa de rutas aéreas de EE. UU.")

def Seleccionar_Archivo_Grafo():
    global graph
    filename = filedialog.askopenfilename(
        title="Selecciona un archivo de grafo",
        filetypes=[("Archivos de texto", "*.txt")]
    )
    if not filename:
        return
    graph = FileGraph(filename)
    if not graph:
        messagebox.showerror("Error", "El grafo está vacío o el formato del archivo es incorrecto.")
        return
    messagebox.showinfo("Éxito", "Grafo cargado con éxito!")
    Plot(graph)


def Mostrar_Nodos_Alcanzables():
    node_name = entry_nodo_alcanzable.get()
    current_graph = None

    if graph and graph.nodes:
        current_graph = graph
    elif custom_graph and custom_graph.nodes:
        current_graph = custom_graph
    else:
        messagebox.showwarning("Advertencia", "No se ha cargado ningún grafo o el grafo está vacío.")
        return

    start_node = None
    for node in current_graph.nodes:
        if node.name == node_name:
            start_node = node
            break

    if not start_node:
        messagebox.showerror("Error", f"Nodo {node_name} no encontrado en el grafo.")
        return

    reachable_nodes = find_reachable_nodes(current_graph, start_node)

    reachable_names = ", ".join([node.name for node in reachable_nodes])
    messagebox.showinfo("Nodos Alcanzables",
                        f"Nodos alcanzables desde {node_name}:\n{reachable_names}")

    plt.figure(figsize=(8, 6))

    for segment in current_graph.segments:
        x_values = [segment.origin.x, segment.destination.x]
        y_values = [segment.origin.y, segment.destination.y]
        plt.plot(x_values, y_values, 'k-', linewidth=1, color='gray')

    for node in current_graph.nodes:
        if node == start_node:
            plt.scatter(node.x, node.y, color='blue', s=100)
        elif node in reachable_nodes:
            plt.scatter(node.x, node.y, color='green', s=80)
        else:
            plt.scatter(node.x, node.y, color='lightgray', s=50)

        plt.text(node.x, node.y, f" {node.name}", fontsize=10, verticalalignment='bottom')

    plt.xlabel("X")
    plt.ylabel("Y")
    plt.title(f"Nodos alcanzables desde {node_name}")
    plt.grid(True, alpha=0.3)
    plt.show()

def Encontrar_Camino_Mas_Corto():
    origen = entry_camino_origen.get()
    destino = entry_camino_destino.get()
    current_graph = None

    if graph and graph.nodes:
        current_graph = graph
    elif custom_graph and custom_graph.nodes:
        current_graph = custom_graph
    else:
        messagebox.showwarning("Advertencia", "No se ha cargado ningún grafo o el grafo está vacío.")
        return

    nodo_origen = None
    nodo_destino = None
    for node in current_graph.nodes:
        if node.name == origen:
            nodo_origen = node
        if node.name == destino:
            nodo_destino = node

    if not nodo_origen or not nodo_destino:
        messagebox.showerror("Error", "Uno o ambos nodos no existen en el grafo.")
        return

    try:
        camino = find_shortest_path(current_graph, nodo_origen, nodo_destino)
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo calcular el camino: {str(e)}")
        return

    if not camino:
        messagebox.showinfo("Resultado", f"No se encontró un camino entre {origen} y {destino}.")
        return

    nombres_nodos = " -> ".join([node.name for node in camino.nodes])
    messagebox.showinfo("Camino más corto",
                        f"Camino encontrado:\n{nombres_nodos}\nCosto total: {camino.cost:.2f}")

    plt.figure(figsize=(8, 6))

    for segment in current_graph.segments:
        x_values = [segment.origin.x, segment.destination.x]
        y_values = [segment.origin.y, segment.destination.y]
        plt.plot(x_values, y_values, 'k-', linewidth=1, color='gray')

    for i in range(len(camino.nodes) - 1):
        x_values = [camino.nodes[i].x, camino.nodes[i + 1].x]
        y_values = [camino.nodes[i].y, camino.nodes[i + 1].y]
        plt.plot(x_values, y_values, 'r-', linewidth=2)

    for node in current_graph.nodes:
        if node in camino.nodes:
            plt.scatter(node.x, node.y, color='green', s=100)
        else:
            plt.scatter(node.x, node.y, color='black', s=50)
        plt.text(node.x, node.y, f" {node.name}", fontsize=12, verticalalignment='bottom')

    plt.xlabel("X")
    plt.ylabel("Y")
    plt.title(f"Camino más corto entre {origen} y {destino}")
    plt.grid(True)
    plt.show()


def Agregar_Nodo():
    nombre = entry_nombre_nodo.get()
    try:
        x = float(entry_x.get())
        y = float(entry_y.get())
    except ValueError:
        messagebox.showerror("Error", "Las coordenadas deben ser números.")
        return

    nodo = Node(nombre, x, y)
    if AddNode(custom_graph, nodo):
        messagebox.showinfo("Éxito", f"Nodo '{nombre}' agregado.")
    else:
        messagebox.showwarning("Aviso", f"El nodo '{nombre}' ya existe.")

def Agregar_Segmento():
    origen = entry_origen.get()
    destino = entry_destino.get()
    if AddSegment(custom_graph, origen, destino):
        messagebox.showinfo("Éxito", f"Segmento entre '{origen}' y '{destino}' agregado.")
    else:
        messagebox.showerror("Error", f"No se pudo agregar el segmento. Asegúrate de que ambos nodos existan.")

def Eliminar_Nodo():

    nombre = entry_eliminar_nodo.get()
    for nodo in custom_graph.nodes:
        if nodo.name == nombre:

            custom_graph.segments = [s for s in custom_graph.segments if s.origin.name != nombre and s.destination.name != nombre]
            custom_graph.nodes.remove(nodo)
            messagebox.showinfo("Éxito", f"Nodo '{nombre}' eliminado.")
            return
    messagebox.showerror("Error", f"No se encontró el nodo '{nombre}' en el grafo.")



def Mostrar_Grafo_Custom():
    Plot(custom_graph, title="Grafo Personalizado")

def Guardar_Grafo():
    filename = filedialog.asksaveasfilename(
        title="Guardar grafo como",
        defaultextension=".txt",
        filetypes=[("Archivos de texto", "*.txt")]
    )
    if not filename:
        return

    try:
        with open(filename, 'w') as f:
            for node in custom_graph.nodes:
                f.write(f"{node.name} {int(node.x)} {int(node.y)}\n")
            for seg in custom_graph.segments:
                f.write(f"{seg.origin.name} {seg.destination.name}\n")
        messagebox.showinfo("Éxito", f"Grafo guardado en {filename}")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo guardar el archivo: {e}")

# Sección de grafo de ejemplo:
example_frame = ttk.LabelFrame(frame, text="Gráficos de ejemplo", padding="10")
example_frame.grid(row=0, column=0, sticky="w", padx=10, pady=5)
Label(example_frame, text="Grafo de ejemplo (paso 3)", font=("Verdana", 12)).grid(row=0, column=0, sticky=W)
ttk.Button(example_frame, text="Mostrar", command=Mostrar_Grafo_Ejemplo).grid(row=0, column=1)

Label(example_frame, text="Grafo inventado (paso 3)", font=("Verdana", 12)).grid(row=1, column=0, sticky=W)
ttk.Button(example_frame, text="Mostrar", command=Mostrar_Grafo_Inventado).grid(row=1, column=1)

Label(example_frame, text="Seleccionar archivo de grafo", font=("Verdana", 12)).grid(row=2, column=0, sticky=W)
ttk.Button(example_frame, text="Seleccionar", command=Seleccionar_Archivo_Grafo).grid(row=2, column=1)

# Sección de nodo:
node_frame = ttk.LabelFrame(frame, text="Agregar Nodo", padding="10")
node_frame.grid(row=1, column=0, sticky="w", padx=10, pady=5)

Label(node_frame, text="Nombre nodo:").grid(row=0, column=0, sticky=W)
entry_nombre_nodo = ttk.Entry(node_frame)
entry_nombre_nodo.grid(row=0, column=1)

Label(node_frame, text="X:").grid(row=1, column=0, sticky=W)
entry_x = ttk.Entry(node_frame)
entry_x.grid(row=1, column=1)

Label(node_frame, text="Y:").grid(row=2, column=0, sticky=W)
entry_y = ttk.Entry(node_frame)
entry_y.grid(row=2, column=1)

ttk.Button(node_frame, text="Agregar nodo", command=Agregar_Nodo).grid(row=3, column=0, columnspan=2, pady=5)

# Sección de segmento:
segment_frame = ttk.LabelFrame(frame, text="Agregar Segmento", padding="10")
segment_frame.grid(row=2, column=0, sticky="w", padx=10, pady=5)

Label(segment_frame, text="Origen:").grid(row=0, column=0, sticky=W)
entry_origen = ttk.Entry(segment_frame)
entry_origen.grid(row=0, column=1)

Label(segment_frame, text="Destino:").grid(row=1, column=0, sticky=W)
entry_destino = ttk.Entry(segment_frame)
entry_destino.grid(row=1, column=1)

ttk.Button(segment_frame, text="Agregar segmento", command=Agregar_Segmento).grid(row=2, column=0, columnspan=2, pady=5)

# Sección para nodos alcanzables
reachable_frame = ttk.LabelFrame(frame, text="Nodos Alcanzables", padding="10")
reachable_frame.grid(row=1, column=1, sticky="w", padx=10, pady=5)

Label(reachable_frame, text="Nodo de inicio:").grid(row=0, column=0, sticky=W)
entry_nodo_alcanzable = ttk.Entry(reachable_frame)
entry_nodo_alcanzable.grid(row=0, column=1)

ttk.Button(reachable_frame, text="Mostrar nodos alcanzables",
          command=Mostrar_Nodos_Alcanzables).grid(row=1, column=0, columnspan=2, pady=5)

# Sección de camino más corto
path_frame = ttk.LabelFrame(frame, text="Camino más Corto", padding="10")
path_frame.grid(row=3, column=0, sticky="w", padx=10, pady=5)

Label(path_frame, text="Nodo origen:").grid(row=0, column=0, sticky=W)
entry_camino_origen = ttk.Entry(path_frame)
entry_camino_origen.grid(row=0, column=1)

Label(path_frame, text="Nodo destino:").grid(row=1, column=0, sticky=W)
entry_camino_destino = ttk.Entry(path_frame)
entry_camino_destino.grid(row=1, column=1)

ttk.Button(path_frame, text="Encontrar camino más corto", command=Encontrar_Camino_Mas_Corto).grid(row=2, column=0, columnspan=2, pady=5)

# Sección de visualización y guardado:
action_frame = ttk.LabelFrame(frame, text="Acciones de Grafo", padding="10")
action_frame.grid(row=4, column=0, sticky="w", padx=10, pady=5)

ttk.Button(action_frame, text="Mostrar grafo personalizado", command=Mostrar_Grafo_Custom).grid(row=0, column=0, pady=5)
ttk.Button(action_frame, text="Guardar grafo", command=Guardar_Grafo).grid(row=1, column=0, pady=5)

# Sección para eliminar nodos
delete_frame = ttk.LabelFrame(frame, text="Eliminar Nodo", padding="10")
delete_frame.grid(row=6, column=0, sticky="w", padx=10, pady=5)

Label(delete_frame, text="Nombre del nodo a eliminar:").grid(row=0, column=0, sticky=W)
entry_eliminar_nodo = ttk.Entry(delete_frame)
entry_eliminar_nodo.grid(row=0, column=1)

ttk.Button(delete_frame, text="Eliminar nodo", command=Eliminar_Nodo).grid(row=1, column=0, columnspan=2, pady=5)

# Botón de salida:
ttk.Button(frame, text="Salir", command=window.destroy).grid(row=7, column=0, columnspan=2, pady=10)

window.mainloop()
