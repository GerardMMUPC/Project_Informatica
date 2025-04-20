#Step 5 - Graphical interface that:
 #Shows example graph in step 3
 #Shows invented graph in step 3
 #Select file with graph with decided on format in step 3 and show
 #Select node in graph to show its neighbors

#We first define the window for the interface:
#Initial conditions:
from tkinter import *
from tkinter import ttk #More modern look to tkinter
from tkinter import filedialog
import matplotlib.pyplot as plt

window = Tk() #Gives me blank window
frame = ttk.Frame(window) #Frame: Grouping code tool
frame.grid() #We will group as a grid (on window)

graph = None

#Assign functions to each button:
def Show_Example_Graph():
    from test_graph import CreateGraph_1
    from Graph import Plot, PlotNode
    G1 = CreateGraph_1()
    Plot(G1, title=  "Node and segment graph/Gráfico con nodos y segmentos")

def Show_Invented_Graph():
    from test_graph import CreateGraph_2
    from Graph import Plot, PlotNode
    G2 = CreateGraph_2()
    Plot(G2, title = "USA's air routes map/Mapa de rutas aéreas de EE. UU.")

def Select_Graph_File(): #CHECK
    global graph #So it can be used by ther functions

    # Using a file picker
    filename = filedialog.askopenfilename(
        title = "Select a graph file",
        filetypes = [("Text Files", "*.txt")]
    )
    if not filename:
        return #Cancelled operation

    #Now, using a graph-maker function we read and input the values for given file:
    from Graph import FileGraph
    print("Reading file...")
    graph = FileGraph(filename)
    if not graph:
        print("The graph is empty or the file format is incorrect.")
        return

    print("Graph loaded successfully!")
    Plot(graph)

def Neighbors_to_Node(): #CHECK
    if graph is None:
        print("No graph loaded.")
        return

    node = node_entry.get()

    if node not in graph:
        print(f"Node {node} not found in the graph.")

    neighbours = graph[node]

    from Graph import Plot
    Plot(graph, title="Graph with Node and Neighbors")

    # Now highlight the node and its neighbors
    from Graph import PlotNode
    PlotNode(graph, node, neighbors, title = f"Graph with Node {node} and Neighbors Highlighted")

#Add text and buttons to the window:
title = ttk.Label(frame, text = "Welcome!", font = ("Verdana", 20))
title.grid(column = 0, row = 0)

subtitle = ttk.Label(frame, text = "This is the program made by group 14", font = ("Verdana", 10))
subtitle.grid(column = 0, row = 1)

text1 = ttk.Label(frame, text = "Example graph of step 3", font = ("Verdana", 12))
text1.grid(column = 0, row = 2)
ttk.Button(frame, text = "Show", command = Show_Example_Graph).grid(column = 1, row = 2)

text2 = ttk.Label(frame, text = "Invented graph of step 3", font = ("Verdana", 12))
text2.grid(column = 0, row = 3)
ttk.Button(frame, text = "Show", command = Show_Invented_Graph).grid(column = 1, row = 3)

text3 = ttk.Label(frame, text = "Select graph file to show", font = ("Verdana", 12))
text3.grid(column = 0, row = 4)
ttk.Button(frame, text = "Select", command = Select_Graph_File).grid(column = 1, row = 4)

text4 = ttk.Label(frame, text = "Select node in graph", font = ("Verdana", 12))
text4.grid(column = 0, row = 5)
node_entry = ttk.Entry(frame)
node_entry.grid(column = 1, row = 5)
ttk.Button(frame, text="Show Neighbors", command=Neighbors_to_Node).grid(column=2, row=5)

ttk.Button(frame, text = "Exit", command = window.destroy).grid(column = 0, row = 6)

window.mainloop() #Keeps window open
#Notes:
 #To make graph first summon "from tkinter import *" and import ttk for more modern
 #Tk(): Tkinter gives a blank window to work with.
 #ttk.Frame(): Groups code and displays it in a certain way
 #frame.grid(): Displays grouped code following a grid placement
 #ttk.Label(): Displays text (customizable)
 #"something".grid(): Lets you position something on window
 #ttk.Button(): Creates a button (customizable) that can follow a command when pressed.