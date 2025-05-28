import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from Graph import Grafico_fichero, Plot, Añadir_nodo, Añadir_segmento, Graph, Encontrar_camino_mas_corto, Encontrar_nodos_alcanzables, Plot_ratón
from Node import Node
import matplotlib.pyplot as plt
from KML import generar_camino_kml
import os

window = tk.Tk()
window.title("Editor de Grafos")
window.configure(bg='#f0f0f0')

frame = ttk.Frame(window, padding=10)
frame.grid(row=0, column=0, sticky="nsew")

custom_graph = Graph()
fig = None
canvas = None

# Entry widgets
entry_nombre_nodo = entry_x = entry_y = None
entry_origen = entry_destino = None
entry_eliminar_nodo = node_entry = None
entry_nodo_alcanzable = entry_camino_origen = entry_camino_destino = None

plot_frame = ttk.LabelFrame(frame, text="Visualización del Grafo", padding="10")
plot_frame.grid(row=0, column=2, rowspan=10, padx=10, pady=5, sticky="nsew")

def embed_plot(fig):
    global canvas
    for widget in plot_frame.winfo_children():
        widget.destroy()

    canvas = FigureCanvasTkAgg(fig, master=plot_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill='both', expand=True)

    # --- Zoom con rueda del ratón ---
    def on_scroll(event):
        ax = fig.gca()  # Obtener el eje actual
        scale_factor = 1.2 if event.button == 'up' else 0.8  # Zoom in/out

        # Límites actuales de los ejes
        xlim = ax.get_xlim()
        ylim = ax.get_ylim()

        # Nuevos límites (centrados en la posición del mouse)
        new_xlim = [
            event.xdata - (event.xdata - xlim[0]) * scale_factor,
            event.xdata + (xlim[1] - event.xdata) * scale_factor
        ]
        new_ylim = [
            event.ydata - (event.ydata - ylim[0]) * scale_factor,
            event.ydata + (ylim[1] - event.ydata) * scale_factor
        ]

        ax.set_xlim(new_xlim)
        ax.set_ylim(new_ylim)
        canvas.draw()

    # Conectar el evento de scroll
    fig.canvas.mpl_connect('scroll_event', on_scroll)

def Mostrar_Grafo_Ejemplo():
    from test_graph import CrearGrafo_1
    G = CrearGrafo_1()
    custom_graph.nodes = G.nodes
    custom_graph.segments = G.segments
    fig = Plot(custom_graph, title="Ejemplo 1")
    embed_plot(fig)

def Mostrar_Grafo_Inventado():
    from test_graph import CrearGrafo_2
    G = CrearGrafo_2()
    custom_graph.nodes = G.nodes
    custom_graph.segments = G.segments
    fig = Plot(custom_graph, title="Ejemplo 2")
    embed_plot(fig)


def Seleccionar_Archivo_Grafo():
    filename = filedialog.askopenfilename(filetypes=[("Archivos de texto", "*.txt")])
    if not filename:
        return

    if "_nav" in filename:
        seg_file = filename.replace("_nav", "_seg")
        aer_file = filename.replace("_nav", "_aer")
        file_graph = Grafico_fichero(filename, seg_file, aer_file)
    else:
        #Si no hay ficheros, genera un grafo corriente
        file_graph = Grafico_fichero(filename)

    if not file_graph or not file_graph.nodes:
        messagebox.showerror("Error", "Archivo inválido o vacío.")
        return

    custom_graph.nodes = file_graph.nodes
    custom_graph.segments = file_graph.segments
    custom_graph.airport_nodes = getattr(file_graph, 'airport_nodes', set())

    messagebox.showinfo("Éxito", "Grafo cargado correctamente.")
    fig = Plot(custom_graph, airport_nodes=custom_graph.airport_nodes)
    embed_plot(fig)

def Mostrar_Nodos_Alcanzables():
    node_name = entry_nodo_alcanzable.get()
    current_graph = custom_graph

    if not current_graph.nodes:
        messagebox.showwarning("Advertencia", "No hay nodos en el grafo.")
        return

    start_node = next((n for n in current_graph.nodes if n.name == node_name), None)
    if not start_node:
        messagebox.showerror("Error", f"Nodo {node_name} no encontrado.")
        return

    reachable = Encontrar_nodos_alcanzables(current_graph, start_node)
    if len(reachable) <= 1:
        message = f"{node_name} no tiene conexiones salientes."
    else:
        names = ", ".join(n.name for n in reachable if n != start_node)
        message = f"Nodos alcanzables desde {node_name}:\n{names}"
    messagebox.showinfo("Alcanzables", message)

    fig = Plot(current_graph, highlight_nodes=reachable, title=f"Desde {node_name}")
    embed_plot(fig)


