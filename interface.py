from tkinter import *
from tkinter import ttk
from tkinter import filedialog, messagebox
from Graph import FileGraph, Plot, PlotNode, AddNode, AddSegment, Graph, PlotReachability
from Node import Node

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

def Vecinos_De_Un_Nodo():
    if graph is None:
        messagebox.showwarning("Advertencia", "No se ha cargado ningún grafo.")
        return

    node_name = node_entry.get()
    if not any(Node.name == node_name for Node in graph.nodes):
        messagebox.showerror("Error", f"Nodo {node_name} no encontrado en el grafo.")
        return

    PlotNode(graph, node_name, title=f"Grafo con el nodo {node_name} y sus vecinos")

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


def Mostrar_Nodos_Alcanzables():
    # Determinar qué grafo usar
    current_graph = None
    graph_name = ""

    if graph and graph.nodes:
        current_graph = graph
        graph_name = "cargado"
    elif custom_graph and custom_graph.nodes:
        current_graph = custom_graph
        graph_name = "personalizado"

    if not current_graph:
        messagebox.showwarning("Advertencia",
                               "No se ha cargado ningún grafo.\n\n"
                               "Por favor:\n"
                               "1. Carga un grafo desde archivo\n"
                               "2. Usa un grafo de ejemplo\n"
                               "3. O crea un grafo personalizado")
        return

    node_name = reach_entry.get().strip()
    if not node_name:
        messagebox.showwarning("Advertencia", "Por favor, introduce un nombre de nodo.")
        return

    if not any(node.name == node_name for node in current_graph.nodes):
        messagebox.showerror("Error", f"Nodo '{node_name}' no encontrado en el grafo {graph_name}.")
        return

    try:
        PlotReachability(current_graph, node_name)
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo mostrar los nodos alcanzables: {str(e)}")

def Mostrar_Camino_Mas_Corto():
    if graph is None:
        messagebox.showwarning("Advertencia", "No se ha cargado ningún grafo.")
        return

    origin = origin_entry.get()
    destination = dest_entry.get()

    if not any(nombre_nodo == origin for Node in graph.nodes):
        messagebox.showerror("Error", f"Nodo {origin} no encontrado en el grafo.")
        return

    if not any(nombre_nodo == destination for Node in graph.nodes):
        messagebox.showerror("Error", f"Nodo {destination} no encontrado en el grafo.")
        return

    path = FindShortestPath(graph, origin, destination)
    if path:
        path.PlotPath(graph)
    else:
        messagebox.showinfo("Información", f"No hay camino entre {origin} y {destination}")

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
            for Node in custom_graph.nodes:
                f.write(f"{Node.name} {int(Node.x)} {int(Node.y)}\n")
            for seg in custom_graph.segments:
                f.write(f"{seg.origin.name} {seg.destination.name}\n")
        messagebox.showinfo("Éxito", f"Grafo guardado en {filename}")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo guardar el archivo: {e}")


# Etiquetas y botones:

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

# Sección de visualización y guardado:
action_frame = ttk.LabelFrame(frame, text="Acciones de Grafo", padding="10")
action_frame.grid(row=3, column=0, sticky="w", padx=10, pady=5)

ttk.Button(action_frame, text="Mostrar grafo personalizado", command=Mostrar_Grafo_Custom).grid(row=0, column=0, pady=5)
ttk.Button(action_frame, text="Guardar grafo", command=Guardar_Grafo).grid(row=1, column=0, pady=5)

# Sección para ver vecinos del nodo:
neighbors_frame = ttk.LabelFrame(frame, text="Ver Vecinos de Nodo", padding="10")
neighbors_frame.grid(row=4, column=0, sticky="w", padx=10, pady=5)

Label(neighbors_frame, text="Nombre del nodo:").grid(row=0, column=0, sticky=W)
node_entry = ttk.Entry(neighbors_frame)
node_entry.grid(row=0, column=1)

ttk.Button(neighbors_frame, text="Mostrar vecinos", command=Vecinos_De_Un_Nodo).grid(row=1, column=0, columnspan=2, pady=5)

# Sección para eliminar nodos
delete_frame = ttk.LabelFrame(frame, text="Eliminar Nodo", padding="10")
delete_frame.grid(row=1, column=1, sticky="w", padx=10, pady=5)

Label(delete_frame, text="Nombre del nodo a eliminar:").grid(row=0, column=0, sticky=W)
entry_eliminar_nodo = ttk.Entry(delete_frame)
entry_eliminar_nodo.grid(row=0, column=1)

ttk.Button(delete_frame, text="Eliminar nodo", command=Eliminar_Nodo).grid(row=1, column=0, columnspan=2, pady=10)

# Sección para nodos alcanzables
reach_frame = ttk.LabelFrame(frame, text="Nodos Alcanzables", padding="10")
reach_frame.grid(row=5, column=0, sticky="w", padx=10, pady=5)

Label(reach_frame, text="Nodo origen:").grid(row=0, column=0, sticky=W)
reach_entry = ttk.Entry(reach_frame)
reach_entry.grid(row=0, column=1)

ttk.Button(reach_frame, text="Mostrar nodos alcanzables", command=Mostrar_Nodos_Alcanzables).grid(row=1, column=0, columnspan=2, pady=5)

# Sección para camino más corto
path_frame = ttk.LabelFrame(frame, text="Camino Más Corto", padding="10")
path_frame.grid(row=6, column=0, sticky="w", padx=10, pady=5)

Label(path_frame, text="Nodo origen:").grid(row=0, column=0, sticky=W)
origin_entry = ttk.Entry(path_frame)
origin_entry.grid(row=0, column=1)

Label(path_frame, text="Nodo destino:").grid(row=1, column=0, sticky=W)
dest_entry = ttk.Entry(path_frame)
dest_entry.grid(row=1, column=1)

ttk.Button(path_frame, text="Mostrar camino más corto", command=Mostrar_Camino_Mas_Corto).grid(row=2, column=0, columnspan=2, pady=5)

# Botón de salida:
ttk.Button(frame, text="Salir", command=window.destroy).grid(row=7, column=0, columnspan=2, pady=10)

window.mainloop()
