import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from Graph import Grafico_fichero, Plot, Añadir_nodo, Añadir_segmento, Graph, Encontrar_camino_mas_corto, Encontrar_nodos_alcanzables, Plot_ratón
from Node import Node
from test_graph import Cargar_Mapa_Catalunya, Cargar_Mapa_España, Cargar_Mapa_ECAC
import matplotlib.pyplot as plt
from KML import generar_camino_kml
import os
from PIL import Image, ImageTk

window = tk.Tk()
window.title("Editor de Grafos")
window.configure(bg='#f0f0f0')


style = ttk.Style()

# Estilo común para ambos botones (verde con texto negro)
style.configure('Common.TButton',
               foreground='black',       # Texto negro (cambia 'white' a 'black')
               background='#4CAF50',    # Fondo verde
               font=('Helvetica', 10, 'bold'),
               padding=5)
style.map('Common.TButton',
          background=[('active', '#45A049'),  # Verde oscuro al pasar el ratón
                     ('disabled', '#cccccc')],
          foreground=[('active', 'black'),    # Texto negro incluso al pasar el ratón
                     ('disabled', '#888888')])  # Texto gris si está deshabilitado

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

    ax = fig.gca()
    original_xlim = ax.get_xlim()
    original_ylim = ax.get_ylim()

    def reset_zoom():
        ax.set_xlim(original_xlim)
        ax.set_ylim(original_ylim)
        canvas.draw()
        print("Resetting zoom.")

    # Reset Zoom button con estilo común
    reset_button = ttk.Button(plot_frame,
                              text="Reset Zoom",
                              command=reset_zoom,
                              style='Common.TButton')
    reset_button.grid(row=0, column=0, sticky="ew", pady=5)

    canvas = FigureCanvasTkAgg(fig, master=plot_frame)
    canvas.draw()
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.grid(row=1, column=0, sticky="nsew")

    plot_frame.rowconfigure(1, weight=1)
    plot_frame.columnconfigure(0, weight=1)

    # Función para manejar zoom con scroll
    def On_Scroll(event):
        ax = fig.gca()
        scale_factor = 1.2 if event.button == 'up' else 0.8

        xlim = ax.get_xlim()
        ylim = ax.get_ylim()

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

    # Función para manejar clics en nodos
    clicked_nodes = []

    def On_Click(event):
        if event.inaxes is None:
            return

        click_x, click_y = event.xdata, event.ydata

        nearest_node = None
        min_dist = float('inf')
        for node in custom_graph.nodes:
            dist = ((node.x - click_x) ** 2 + (node.y - click_y) ** 2) ** 0.5
            if dist < min_dist and dist < 1.0:
                min_dist = dist
                nearest_node = node

        if nearest_node:
            clicked_nodes.append(nearest_node)
            print(f"Selected: {nearest_node.name}")

            if len(clicked_nodes) == 2:
                node1, node2 = clicked_nodes
                path = Encontrar_camino_mas_corto(custom_graph, node1, node2)

                if path:
                    fig, ax = plt.subplots(figsize=(8, 6))

                    # Dibujar todos los segmentos en gris
                    for seg in custom_graph.segments:
                        ax.plot([seg.origin.x, seg.destination.x],
                                [seg.origin.y, seg.destination.y],
                                'gray', linewidth=1, alpha=0.5)

                    # Dibujar el camino en rojo
                    for i in range(len(path.nodes) - 1):
                        ax.plot([path.nodes[i].x, path.nodes[i + 1].x],
                                [path.nodes[i].y, path.nodes[i + 1].y],
                                'red', linewidth=2)

                    # Dibujar nodos
                    for node in custom_graph.nodes:
                        color = 'red' if node in path.nodes else 'gray'
                        ax.scatter(node.x, node.y, color=color)
                        ax.text(node.x, node.y, f" {node.name}", fontsize=9)

                    ax.set_title(f"Camino más corto: {node1.name} → {node2.name}")
                    ax.grid(True)
                    clicked_nodes.clear()
                    embed_plot(fig)
                else:
                    messagebox.showinfo("Información", "No se encontró camino entre los nodos")
                    clicked_nodes.clear()

    # Conectar eventos
    fig.canvas.mpl_connect('scroll_event', On_Scroll)
    fig.canvas.mpl_connect("button_press_event", On_Click)

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


