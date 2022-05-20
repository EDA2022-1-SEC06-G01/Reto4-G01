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

import config as cf
import model
import csv
import timeit


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
    for ruta in input_file:
        if ruta["Trip Id"] == "" or ruta["Trip  Duration"] == 0 or ruta["Start Station Id"] == "" or ruta["Start Time"] == "" or ruta["Start Station Name"] == "" or ruta["End Station Id"] == "" or ruta["End Time"] == "" or ruta["End Station Name"] == "" or ruta["Bike Id"] == "" or ruta["User Type"] == "":
            fila_incorrecta += 1
        else:
            model.aniadir_nueva_ruta(catalog, ruta)
    model.aniadir_conexiones(catalog)
    catalog["filas_incorrectas"] = fila_incorrecta

    #model.grafo_scc(catalog)
    
    return catalog
    

"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

# Inicialización del Catálogo de libros

# Funciones para la carga de datos

# Funciones de ordenamiento

# Funciones de consulta sobre el catálogo
