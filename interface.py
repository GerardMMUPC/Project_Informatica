import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from Graph import FileGraph, Plot, PlotNode, AddNode, AddSegment, Graph
from Node import Node

window = tk.Tk()
window.title("Editor de Grafos")
window.configure(bg='#f0f0f0')

frame = ttk.Frame(window, padding=10)
frame.grid(row=0, column=0, sticky="nsew")

graph = None
custom_graph = Graph()

plot_frame = ttk.LabelFrame(frame, text="Visualización del Grafo", padding="10")
plot_frame.grid(row=0, column=1, rowspan=8, padx=10, pady=5, sticky="nsew")

fig = None
canvas = None

# Global entry widgets
entry_nombre_nodo = None
entry_x = None
entry_y = None
entry_origen = None
entry_destino = None
entry_eliminar_nodo = None
node_entry = None

def embed_plot(fig):
    global canvas
    for widget in plot_frame.winfo_children():
        widget.destroy()
    canvas = FigureCanvasTkAgg(fig, master=plot_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill='both', expand=True)

def Mostrar_Grafo_Ejemplo():
    from test_graph import CreateGraph_1
    G1 = CreateGraph_1()
    global fig
    fig = Plot(G1, title="Ejemplo 1")
    embed_plot(fig)

def Mostrar_Grafo_Inventado():
    from test_graph import CreateGraph_2
    G2 = CreateGraph_2()
    global fig
    fig = Plot(G2, title="Ejemplo 2")
    embed_plot(fig)

def Seleccionar_Archivo_Grafo():
    global graph, fig
    filename = filedialog.askopenfilename(filetypes=[("Archivos de texto", "*.txt")])
    if not filename:
        return
    graph = FileGraph(filename)
    if not graph:
        messagebox.showerror("Error", "El archivo está vacío o mal formado.")
        return
    fig = Plot(graph)
    embed_plot(fig)

def Vecinos_De_Un_Nodo():
    if graph is None:
        messagebox.showwarning("Advertencia", "No se ha cargado ningún grafo.")
        return
    node_name = node_entry.get()
    fig = PlotNode(graph, node_name, title="Vecinos del nodo")
    embed_plot(fig)

def Agregar_Nodo():
    nombre = entry_nombre_nodo.get()
    try:
        x = float(entry_x.get())
        y = float(entry_y.get())
    except ValueError:
        messagebox.showerror("Error", "Coordenadas inválidas.")
        return
    nodo = Node(nombre, x, y)
    if AddNode(custom_graph, nodo):
        messagebox.showinfo("Éxito", f"Nodo '{nombre}' agregado.")
    else:
        messagebox.showwarning("Aviso", f"Nodo '{nombre}' ya existe.")

def Agregar_Segmento():
    origen = entry_origen.get()
    destino = entry_destino.get()
    if AddSegment(custom_graph, origen, destino):
        messagebox.showinfo("Éxito", f"Segmento '{origen} → {destino}' agregado.")
    else:
        messagebox.showerror("Error", "Los nodos no existen.")

def Eliminar_Nodo():
    nombre = entry_eliminar_nodo.get()
    for nodo in custom_graph.nodes:
        if nodo.name == nombre:
            custom_graph.segments = [s for s in custom_graph.segments if s.origin.name != nombre and s.destination.name != nombre]
            custom_graph.nodes.remove(nodo)
            messagebox.showinfo("Éxito", f"Nodo '{nombre}' eliminado.")
            return
    messagebox.showerror("Error", f"Nodo '{nombre}' no encontrado.")

def Mostrar_Grafo_Custom():
    global fig
    fig = Plot(custom_graph, title="Grafo Personalizado")
    embed_plot(fig)

def Guardar_Grafo():
    filename = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Archivos de texto", "*.txt")])
    if not filename:
        return
    try:
        with open(filename, 'w') as f:
            for node in custom_graph.nodes:
                f.write(f"{node.name} {int(node.x)} {int(node.y)}\n")
            for seg in custom_graph.segments:
                f.write(f"{seg.origin.name} {seg.destination.name}\n")
        messagebox.showinfo("Éxito", "Grafo guardado correctamente.")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo guardar el archivo: {e}")