def Encontrar_Camino_Mas_Corto():
    origen = entry_camino_origen.get().strip()
    destino = entry_camino_destino.get().strip()

    if not origen or not destino:
        messagebox.showwarning("Error input", "Porfavor introducir un origen y un destino")
        return

    current_graph = custom_graph


    nodo_origen = next((n for n in current_graph.nodes if n.name == origen), None)
    nodo_destino = next((n for n in current_graph.nodes if n.name == destino), None)

    if not nodo_origen:
        messagebox.showerror("Error", f"Nodo de origen '{origen}' no encontrado")
        return
    if not nodo_destino:
        messagebox.showerror("Error", f"Nodo de destino '{destino}' no encontrado")
        return

    try:
        #calcular camino
        camino = Encontrar_camino_mas_corto(current_graph, nodo_origen, nodo_destino)

        if camino:
            names = " → ".join(n.name for n in camino.nodes)
            messagebox.showinfo(
                "Camino mas corto encontrado",
                f"{names}\nCoste total: {camino.cost:.2f}"
            )

            # Visualizar el camino
            fig, ax = plt.subplots(figsize=(8, 6))

            # Dibujar segmentos en gris
            for seg in current_graph.segments:
                ax.plot([seg.origin.x, seg.destination.x],
                        [seg.origin.y, seg.destination.y],
                        'gray', linewidth=1, alpha=0.5)

            # Camino en rojo
            for i in range(len(camino.nodes) - 1):
                ax.plot([camino.nodes[i].x, camino.nodes[i + 1].x],
                        [camino.nodes[i].y, camino.nodes[i + 1].y],
                        'red', linewidth=2)

            # Dibujar nodos
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
            "Error",
            f"Error al buscar el camino mas corto:\n{str(e)}"
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


def Mostrar_Navpoints_Sobrevolar():
    # Verificar si hay un camino calculado
    if not hasattr(custom_graph, 'shortest_path') or not custom_graph.shortest_path:
        messagebox.showwarning("Advertencia", "Primero calcule un camino usando 'Camino más corto'")
        return

    # Obtener nodos del camino
    nodos_camino = custom_graph.shortest_path.nodes

    # Crear ventana emergente
    ventana_navpoints = tk.Toplevel(window)
    ventana_navpoints.title("Puntos de Navegación Sobrevolar")
    ventana_navpoints.geometry("500x400")

    # Frame principal con scrollbar
    frame_principal = ttk.Frame(ventana_navpoints)
    frame_principal.pack(fill='both', expand=True, padx=10, pady=10)

    # Texto con los puntos
    texto_navpoints = tk.Text(frame_principal, wrap='word', font=('Courier', 10))
    scrollbar = ttk.Scrollbar(frame_principal, command=texto_navpoints.yview)
    texto_navpoints.configure(yscrollcommand=scrollbar.set)

    scrollbar.pack(side='right', fill='y')
    texto_navpoints.pack(fill='both', expand=True)

    # Cabecera
    texto_navpoints.insert('end', "Puntos de navegación en el trayecto:\n\n")
    texto_navpoints.insert('end', "{:<10} {:<15} {:<15}\n".format("Nombre", "Latitud", "Longitud"))
    texto_navpoints.insert('end', "-" * 45 + "\n")

    # Lista de puntos con coordenadas
    for nodo in nodos_camino:
        texto_navpoints.insert('end', "{:<10} {:<15.6f} {:<15.6f}\n".format(
            nodo.name, nodo.y, nodo.x  # Nota: y=latitud, x=longitud
        ))

    texto_navpoints.config(state='disabled')

    # Botón para exportar
    btn_exportar = ttk.Button(ventana_navpoints,
                              text="Exportar a KML",
                              command=Exportar_a_KML)
    btn_exportar.pack(pady=10)


