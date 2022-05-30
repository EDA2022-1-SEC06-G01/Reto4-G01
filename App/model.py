"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


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

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos

def newCatalog():
    """ Inicializa el analizador
   stops: Tabla de hash para guardar los vertices del grafo
   connections: Grafo para representar las rutas entre estaciones
   components: Almacena la informacion de los componentes conectados
   paths: Estructura que almancena los caminos de costo minimo desde un
           vertice determinado a todos los otros vértices del grafo
    """
    try:
        catalog = {
            'grafo': None,
            'grafo_scc': None,
            'maxValue_stationInComponent': None,
            'peso_arcos': None,
            'grafo_dijsktra': None
        }

        catalog['estaciones'] = mp.newMap(numelements=14000, maptype='PROBING', loadfactor=0.5)        

        catalog['nombreEstaciones_nombreFormateados'] = mp.newMap(numelements=14000, maptype='PROBING', loadfactor=0.5)   

        catalog['grafo'] = gr.newGraph(datastructure='ADJ_LIST',
                                              directed=True,
                                              size=14000,
                                              comparefunction=compareStopIds)

        return catalog
    except Exception as exp:
        error.reraise(exp, 'model:newCatalog')


def aniadir_nueva_ruta(catalog, route):
    mapa_estaciones = catalog['estaciones']
    grafo = catalog['grafo']
    nombreEstaciones_nombreFormateados = catalog['nombreEstaciones_nombreFormateados']

    nombre_estacionSalida = route['Start Station Name']
    id_estacionSalida = route["Start Station Id"]
    nombreFormateado_estacionSalida = f"{id_estacionSalida}-{'UNKNOWN' if nombre_estacionSalida == '' else nombre_estacionSalida}"

    nombre_estacionLlegada = route['End Station Name']
    id_estacionLlegada = route["End Station Id"][:-2]
    nombreFormateado_estacionLlegada = f"{id_estacionLlegada}-{'UNKNOWN' if nombre_estacionLlegada == '' else nombre_estacionLlegada}"
    
    peso = route["Trip  Duration"]
    
    aniadirNombreEstacion_estacionFormateada(nombreEstaciones_nombreFormateados, nombre_estacionSalida, nombreFormateado_estacionSalida)
    salida(grafo, mapa_estaciones, nombreFormateado_estacionSalida, nombre_estacionSalida, id_estacionSalida, nombreFormateado_estacionLlegada, peso)

    aniadirNombreEstacion_estacionFormateada(nombreEstaciones_nombreFormateados, nombre_estacionLlegada, nombreFormateado_estacionLlegada)
    llegada(grafo, mapa_estaciones, nombreFormateado_estacionLlegada, nombre_estacionLlegada, id_estacionLlegada)
    

def salida(grafo, mapa_estaciones, nombreFormateado_estacionSalida, nombre_estacionSalida, id_estacionSalida, nombreFormateado_estacionLlegada, peso):
    contiene_llave = mp.contains(mapa_estaciones, nombreFormateado_estacionSalida)

    if contiene_llave:
        estacion = me.getValue(mp.get(mapa_estaciones, nombreFormateado_estacionSalida))
        estacion.aniadir_salida(nombreFormateado_estacionLlegada, peso)
    else:
        estacion = Estacion(nombreFormateado_estacionSalida, nombre_estacionSalida, id_estacionSalida)
        estacion.aniadir_salida(nombreFormateado_estacionLlegada, peso)
        mp.put(mapa_estaciones, nombreFormateado_estacionSalida, estacion)
        gr.insertVertex(grafo, nombreFormateado_estacionSalida)


def llegada(grafo, mapa_estaciones, nombreFormateado_estacionLlegada, nombre_estacionLlegada, id_estacionLlegada):
    contiene_llave = mp.contains(mapa_estaciones, nombreFormateado_estacionLlegada)

    if contiene_llave:
        estacion = me.getValue(mp.get(mapa_estaciones, nombreFormateado_estacionLlegada))
        estacion.aniadir_llegada()
    else:
        estacion = Estacion(nombreFormateado_estacionLlegada, nombre_estacionLlegada, id_estacionLlegada)
        estacion.aniadir_llegada()
        mp.put(mapa_estaciones, nombreFormateado_estacionLlegada, estacion)
        gr.insertVertex(grafo, nombreFormateado_estacionLlegada)


def aniadir_conexiones(catalog):
    mapa_estaciones = catalog['estaciones']
    grafo = catalog['grafo']

    nombre_estaciones = mp.keySet(mapa_estaciones)
    for estacion in lt.iterator(nombre_estaciones):
        valor = me.getValue(mp.get(mapa_estaciones, estacion))
        arcos = valor.arcos
        nombre_estacionesSalida = mp.keySet(arcos)
        for estacionSalida in lt.iterator(nombre_estacionesSalida):
            lst_peso = me.getValue(mp.get(arcos, estacionSalida))
            gr.addEdge(grafo, estacion, estacionSalida, lt.getElement(lst_peso, 2) / lt.getElement(lst_peso, 1))