# Zoom In function (for MouseWheel)
def zoom_in(event):
    if fig is None:
        return
    ax = fig.axes[0]
    xlim, ylim = ax.get_xlim(), ax.get_ylim()
    zoom_factor = 0.8  # Zoom in by 80%
    ax.set_xlim([x * zoom_factor for x in xlim])
    ax.set_ylim([y * zoom_factor for y in ylim])
    canvas.draw()

# Zoom Out function (for MouseWheel)
def zoom_out(event):
    if fig is None:
        return
    ax = fig.axes[0]
    xlim, ylim = ax.get_xlim(), ax.get_ylim()
    zoom_factor = 1.2  # Zoom out by 120%
    ax.set_xlim([x * zoom_factor for x in xlim])
    ax.set_ylim([y * zoom_factor for y in ylim])
    canvas.draw()

# Bind mouse scroll event to zoom in or out
window.bind("<MouseWheel>", lambda event: zoom_in(event) if event.delta > 0 else zoom_out(event))

# Widgets
def create_entry(label_text, parent, row):
    ttk.Label(parent, text=label_text).grid(row=row, column=0, sticky="w")
    entry = ttk.Entry(parent)
    entry.grid(row=row, column=1)
    return entry

# Gráficos ejemplo
example_frame = ttk.LabelFrame(frame, text="Gráficos de ejemplo", padding="10")
example_frame.grid(row=0, column=0, sticky="w", padx=10, pady=5)
ttk.Button(example_frame, text="Ejemplo 1", command=Mostrar_Grafo_Ejemplo).grid(row=0, column=0)
ttk.Button(example_frame, text="Ejemplo 2", command=Mostrar_Grafo_Inventado).grid(row=0, column=1)
ttk.Button(example_frame, text="Cargar archivo", command=Seleccionar_Archivo_Grafo).grid(row=0, column=2)

# Node Inputs
node_frame = ttk.LabelFrame(frame, text="Agregar Nodo", padding="10")
node_frame.grid(row=1, column=0, sticky="w", padx=10)
entry_nombre_nodo = create_entry("Nombre:", node_frame, 0)
entry_x = create_entry("X:", node_frame, 1)
entry_y = create_entry("Y:", node_frame, 2)
ttk.Button(node_frame, text="Agregar nodo", command=Agregar_Nodo).grid(row=3, column=0, columnspan=2)

# Segment Inputs
segment_frame = ttk.LabelFrame(frame, text="Agregar Segmento", padding="10")
segment_frame.grid(row=2, column=0, sticky="w", padx=10)
entry_origen = create_entry("Origen:", segment_frame, 0)
entry_destino = create_entry("Destino:", segment_frame, 1)
ttk.Button(segment_frame, text="Agregar segmento", command=Agregar_Segmento).grid(row=2, column=0, columnspan=2)

# Vecinos
neighbors_frame = ttk.LabelFrame(frame, text="Ver Vecinos", padding="10")
neighbors_frame.grid(row=3, column=0, sticky="w", padx=10)
node_entry = create_entry("Nodo:", neighbors_frame, 0)
ttk.Button(neighbors_frame, text="Mostrar vecinos", command=Vecinos_De_Un_Nodo).grid(row=1, column=0, columnspan=2)

# Eliminar
delete_frame = ttk.LabelFrame(frame, text="Eliminar Nodo", padding=10)
delete_frame.grid(row=4, column=0, sticky="w")
entry_eliminar_nodo = create_entry("Nodo:", delete_frame, 0)
ttk.Button(delete_frame, text="Eliminar nodo", command=Eliminar_Nodo).grid(row=1, column=0, columnspan=2)

# Acciones
action_frame = ttk.LabelFrame(frame, text="Acciones", padding=10)
action_frame.grid(row=5, column=0, sticky="w")
ttk.Button(action_frame, text="Mostrar grafo personalizado", command=Mostrar_Grafo_Custom).grid(row=0, column=0)
ttk.Button(action_frame, text="Guardar grafo", command=Guardar_Grafo).grid(row=1, column=0)

# Salir
ttk.Button(frame, text="Salir", command=window.destroy).grid(row=6, column=0, pady=10)

window.mainloop()