def Exportar_a_KML():
    if not hasattr(custom_graph, 'nodes') or not custom_graph.nodes:
        messagebox.showwarning("Advertencia", "No hay datos a exportar")
        return

    export_choice = messagebox.askquestion(
        "Opciones de exportación",
        "¿Exportar todo el grafo? (Si para todos los nodos, No para el camino actual)",
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
        if export_choice == 'yes':
            # Export all nodes
            generar_camino_kml(custom_graph.nodes, filename)
            messagebox.showinfo(
                "Exito",
                f"Exportado {len(custom_graph.nodes)} nodos a:\n{filename}"
            )
        else:
            # Export current path if available
            if hasattr(custom_graph, 'shortest_path') and custom_graph.shortest_path:
                generar_camino_kml(custom_graph.shortest_path.nodes, filename)
                messagebox.showinfo(
                    "Exito",
                    f"Exportado el camino ({len(custom_graph.shortest_path.nodes)} points) a:\n{filename}"
                )
            else:
                messagebox.showwarning(
                    "No hay ningun camino",
                    "Porfavor calcular un camino usando la funcion en la interfaz"
                )
                return

        if messagebox.askyesno(
                "Abrir en google earth",
                "¿Abrir el fichero en Google earth?"
        ):
            try:
                os.startfile(filename)
            except Exception as e:
                messagebox.showerror(
                    "Error",
                    f"No se pudo abrir en Google Earth:\n{str(e)}"
                )

    except Exception as e:
        messagebox.showerror(
            "Error exportación",
            f"Error durante exportación a KML:\n{str(e)}"
        )


def create_entry(label, parent, row):
    ttk.Label(parent, text=label).grid(row=row, column=0, sticky="w")
    entry = ttk.Entry(parent)
    entry.grid(row=row, column=1)
    return entry

def Mostrar_Imagenes():
    img_window = tk.Toplevel(window)
    img_window.title("Imágenes de personas")

    image_paths = [
        "C:/Users/polso/OneDrive/Imágenes/Saved Pictures/IMG-20250528-WA0011.jpg", "C:/Users/polso/OneDrive/Imágenes/Saved Pictures/Screenshot_20250528_200036_Gallery.jpg",
        "C:/Users/polso/OneDrive/Imágenes/Saved Pictures/IMG_1755.jpg", "C:/Users/polso/OneDrive/Imágenes/Saved Pictures/20250528_195800.jpg"

    ]

    image_refs = []

    for i, path in enumerate(image_paths):
        try:
            img = Image.open(path)
            img = img.resize((150, 150))
            img_tk = ImageTk.PhotoImage(img)
            image_refs.append(img_tk)  # evita que se borren por el recolector de basura

            label = ttk.Label(img_window, image=img_tk)
            label.grid(row=i // 2, column=i % 2, padx=10, pady=10)

        except Exception as e:
            print(f"Error loading {path}: {e}")
            label = ttk.Label(img_window, text=f"Error: {path}")
            label.grid(row=i // 2, column=i % 2)

    img_window.image_refs = image_refs

def Mostrar_Mapa_Aereo():
    # Crear ventana de selección
    selection_win = tk.Toplevel(window)
    selection_win.title("Seleccionar Mapa Aéreo")
    selection_win.geometry("300x150")

    # Definir las funciones de carga primero
    def cargar_catalunya():
        try:
            graph = Cargar_Mapa_Catalunya()
            mostrar_mapa(graph, "Mapa Aéreo de Catalunya")
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar mapa: {str(e)}")
        finally:
            selection_win.destroy()

    def cargar_espana():
        try:
            graph = Cargar_Mapa_España()
            mostrar_mapa(graph, "Mapa Aéreo de España")
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar mapa: {str(e)}")
        finally:
            selection_win.destroy()

    def cargar_ecac():
        try:
            graph = Cargar_Mapa_ECAC()
            mostrar_mapa(graph, "Mapa Aéreo ECAC")
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar mapa: {str(e)}")
        finally:
            selection_win.destroy()

    # Función auxiliar para mostrar el mapa
    def mostrar_mapa(graph, title):
        if graph and graph.nodes:
            custom_graph.nodes = graph.nodes
            custom_graph.segments = graph.segments
            custom_graph.airport_nodes = getattr(graph, 'airport_nodes', set())
            fig = Plot(custom_graph, title=title, airport_nodes=custom_graph.airport_nodes)
            embed_plot(fig)
        else:
            messagebox.showerror("Error", "No se pudo cargar el mapa seleccionado.")

    # Crear botones
    ttk.Button(selection_win, text="Catalunya", command=cargar_catalunya).pack(pady=10)
    ttk.Button(selection_win, text="España", command=cargar_espana).pack(pady=10)
    ttk.Button(selection_win, text="ECAC", command=cargar_ecac).pack(pady=10)

def Export_To_KML():
    if not hasattr(custom_graph, 'nodes') or not custom_graph.nodes:
        messagebox.showwarning("Advertencia", "No hay datos a exportar")
        return

    export_choice = messagebox.askquestion(
        "Opciones de exportación",
        "¿Exportar todo el grafo? (Si para todos los nodos, No para el camino actual)",
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
        if export_choice == 'yes':
            generar_camino_kml(custom_graph.nodes, filename)
            messagebox.showinfo(
                "Exito",
                f"Exportado {len(custom_graph.nodes)} nodos a:\n{filename}"
            )
        else:
            if hasattr(custom_graph, 'shortest_path') and custom_graph.shortest_path:
                generar_camino_kml(custom_graph.shortest_path.nodes, filename)
                messagebox.showinfo(
                    "Exito",
                    f"Exportado el camino ({len(custom_graph.shortest_path.nodes)} points) a:\n{filename}"
                )
            else:
                messagebox.showwarning(
                    "No hay ningun camino",
                    "Porfavor calcular un camino usando la funcion en la interfaz"
                )
                return

        if messagebox.askyesno(
                "Abrir en google earth",
                "¿Abrir el fichero en Google earth?"
        ):
            try:
                os.startfile(filename)
            except Exception as e:
                messagebox.showerror(
                    "Error",
                    f"No se pudo abrir en Google Earth:\n{str(e)}"
                )

    except Exception as e:
        messagebox.showerror(
            "Error exportación",
            f"Error durante exportación a KML:\n{str(e)}"
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


# --- UI Layouts ---

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
ttk.Button(camino_frame, text="Buscar", command=Encontrar_Camino_Mas_Corto).grid(row=2, column=0, columnspan=2)

# Exportar a KML
ttk.Button(frame, text="Exportar a KML", command=Exportar_a_KML).grid(row=2, column=1, pady=5)

ttk.Button(frame,
          text="Mostrar Navpoints Sobrevolar",
          command=Mostrar_Navpoints_Sobrevolar,
          style='Common.TButton').grid(row=9, column=0, pady=5)
boton = ttk.Button(window, text="Mostrar Imágenes del Grupo", command=Mostrar_Imagenes)
boton.grid(row=1, column=0, padx=20, pady=20)

#Abrir mapas esp,cat,ecac
ttk.Button(example_frame, text="Mapas Aéreos", command=Mostrar_Mapa_Aereo).grid(row=0, column=3, padx=5)

def cerrar_programa():
    window.destroy()

window.protocol("WM_DELETE_WINDOW", cerrar_programa)

window.mainloop()