def aniadirNombreEstacion_estacionFormateada(mapa, nombre_estacion, nombreFormateado_estacion):
    existe = mp.contains(mapa, nombre_estacion)
    if existe:
        lst = me.getValue(mp.get(mapa, nombre_estacion))
        existe = lt.isPresent(lst, nombreFormateado_estacion)
        if not existe:
            lt.addLast(lst, nombreFormateado_estacion)
    else:
        lst = lt.newList()
        mp.put(mapa, nombre_estacion, lst)
        lt.addLast(lst, nombreFormateado_estacion)

def grafo_scc(catalog):
    grafo = catalog["grafo"]
    catalog["grafo_scc"] = scc.KosarajuSCC(grafo)
    scc_ = catalog["grafo_scc"]

    # print(scc.connectedComponents(scc_))
    # print("propos")
    # value = scc.sccCount(grafo, scc_, "Nassau St / Bellevue Ave")['idscc']
    # print(value)
    # print()
    # print()
    # print(mp.keySet(value))
    # print()
    # print()
    # print()
    # print(mp.valueSet(value))


def max_scc(catalog):
    value = catalog["grafo_scc"]
    keys = mp.keySet(value)
    values = mp.valueSet(value)
    maximums = mp.newMap(numelements=14000, maptype='PROBING', loadfactor=0.5)
    for value in range(1, lt.size(values) + 1):
        existe = mp.contains(maximums, value)
        if existe:
            pass
        else:
            pass

def grafo_dijsktra(catalog, vertice_inicial):
    grafo = catalog["grafo"]
    catalog["grafo_dijsktra"] = dijsktra.Dijkstra(grafo, vertice_inicial)

def hasPath(catalog, station_to_reach):
    search = catalog["grafo_dijsktra"]
    return dijsktra.hasPathTo(search, station_to_reach)

def findPath(catalog, station_to_reach):
    search = catalog["grafo_dijsktra"]
    return dijsktra.pathTo(search, station_to_reach)



# Funciones para agregar informacion al catalogo

# Funciones para creacion de datos

# Funciones de consulta

def searchPaths(catalog, initialVertex):
    path = dfs.DepthFirstSearch(catalog['grafo'], initialVertex)
    catalog['posibles_caminos'] = path
    return catalog

def posibles_rutas_de_viaje(catalog, initialVertex, maxDuration, numMinStopStations, maxStations):
    paths = searchPaths(catalog, initialVertex)
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

# Funciones utilizadas para comparar elementos dentro de una lista

# Funciones de ordenamiento


def compareStopIds(stop, keyvaluestop):
    """
    Compara dos estaciones
    """
    stopcode = keyvaluestop['key']
    if (stop == stopcode):
        return 0
    elif (stop > stopcode):
        return 1
    else:
        return -1



# Modelos de los objetos 

class Estacion:

    cantidad_estaciones = 0

    def __init__(self, nombre_formateado, nombre, id_estacion) -> None:
        self.nombre = nombre
        self.nombre_formatedo = nombre_formateado
        self.id_estacion = id_estacion
        self.estacion_salida = 0
        self.estacion_llegada = 0
        self.arcos = mp.newMap(numelements=5, maptype='PROBING', loadfactor=0.5)

        Estacion.cantidad_estaciones += 1
    
    def aniadir_llegada(self) -> None:
        self.estacion_llegada += 1
    
    def aniadir_salida(self, estacion_salida, peso_de_estacion):
        peso_de_estacion = float(peso_de_estacion)
        self.estacion_salida += 1
        mapa = self.arcos

        existe_estacion = mp.contains(mapa, estacion_salida)

        if existe_estacion:
            peso = mp.get(mapa, estacion_salida)
            lst_peso = me.getValue(peso)
            cantidad_elementos = lt.getElement(lst_peso, 1)
            peso = lt.getElement(lst_peso, 2)

            lt.changeInfo(lst_peso, 1, cantidad_elementos + 1)
            lt.changeInfo(lst_peso, 2, peso + peso_de_estacion)

        else:
            lst = lt.newList(datastructure="ARRAY_LIST")
            lt.addLast(lst, 1)
            lt.addLast(lst, peso_de_estacion)
            mp.put(mapa, estacion_salida, lst)
# cambiar sumatroria de pesos por una lista con los elementos que vaya encontrando

class Bicicleta:
    def __init__(self) -> None:
        pass

# los que llegan asi mismo y los que no tienen duracion (o los que tienen duracion 0)