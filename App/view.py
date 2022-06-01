"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
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
import sys
import controller
from DISClib.ADT import list as lt
assert cf


"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

def printMenu():
    """
    Funcion encargada de hacer mostrar en la consola las opciones del menu
    """       
    print("Bienvenido")
    print("1- Comprar bicicletas para las estaciones con mas viajes de origen - Requerimiento 1")
    print("2- Planear paseos turisticos por la ciudad - Requerimiento 2")
    print("3- Reconocer los componentes fuertemente conectados - Requerimiento 3")
    print("4- Planear una ruta rapida para el usuario - Requerimiento 4")
    print("5- Reportar rutas en un rango de fechas para los usuarios anuales - Requerimiento 5")
    print("6- Planear el mantenimiento preventivo de bicicletas - Requerimiento 6")
    print("7- La estacion mas frecuentada por los visitantes - Requerimiento 7")
    print("8- Cargar información en el catálogo")



"""
 - (งツ)ว - (งツ)ว - (งツ)ว - (งツ)ว - (งツ)ว - (งツ)ว - (งツ)ว - (งツ)ว - (งツ)ว -

        Funciones para mostrar en la consola los datos solicitados

 - (งツ)ว - (งツ)ว - (งツ)ว - (งツ)ว - (งツ)ว - (งツ)ว - (งツ)ว - (งツ)ว - (งツ)ว -
"""



catalog = None

"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    
    # Condicional para seleccionar la opcion 1 (Comprar bicicletas para las estaciones con mas viajes de origen)
    if int(inputs[0]) == 1:
        controller.requerimiento_1(catalog)

    # Condicional para seleccionar la opcion 2 (Planear paseos turisticos por la ciudad)
    elif int(inputs[0]) == 2:
        estacion_origen = input("Ingrese el nombre de la estacion de la cual quiere partir: ")
        estacion_origen = "7543-Nassau St / Bellevue Ave"
        maxDuration = int(input("Ingrese cual es el maximo de tiempo del recorrido: "))
        numMinStopsStations = int(input("Ingrese la cantidad de estaciones que quiere visitar: "))
        maxStations = int(input("Ingrese el maximo de paradas que quiere hacer: "))
        controller.requerimiento_2(catalog, estacion_origen, maxDuration, numMinStopsStations, maxStations)

    # Condicional para seleccionar la opcion 3 (Reconocer los componentes fuertemente conectados)
    elif int(inputs[0]) == 3:
        pass
    
    # Condicional para seleccionar la opcion 4 (Planear una ruta rapida para el usuario) 
    elif int(inputs[0]) == 4:
        estacion_origen = input("Desde donde deseas que salga el usuario: ")
        estacion_destino = input("A donde desea llegar el usuario: ")

        controller.grafo_dijsktra(catalog, estacion_origen)
        tiene = controller.hasPath(catalog, estacion_destino)
        print(tiene)

    # Condicional para seleccionar la opcion 5 (Reportar rutas en un rango de fechas para los usuarios anuales)
    elif int(inputs[0]) == 5:
        pass

    # Condicional para seleccionar la opcion 6 (Planear el mantenimiento preventivo de bicicletas)
    elif int(inputs[0]) == 6:
        pass

    # Condicional para seleccionar la opcion 7 (La estacion mas frecuentada por los visitantes)
    elif int(inputs[0]) == 7:
        pass

    # Condicional para seleccionar la opcion 8 (Cargar información en el catálogo)
    elif int(inputs[0]) == 8:
        # avance carga datos
        import time
        print("Cargando información de los archivos ....")
        catalog = controller.init()

        start_time = time.time()
        catalog = controller.loadRoutes(catalog, "Bikeshare-ridership-2021-utf8-small.csv")
        print("--- %s seconds ---" % (time.time() - start_time))
        from DISClib.ADT import graph as gr
        print(f"Num vertices:{gr.numVertices(catalog['grafo'])}")
        print(f"Num edges:{gr.numEdges(catalog['grafo'])}")
        


    else:
        sys.exit(0)
sys.exit(0)
