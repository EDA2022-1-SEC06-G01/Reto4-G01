from re import L
import config as cf
from DISClib.ADT import graph as gr
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
from DISClib.Algorithms.Graphs import dfs
from DISClib.Algorithms.Graphs import bfs
from DISClib.Algorithms.Graphs import dijsktra
from DISClib.Algorithms.Graphs import scc
from DISClib.ADT import orderedmap as om
from DISClib.Utils import error as error
assert cf

catalog = {}

def searchPaths(catalog, initialVertex):
    path = dfs.DepthFirstSearch(catalog['grafo'], initialVertex)
    catalog['posibles_caminos'] = path
    return catalog

def posibles_rutas_de_viaje(catalog, initialVertex):
    paths = searchPaths(catalog, initialVertex)
    print(paths)
    input("jeje")
    stations = mp.keySet(paths)
    print(stations)
    return

def estacion_mas_viajes_origen(catalog):

    grafo = catalog['grafo']
    num_est = gr.numVertices(grafo)
    list_vert = gr.vertices(grafo)

    #for i in range(num_est):
    vertice = list_vert[0]
    print(gr.degree(vertice))
    return


catalog['grafo'] = gr.newGraph()
graph = catalog['grafo']
gr.insertVertex(graph, 'a')
gr.insertVertex(graph, 'b')
gr.insertVertex(graph, 'c')

gr.addEdge(graph, 'a', 'b', 1)
gr.addEdge(graph, 'b', 'c', 1)
gr.addEdge(graph, 'c', 'a', 1)


print(posibles_rutas_de_viaje(catalog, 'a'))