def Camino_Mas_Corto():
    origen = entry_camino_origen.get().strip()
    destino = entry_camino_destino.get().strip()

    if not origen or not destino:
        messagebox.showwarning("Input Error", "Porfavor, introduzca un punto de origen y destino")
        return

    current_graph = custom_graph

    nodo_origen = next((n for n in current_graph.nodes if n.name == origen), None)
    nodo_destino = next((n for n in current_graph.nodes if n.name == destino), None)

    if not nodo_origen:
        messagebox.showerror("Error", f"Nodo de origen: '{origen}' no encontrado")
        return
    if not nodo_destino:
        messagebox.showerror("Error", f"Nodo destinación '{destino}' no encontrado")
        return

    try:
        #Calcula el camino mas corto con la funcion Encontrar_camino_mas_corto
        camino = Encontrar_camino_mas_corto(current_graph, nodo_origen, nodo_destino)

        if camino:
            #Si encuentra un camino envia un mensaje de exito
            names = " → ".join(n.name for n in camino.nodes)
            messagebox.showinfo(
                "Camino mas corto encontrado",
                f"{names}\nCoste total: {camino.cost:.2f}"
            )

            #Para visualizar el camino
            fig, ax = plt.subplots(figsize=(8, 6))

            # Dibuja los segmentos restantes en gris
            for seg in current_graph.segments:
                ax.plot([seg.origin.x, seg.destination.x],
                        [seg.origin.y, seg.destination.y],
                        'gray', linewidth=1, alpha=0.5)

            # Pinta el recorrido en rojo
            for i in range(len(camino.nodes) - 1):
                ax.plot([camino.nodes[i].x, camino.nodes[i + 1].x],
                        [camino.nodes[i].y, camino.nodes[i + 1].y],
                        'red', linewidth=2)

            # Pinta los nodos del camino en rojo
            for node in current_graph.nodes:
                color = 'red' if node in camino.nodes else 'gray'
                ax.scatter(node.x, node.y, color=color)
                ax.text(node.x, node.y, f" {node.name}", fontsize=9)

            ax.set_title(f"Camino mas corto: {origen} → {destino}")
            ax.grid(True)
            embed_plot(fig)

        else:
            messagebox.showinfo(
                "No se ha encontrado un camino",
                f"No existe un camino entre {origen} y {destino}"
            )

    except Exception as e:
        messagebox.showerror(
            "Error de calculo",
            f"Error encontrando el camino mas corto:\n{str(e)}"
        )

def Agregar_Nodo():
    nombre = entry_nombre_nodo.get()
    try:
        x = float(entry_x.get())
        y = float(entry_y.get())
    except ValueError:
        messagebox.showerror("Error", "Coordenadas inválidas.")
        return
    if Añadir_nodo(custom_graph, Node(nombre, x, y)):
        messagebox.showinfo("Éxito", f"Nodo '{nombre}' agregado.")
    else:
        messagebox.showwarning("Duplicado", f"El nodo '{nombre}' ya existe.")

def Agregar_Segmento():
    if Añadir_segmento(custom_graph, entry_origen.get(), entry_destino.get()):
        messagebox.showinfo("Éxito", "Segmento agregado.")
    else:
        messagebox.showerror("Error", "Asegúrate de que los nodos existan.")

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
    fig = Plot_ratón(custom_graph, title="Grafo Personalizado")
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
        messagebox.showinfo("Éxito", "Grafo guardado.")
    except Exception as e:
        messagebox.showerror("Error", str(e))


def plot_navpoints():
    try:
        # Carga los nodos y segmentos
        nav_graph = Grafico_fichero("_nav.txt", "_seg.txt")

        if not nav_graph or not nav_graph.nodes:
            messagebox.showerror("Error", "Fallo al cargar la información de navegación")
            return

        #Dibuja el grafo, con la información de los ficheros
        fig = Plot(nav_graph, title="Custom map")

        # Limites de los ejes
        all_x = [node.x for node in nav_graph.nodes]
        all_y = [node.y for node in nav_graph.nodes]
        ax = fig.gca()
        ax.set_xlim(min(all_x) - 0.5, max(all_x) + 0.5)
        ax.set_ylim(min(all_y) - 0.5, max(all_y) + 0.5)

        embed_plot(fig)

    except Exception as e:
        messagebox.showerror("Error", f"Fallo al dibujar los puntos de navegación: {str(e)}")


