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
 """

from gettext import Catalog
import config as cf
import model
import csv
import timeit
from DISClib.ADT import map as mp
import datetime

from DISClib.ADT import orderedmap as om
from DISClib.ADT import list as lt
from DISClib.Algorithms.Sorting import shellsort as sa
from DISClib.ADT import graph as gr
from DISClib.DataStructures import mapentry as me




import sys
sys.setrecursionlimit(10000000)


def init():
    """
    Llama la funcion de inicializacion  del modelo.
    """
    # analyzer es utilizado para interactuar con el modelo
    catalog = model.newCatalog()
    return catalog


def loadRoutes(catalog, routesFile):
    """
    Carga los datos de los archivos CSV en el modelo.
    Se crea un arco entre cada par de estaciones que
    pertenecen al mismo servicio y van en el mismo sentido.
    addRouteConnection crea conexiones entre diferentes rutas
    servidas en una misma estación.
    """
    routesFile = cf.data_dir + routesFile
    input_file = csv.DictReader(open(routesFile, encoding="utf-8"),
                                delimiter=",")
    fila_incorrecta = 0
    contador = 0
    for ruta in input_file:
        contador += 1
        if ruta["Bike Id"] == "" \
            or int(ruta["Trip  Duration"]) <= 0 \
            or ruta["Trip  Duration"] == "" \
            or ruta["Start Station Id"] == "" \
            or ruta["End Station Id"] == "" \
            or ruta["Start Station Name"] == ruta["End Station Name"]:
            fila_incorrecta += 1 
            continue
        else:
            ruta['Start Time Parcial'] = datetime.datetime.strptime(ruta['Start Time'][0:10], '%m/%d/%Y')
            ruta['End Time Parcial'] = datetime.datetime.strptime(ruta['End Time'][0:10], '%m/%d/%Y')
            ruta['Start Time'] = datetime.datetime.strptime(ruta['Start Time'], '%m/%d/%Y %H:%M')
            ruta['End Time'] = datetime.datetime.strptime(ruta['End Time'], '%m/%d/%Y %H:%M')
            model.Viaje(catalog, ruta)
    model.Viaje.aniadir_conexiones(catalog)
    catalog["filas_incorrectas"] = fila_incorrecta

    catalog["respuesta_req3"] = model.grafo_scc(catalog)


    
    # sa.sort(model.Estacion.top_estacionesSalida, model.cmpGeneral)
    # print(lt.getElement(model.Estacion.top_estacionesSalida, 1))

    model.grafo_scc(catalog)

    
    
    return catalog
    

"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

def grafo_dijsktra(catalog, vertice_inicial):
    return model.grafo_dijsktra(catalog, vertice_inicial)

def hasPath(catalog, station_to_reach):
    return model.hasPath(catalog, station_to_reach)

def findPath(catalog, station_to_reach):
    return model.findPath(catalog, station_to_reach)

def requerimiento1():
    pass

def requerimiento3(catalog):
    return catalog["respuesta_req3"]

def requerimiento5(catalog, fecha_inicial, fecha_final):
    model.Viaje.respuesta_req5(catalog, fecha_inicial, fecha_final)

# Inicialización del Catálogo de libros

# Funciones para la carga de datos

# Funciones de ordenamiento

# Funciones de consulta sobre el catálogo

def requerimiento_1(catalog):
    return model.estacion_mas_viajes_origen(catalog)

def requerimiento_2(catalog, initialVertex, maxDuration, numMinStopStations, maxStations):
    return model.posibles_rutas_de_viaje(catalog, initialVertex, maxDuration, numMinStopStations, maxStations)