def Exportar_a_KML():
    if not hasattr(custom_graph, 'nodes') or not custom_graph.nodes:
        messagebox.showwarning("Advertencia", "No hay datos a exportar")
        return

    # Para determinar si exportar todo o un camino
    elección_exportar = messagebox.askquestion(
        "Opciones de exportación",
        "¿Exportar todo el grafo? (Si para todos los nodos, No para solo exportar el camino)",
        icon='question'
    )

    filename = filedialog.asksaveasfilename(
        defaultextension=".kml",
        filetypes=[("KML Files", "*.kml")],
        title="Guardar fichero KML"
    )
    if not filename:
        return

    try:
        if elección_exportar == 'si':
            # Exportar todos los nodos
            generar_camino_kml(custom_graph.nodes, filename)
            messagebox.showinfo(
                "Exito",
                f"Se han exportado los {len(custom_graph.nodes)} nodos a:\n{filename}"
            )
        else:
            # Exporta el camino mas corto
            if hasattr(custom_graph, 'shortest_path') and custom_graph.shortest_path:
                generar_camino_kml(custom_graph.shortest_path.nodes, filename)
                messagebox.showinfo(
                    "Exito",
                    f"Se ha exportado ({len(custom_graph.shortest_path.nodes)} points) a:\n{filename}"
                )
            else:
                messagebox.showwarning(
                    "No se ha seleccionado un camino",
                    "Porfavor, calcule un camino mas corto usando la interfaz"
                )
                return

        # Abrir en Google Earth
        if messagebox.askyesno(
                "Abrir en Google Earth",
                "¿Desea abrir el fichero KML en Google Earth?"
        ):
            try:
                os.startfile(filename)
            except Exception as e:
                messagebox.showerror(
                    "Error",
                    f"No se ha podido abrir Google Earth:\n{str(e)}"
                )

    except Exception as e:
        messagebox.showerror(
            "Fallo en la exportación",
            f"Error al exportar a KML:\n{str(e)}"
        )

# --- UI Layouts ---

def create_entry(label, parent, row):
    ttk.Label(parent, text=label).grid(row=row, column=0, sticky="w")
    entry = ttk.Entry(parent)
    entry.grid(row=row, column=1)
    return entry


# Graficos de ejemplo
example_frame = ttk.LabelFrame(frame, text="Ejemplos", padding="10")
example_frame.grid(row=0, column=0, columnspan=2, sticky="ew")
ttk.Button(example_frame, text="Ejemplo 1", command=Mostrar_Grafo_Ejemplo).grid(row=0, column=0)
ttk.Button(example_frame, text="Ejemplo 2", command=Mostrar_Grafo_Inventado).grid(row=0, column=1)
ttk.Button(example_frame, text="Cargar archivo", command=Seleccionar_Archivo_Grafo).grid(row=0, column=2)

# Añadir nodos
node_frame = ttk.LabelFrame(frame, text="Agregar Nodo", padding="10")
node_frame.grid(row=1, column=0, sticky="w")
entry_nombre_nodo = create_entry("Nombre:", node_frame, 0)
entry_x = create_entry("X:", node_frame, 1)
entry_y = create_entry("Y:", node_frame, 2)
ttk.Button(node_frame, text="Agregar", command=Agregar_Nodo).grid(row=3, column=0, columnspan=2)

# Añadir segmentos
segment_frame = ttk.LabelFrame(frame, text="Agregar Segmento", padding="10")
segment_frame.grid(row=2, column=0, sticky="w")
entry_origen = create_entry("Origen:", segment_frame, 0)
entry_destino = create_entry("Destino:", segment_frame, 1)
ttk.Button(segment_frame, text="Agregar", command=Agregar_Segmento).grid(row=2, column=0, columnspan=2)

# Borrar nodo
delete_frame = ttk.LabelFrame(frame, text="Eliminar Nodo", padding="10")
delete_frame.grid(row=3, column=0, sticky="w")
entry_eliminar_nodo = create_entry("Nombre:", delete_frame, 0)
ttk.Button(delete_frame, text="Eliminar", command=Eliminar_Nodo).grid(row=1, column=0, columnspan=2)

# Dibujar grafo
ttk.Button(frame, text="Mostrar Grafo Personalizado", command=Mostrar_Grafo_Custom).grid(row=4, column=0, pady=5)
ttk.Button(frame, text="Guardar Grafo", command=Guardar_Grafo).grid(row=4, column=1)

# Nodos alcanzables
alcance_frame = ttk.LabelFrame(frame, text="Alcanzables", padding="10")
alcance_frame.grid(row=5, column=0, sticky="w")
entry_nodo_alcanzable = create_entry("Desde nodo:", alcance_frame, 0)
ttk.Button(alcance_frame, text="Mostrar", command=Mostrar_Nodos_Alcanzables).grid(row=1, column=0, columnspan=2)

# Camino mas corto
camino_frame = ttk.LabelFrame(frame, text="Camino más corto", padding="10")
camino_frame.grid(row=6, column=0, sticky="w")
entry_camino_origen = create_entry("Origen:", camino_frame, 0)
entry_camino_destino = create_entry("Destino:", camino_frame, 1)
ttk.Button(camino_frame, text="Buscar", command=Camino_Mas_Corto).grid(row=2, column=0, columnspan=2)

# Exportar a KML
ttk.Button(frame, text="Exportar a KML", command=Exportar_a_KML).grid(row=8, column=0, pady=5)

window.mainloop()