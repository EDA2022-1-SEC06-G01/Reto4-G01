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
import datetime



import sys
sys.setrecursionlimit(10000000)



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
            'grafo_dijsktra': None,
            'componentesFuertementeConectados': None,
        }

        catalog['estaciones'] = mp.newMap(numelements=14000, maptype='PROBING', loadfactor=0.5)        

        catalog['nombreEstaciones_nombreFormateados'] = mp.newMap(numelements=14000, maptype='PROBING', loadfactor=0.5)   

        catalog['idBicicleta_objetoBicicleta'] = mp.newMap(numelements=14000, maptype='PROBING', loadfactor=0.5)   

        catalog['grafo'] = gr.newGraph(datastructure='ADJ_LIST',
                                              directed=True,
                                              size=14000,
                                              comparefunction=compareStopIds)
        catalog["componentesFuertementeConectados"] = lt.newList(datastructure='ARRAY_LIST')

        catalog["arbolFechas_viajes_usuariosAnuales"] = om.newMap(comparefunction=compare_generalArboles)

        catalog["respuesta_req3"] = None


        return catalog
    except Exception as exp:
        error.reraise(exp, 'model:newCatalog')


def grafo_scc(catalog):
    grafo = catalog["grafo"]
    lst_componentes = catalog["componentesFuertementeConectados"]
    catalog["grafo_scc"] = scc.KosarajuSCC(grafo)
    scc_ = catalog["grafo_scc"]

    numero_de_componentesFuertementementeConectados = scc.connectedComponents(scc_)
    value = scc.sccCount(grafo, scc_, "7543-Nassau St / Bellevue Ave")['idscc']

    estacion = mp.keySet(value)
    componente = mp.valueSet(value)
    cantidad = lt.size(estacion)

    for _ in range(1, numero_de_componentesFuertementementeConectados + 1):
        lst = lt.newList(datastructure='ARRAY_LIST')
        lt.addLast(lst, _)
        lt.addLast(lst_componentes, lst)
    

    for _ in range(1, cantidad + 1):
        estation = lt.getElement(estacion, _)
        comp = lt.getElement(componente, _)
        lst_actual = lt.getElement(lst_componentes, comp)
        lt.addLast(lst_actual, estation)

    lst_componentes = sa.sort(lst_componentes, cmpGeneral2)

    firstThree = lt.subList(lst_componentes, 1, 3)
    lastThree = lt.subList(lst_componentes, numero_de_componentesFuertementementeConectados - 2, 3)
    respuesta = formatear_respuesta_req3(catalog, firstThree, lastThree)
    return respuesta

def formatear_respuesta_req3(catalog, firstThree, lastThree):
    lst_respuesta = lt.newList(datastructure='ARRAY_LIST')
    for _ in lt.iterator(firstThree):
        size = lt.size(_) - 1
        lst_respuestaActual = lt.newList(datastructure='ARRAY_LIST')
        lt.addLast(lst_respuestaActual, lt.getElement(_, 1))
        lt.addLast(lst_respuestaActual, size)
        resSalidas = mayorCantidad_salidas(catalog, _)
        resLlegadas = mayorCantidad_llegadas(catalog, _)
        lt.addLast(lst_respuestaActual, resSalidas)
        lt.addLast(lst_respuestaActual, resLlegadas)
        lt.addLast(lst_respuesta, lst_respuestaActual)
    for _ in lt.iterator(lastThree):
        size = lt.size(_) - 1
        lst_respuestaActual = lt.newList(datastructure='ARRAY_LIST')
        lt.addLast(lst_respuestaActual, lt.getElement(_, 1))
        lt.addLast(lst_respuestaActual, size)
        resSalidas = mayorCantidad_salidas(catalog, _)
        resLlegadas = mayorCantidad_llegadas(catalog, _)
        lt.addLast(lst_respuestaActual, resSalidas)
        lt.addLast(lst_respuestaActual, resLlegadas)
        lt.addLast(lst_respuesta, lst_respuestaActual)
    return lst_respuesta

def mayorCantidad_salidas(catalog, lst):
    mapa_estaciones = catalog['estaciones']
    
    max = -1
    estacion = None
    for element in lt.iterator(lst):
        if isinstance(element, int):
            continue
        object = me.getValue(mp.get(mapa_estaciones, element))
        salidas = object.estacion_salida
        if salidas > max:
            max = salidas
            estacion = object
    return estacion

def mayorCantidad_llegadas(catalog, lst):
    mapa_estaciones = catalog['estaciones']
    
    max = -1
    estacion = None
    for element in lt.iterator(lst):
        if isinstance(element, int):
            continue
        object = me.getValue(mp.get(mapa_estaciones, element))
        llegadas = object.estacion_llegada
        if llegadas > max:
            max = llegadas
            estacion = object
    return estacion



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

def posibles_rutas_de_viaje(catalog, initialVertex, maxDuration, numMinStopStations, maxStations):

    dijsktra = grafo_dijsktra(catalog, initialVertex)
    visited = dijsktra["grafo_dijsktra"]["visited"]
    stations = mp.keySet(visited)
    routes = lt.newList('ARRAY_LIST')
    print(visited)
    print(stations)

    for i in lt.iterator(stations):
        path = findPath(catalog["grafo_dijsktra"], i)
        print(path)

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

def cmpGeneral(val1, val2):
    val1 = lt.getElement(val1, 1)
    val2 = lt.getElement(val2, 1)
    return val1 > val2

def cmpGeneral2(val1, val2):
    val_1 = lt.size(val1)
    val_2 = lt.size(val2)
    val_ = lt.getElement(val1, 1)
    val2_ = lt.getElement(val2, 1)
    if val_1 == val_2:
        return val_ > val2_
    else:
        return val_1 > val_2

def cmpGeneral3(val1, val2):
    val1 = lt.getElement(val1, 2)
    val2 = lt.getElement(val2, 2)
    return val1 > val2

def compare_generalArboles(val1, val2):
    if (val1 == val2):
        return 0
    elif val1 > val2:
        return 1
    else:
        return -1

# Modelos de los objetos 

class Estacion:

    cantidad_estaciones = 0
    top_estacionesSalida = lt.newList(datastructure='ARRAY_LIST')

    def __init__(self, nombre_formateado, nombre, id_estacion) -> None:
        self.nombre = nombre
        self.nombre_formatedo = nombre_formateado
        self.id_estacion = id_estacion
        self.estacion_numSalida = lt.newList(datastructure='ARRAY_LIST')
        
        lt.addLast(self.estacion_numSalida, 0)
        lt.addLast(self.estacion_numSalida, self.nombre_formatedo)
        lt.addLast(Estacion.top_estacionesSalida, self.estacion_numSalida)

        self.estacion_llegada = 0
        self.estacion_salida = 0
        self.registro_hora = mp.newMap(numelements=29, maptype='PROBING', loadfactor=0.5)
        self.registro_anio = mp.newMap(numelements=29, maptype='PROBING', loadfactor=0.5)
        self.arcos = mp.newMap(numelements=5, maptype='PROBING', loadfactor=0.5)

        Estacion.cantidad_estaciones += 1
    
    def aniadir_llegada(self) -> None:
        self.estacion_llegada += 1
    
    def aniadir_salida(self, nombreFormateado_estacionLlegada, peso_de_estacion, hora):
        self.estacion_salida += 1
        self.registrar_hora(hora)
        peso_de_estacion = float(peso_de_estacion)
        
        mapa = self.arcos

        existe_estacion = mp.contains(mapa, nombreFormateado_estacionLlegada)

        val = lt.getElement(self.estacion_numSalida, 1)
        lt.changeInfo(self.estacion_numSalida, 1, val + 1)

        if existe_estacion:
            peso = mp.get(mapa, nombreFormateado_estacionLlegada)
            lst_peso = me.getValue(peso)
            cantidad_elementos = lt.getElement(lst_peso, 1)
            peso = lt.getElement(lst_peso, 2)

            lt.changeInfo(lst_peso, 1, cantidad_elementos + 1)
            lt.changeInfo(lst_peso, 2, peso + peso_de_estacion)

        else:
            lst = lt.newList(datastructure="ARRAY_LIST")
            lt.addLast(lst, 1)
            lt.addLast(lst, peso_de_estacion)
            mp.put(mapa, nombreFormateado_estacionLlegada, lst)
    
    def registrar_hora(self, datetime):
        mapa = self.registro_hora
        hour = datetime.hour
        existe = mp.contains(mapa, hour)
        if existe:
            val = me.getValue(mp.get(mapa, hour))
            mp.put(mapa, hour, val + 1)
        else:
            mp.put(mapa, hour, 1)
    
    def registrar_anio(self, datetime):
        mapa = self.registro_anio
        anio = datetime.year
        existe = mp.contains(mapa, anio)
        if existe:
            val = me.getValue(mp.get(mapa, anio))
            mp.put(mapa, anio, val + 1)
        else:
            mp.put(mapa, anio, 1)



class Bicicleta:
    total_bicicletas = 0
    def __init__(self, id) -> None:
        Bicicleta.total_bicicletas += 1
        self.id_bicicleta = id
        self.tiempo_de_uso_bicicleta = 0

        self.estaciones_iniciado = lt.newList(datastructure="ARRAY_LIST")
        self.estaciones_iniciadoMapa = mp.newMap(numelements=29, maptype='PROBING', loadfactor=0.5)
        self.estaciones_terminado = lt.newList(datastructure="ARRAY_LIST")
        self.estaciones_terminadoMapa = mp.newMap(numelements=29, maptype='PROBING', loadfactor=0.5)

    def anidir_uso(self, duracion):
        self.tiempo_de_uso_bicicleta += duracion
    
    def aniadir_estacionInicio(self, estacion):
        existe = mp.contains(self.estaciones_iniciadoMapa, estacion)
        if existe:
            lst = me.getValue(mp.get(self.estaciones_iniciadoMapa, estacion))
            val = lt.getElement(lst, 2)
            lt.changeInfo(lst, 2, val + 1)
        else:
            lst = lt.newList(datastructure="ARRAY_LIST")
            lt.addLast(lst, estacion)
            lt.addLast(lst, 1)
            lt.addLast(self.estaciones_iniciado, lst)
            mp.put(self.estaciones_iniciadoMapa, estacion, lst)
    
    def aniadir_estacionFinalizacion(self, estacion):
        existe = mp.contains(self.estaciones_terminadoMapa, estacion)
        if existe:
            lst = me.getValue(mp.get(self.estaciones_terminadoMapa, estacion))
            val = lt.getElement(lst, 2)
            lt.changeInfo(lst, 2, val + 1)
        else:
            lst = lt.newList(datastructure="ARRAY_LIST")
            lt.addLast(lst, estacion)
            lt.addLast(lst, 1)
            lt.addLast(self.estaciones_terminado, lst)
            mp.put(self.estaciones_terminadoMapa, estacion, lst)
    
    def sort(self):
        sa.sort(self.estaciones_iniciado, cmpGeneral3)
        sa.sort(self.estaciones_terminado, cmpGeneral3)






class Viaje:

    cantidad_viajes = 0
    

    def __init__(self, catalog, route) -> None:
        Viaje.cantidad_viajes += 1


        self.id_viaje = Viaje.cantidad_viajes
        self.nombre_estacionSalida = route['Start Station Name']
        self.id_estacionSalida = route["Start Station Id"]
        self.nombreFormateado_estacionSalida = self.formatear_nombre(self.id_estacionSalida, self.nombre_estacionSalida)

        self.nombre_estacionLlegada = route['End Station Name']
        self.id_estacionLlegada = route["End Station Id"].split('.')[0]
        self.nombreFormateado_estacionLlegada = self.formatear_nombre(self.id_estacionLlegada, self.nombre_estacionLlegada)

        self.peso = route["Trip  Duration"]

        
        if route["User Type"] == "Annual Member":
            self.aniadirFecha_arbol(catalog, route, self.nombreFormateado_estacionSalida, self.nombreFormateado_estacionLlegada)

        # Datos bicicleta
        id = route["Bike Id"]
        idBicicleta_objetoBicicleta = catalog['idBicicleta_objetoBicicleta']
        existe = mp.contains(idBicicleta_objetoBicicleta, id)
        if existe:
            bicicleta = me.getValue(mp.get(idBicicleta_objetoBicicleta, id))
            bicicleta.aniadir_estacionInicio(self.nombreFormateado_estacionSalida)
            bicicleta.aniadir_estacionFinalizacion(self.nombreFormateado_estacionLlegada)
        else:
            bicicleta = Bicicleta(id)
            bicicleta.aniadir_estacionInicio(self.nombreFormateado_estacionSalida)
            bicicleta.aniadir_estacionFinalizacion(self.nombreFormateado_estacionLlegada)
            mp.put(idBicicleta_objetoBicicleta, id, bicicleta)
        Bicicleta.sort


        mapa_estaciones = catalog['estaciones']
        nombreEstaciones_nombreFormateados = catalog['nombreEstaciones_nombreFormateados']
        grafo = catalog['grafo']
        fecha_salida = route["Start Time"]
        self.agregar_datosViaje(grafo, mapa_estaciones, self.nombreFormateado_estacionSalida, self.nombre_estacionSalida, self.id_estacionSalida, self.nombreFormateado_estacionLlegada, self.peso, nombreEstaciones_nombreFormateados, self.nombre_estacionLlegada, self.id_estacionLlegada, fecha_salida)
    
    def agregar_datosViaje(self,
                            grafo,
                            mapa_estaciones,
                            nombreFormateado_estacionSalida,
                            nombre_estacionSalida, id_estacionSalida,
                            nombreFormateado_estacionLlegada,
                            peso,
                            nombreEstaciones_nombreFormateados,
                            nombre_estacionLlegada,
                            id_estacionLlegada,
                            hora_salida):

        self.salida(grafo, mapa_estaciones, nombreFormateado_estacionSalida, nombre_estacionSalida, id_estacionSalida, nombreFormateado_estacionLlegada, peso, nombreEstaciones_nombreFormateados, hora_salida)
        self.llegada(grafo, mapa_estaciones, nombreFormateado_estacionLlegada, nombre_estacionLlegada, id_estacionLlegada, nombreEstaciones_nombreFormateados)
    
    def formatear_nombre(self, id, nombre) -> str:
        return f"{id}-{'UNKNOWN' if nombre == '' else nombre}"

    def salida(self, grafo, mapa_estaciones, nombreFormateado_estacionSalida, nombre_estacionSalida, id_estacionSalida, nombreFormateado_estacionLlegada, peso, nombreEstaciones_nombreFormateados, hora_salida):
        self.aniadirNombreEstacion_estacionFormateada(nombreEstaciones_nombreFormateados, nombre_estacionSalida, nombreFormateado_estacionSalida)
        contiene_llave = mp.contains(mapa_estaciones, nombreFormateado_estacionSalida)
    



        # CONTINUA REQUERIMIENTO 6
        if contiene_llave:
            estacion = me.getValue(mp.get(mapa_estaciones, nombreFormateado_estacionSalida))
            estacion.aniadir_salida(nombreFormateado_estacionLlegada, peso, hora_salida)
        else:
            estacion = Estacion(nombreFormateado_estacionSalida, nombre_estacionSalida, id_estacionSalida)
            estacion.aniadir_salida(nombreFormateado_estacionLlegada, peso, hora_salida)
            mp.put(mapa_estaciones, nombreFormateado_estacionSalida, estacion)
            gr.insertVertex(grafo, nombreFormateado_estacionSalida)


    def llegada(self, grafo, mapa_estaciones, nombreFormateado_estacionLlegada, nombre_estacionLlegada, id_estacionLlegada, nombreEstaciones_nombreFormateados):
        self.aniadirNombreEstacion_estacionFormateada(nombreEstaciones_nombreFormateados, nombre_estacionLlegada, nombreFormateado_estacionLlegada)
        contiene_llave = mp.contains(mapa_estaciones, nombreFormateado_estacionLlegada)

        if contiene_llave:
            estacion = me.getValue(mp.get(mapa_estaciones, nombreFormateado_estacionLlegada))
            estacion.aniadir_llegada()
        else:
            estacion = Estacion(nombreFormateado_estacionLlegada, nombre_estacionLlegada, id_estacionLlegada)
            estacion.aniadir_llegada()
            mp.put(mapa_estaciones, nombreFormateado_estacionLlegada, estacion)
            gr.insertVertex(grafo, nombreFormateado_estacionLlegada)
        
    def aniadirNombreEstacion_estacionFormateada(self, mapa, nombre_estacion, nombreFormateado_estacion):
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
    
    
    def aniadirFecha_arbol(self, catalog, route, nombreFormateado_estacionSalida, nombreFormateado_estacionLlegada):
        arbol = catalog["arbolFechas_viajes_usuariosAnuales"]
        fecha1 = route["Start Time"]
        fecha2 = route["End Time"]
        fechaParcial1 = route["Start Time Parcial"]
        fechaParcial2 = route["End Time Parcial"]
        
        existe1 = om.contains(arbol, fechaParcial1)
        existe2 = om.contains(arbol, fechaParcial2)

        tiempo_viaje = int(route["Trip  Duration"])
        dia1 = fecha1.day
        dia2 = fecha2.day
        hora1 = int(fecha1.hour)
        hora2 = int(fecha2.hour)
        
        if dia1 == dia2:
            if existe1:
                lst = me.getValue(om.get(arbol, fechaParcial1))
                mapa_estacionOrigen = lt.getElement(lst, 3)
                mapa_estacionDestino = lt.getElement(lst, 4)
                mapa_horasOrigen= lt.getElement(lst, 5)
                mapa_horasDestino= lt.getElement(lst, 6)
                
                val_totalViajes = lt.getElement(lst, 1)
                val_totalTiempoViaje = lt.getElement(lst, 2)
                
                try:
                    veces_estacionOrigen = me.getValue(mp.get(mapa_estacionOrigen, nombreFormateado_estacionSalida))
                    mp.put(mapa_estacionOrigen, nombreFormateado_estacionSalida, veces_estacionOrigen + 1)
                except:
                    mp.put(mapa_estacionOrigen, nombreFormateado_estacionSalida, 1)
                
                try:
                    veces_estacionDestino = me.getValue(mp.get(mapa_estacionDestino, nombreFormateado_estacionLlegada))
                    mp.put(mapa_estacionDestino, nombreFormateado_estacionLlegada, veces_estacionDestino + 1)
                except:
                    mp.put(mapa_estacionDestino, nombreFormateado_estacionLlegada, 1)

                veces_horaOrigen = me.getValue(mp.get(mapa_horasOrigen, hora1))
                veces_horaDestino = me.getValue(mp.get(mapa_horasDestino, hora2))


                mp.put(mapa_horasOrigen, hora1, veces_horaOrigen + 1)
                mp.put(mapa_horasDestino, hora2, veces_horaDestino + 1)

                lt.changeInfo(lst, 1, val_totalViajes + 1)
                lt.changeInfo(lst, 2, val_totalTiempoViaje + tiempo_viaje)
                lt.changeInfo(lst, 3, mapa_estacionOrigen)
                lt.changeInfo(lst, 4, mapa_estacionDestino)
                lt.changeInfo(lst, 5, mapa_horasOrigen)
                lt.changeInfo(lst, 6, mapa_horasDestino)
                om.put(arbol, fechaParcial1, lst)
            else:
                lst = lt.newList(datastructure='ARRAY_LIST')
                mapa_estacionOrigen = mp.newMap()
                mapa_estacionDestino = mp.newMap()
                mapa_horasOrigen= mp.newMap()
                mapa_horasDestino= mp.newMap()
                mp.put(mapa_estacionOrigen, nombreFormateado_estacionSalida, 1)
                mp.put(mapa_estacionDestino, nombreFormateado_estacionLlegada, 1)
                for _ in range(24):
                    mp.put(mapa_horasOrigen, _, 0)
                    mp.put(mapa_horasDestino, _, 0)
                mp.put(mapa_horasOrigen, hora1, 1)
                mp.put(mapa_horasDestino, hora2, 1)
                lt.addLast(lst, 1)
                lt.addLast(lst, tiempo_viaje)
                lt.addLast(lst, mapa_estacionOrigen)
                lt.addLast(lst, mapa_estacionDestino)
                lt.addLast(lst, mapa_horasOrigen)
                lt.addLast(lst, mapa_horasDestino)
                om.put(arbol, fechaParcial1, lst)

        else:
            if existe1:
                lst = me.getValue(om.get(arbol, fechaParcial1))
                mapa_estacionOrigen = lt.getElement(lst, 3)
                mapa_horasOrigen= lt.getElement(lst, 5)
                val_totalViajes = lt.getElement(lst, 1)
                val_totalTiempoViaje = lt.getElement(lst, 2)
                lt.changeInfo(lst, 1, val_totalViajes + 1)
                lt.changeInfo(lst, 2, val_totalTiempoViaje + tiempo_viaje)
                
                try:
                    veces_estacionOrigen = me.getValue(mp.get(mapa_estacionOrigen, nombreFormateado_estacionSalida))
                    mp.put(mapa_estacionOrigen, nombreFormateado_estacionSalida, veces_estacionOrigen + 1)
                except:
                    mp.put(mapa_estacionOrigen, nombreFormateado_estacionSalida, 1)

                veces_horaOrigen = me.getValue(mp.get(mapa_horasOrigen, hora1))
                mp.put(mapa_horasOrigen, hora1, veces_horaOrigen + 1)

                lt.changeInfo(lst, 1, val_totalViajes + 1)
                lt.changeInfo(lst, 2, val_totalTiempoViaje + tiempo_viaje)
                lt.changeInfo(lst, 3, mapa_estacionOrigen)
                lt.changeInfo(lst, 5, mapa_horasOrigen)
                om.put(arbol, fechaParcial1, lst)                

            else:
                lst = lt.newList(datastructure='ARRAY_LIST')
                mapa_estacionOrigen = mp.newMap()
                mapa_estacionDestino = mp.newMap()
                mapa_horasOrigen= mp.newMap()
                mapa_horasDestino= mp.newMap()
                mp.put(mapa_estacionOrigen, nombreFormateado_estacionSalida, 1)
                for _ in range(24):
                    mp.put(mapa_horasOrigen, _, 0)
                    mp.put(mapa_horasDestino, _, 0)
                mp.put(mapa_horasOrigen, hora1, 1)
                lt.addLast(lst, 1)
                lt.addLast(lst, tiempo_viaje)
                lt.addLast(lst, mapa_estacionOrigen)
                lt.addLast(lst, mapa_estacionDestino)
                lt.addLast(lst, mapa_horasOrigen)
                lt.addLast(lst, mapa_horasDestino)
                om.put(arbol, fechaParcial1, lst)

            if existe2:
                lst = me.getValue(om.get(arbol, fechaParcial2))
                val_totalViajes = lt.getElement(lst, 1)
                val_totalTiempoViaje = lt.getElement(lst, 2)
                mapa_estacionDestino = lt.getElement(lst, 4)
                mapa_horasDestino= lt.getElement(lst, 6)

                

                try:
                    veces_estacionDestino = me.getValue(mp.get(mapa_estacionDestino, nombreFormateado_estacionLlegada))
                    mp.put(mapa_estacionDestino, nombreFormateado_estacionLlegada, veces_estacionDestino + 1)
                except:
                    mp.put(mapa_estacionDestino, nombreFormateado_estacionLlegada, 1)
                
                veces_horaDestino = me.getValue(mp.get(mapa_horasDestino, hora2))
                mp.put(mapa_horasDestino, hora2, veces_horaDestino + 1)

                lt.changeInfo(lst, 1, val_totalViajes + 1)
                lt.changeInfo(lst, 2, val_totalTiempoViaje + tiempo_viaje)
                lt.changeInfo(lst, 4, mapa_estacionDestino)
                lt.changeInfo(lst, 6, mapa_horasDestino)
                om.put(arbol, fechaParcial2, lst)
            else:
                lst = lt.newList(datastructure='ARRAY_LIST')
                mapa_estacionOrigen = mp.newMap()
                mapa_estacionDestino = mp.newMap()
                mapa_horasOrigen= mp.newMap()
                mapa_horasDestino= mp.newMap()
                mp.put(mapa_estacionDestino, nombreFormateado_estacionLlegada, 1)
                for _ in range(24):
                    mp.put(mapa_horasOrigen, _, 0)
                    mp.put(mapa_horasDestino, _, 0)
                mp.put(mapa_horasDestino, hora2, 1)
                lt.addLast(lst, 1)
                lt.addLast(lst, tiempo_viaje)
                lt.addLast(lst, mapa_estacionOrigen)
                lt.addLast(lst, mapa_estacionDestino)
                lt.addLast(lst, mapa_horasOrigen)
                lt.addLast(lst, mapa_horasDestino)
                om.put(arbol, fechaParcial2, lst)
    
    def respuesta_req5(catalog, fecha_inicial, fecha_final):
        mapa = catalog["arbolFechas_viajes_usuariosAnuales"]
        fecha_inicial = datetime.datetime.strptime(fecha_inicial, '%m/%d/%Y')
        fecha_final = datetime.datetime.strptime(fecha_final, '%m/%d/%Y')
        valores = om.values(mapa, fecha_inicial, fecha_final)

        estacionOrigenMasFrecuentada = lt.newList()
        estacionOrigenMasFrecuentada_mapa = mp.newMap()
        estacionDestinoMasFrecuentada = lt.newList()
        estacionDestinoMasFrecuentada_mapa = mp.newMap()
        horaDelDiaMasViajesInician = lt.newList()
        horaDelDiaMasViajesInician_mapa = mp.newMap()
        horaDelDiaMasViajesTerminan = lt.newList()
        horaDelDiaMasViajesTerminan_mapa = mp.newMap()

        # cmpGeneral3 - elemento a comparar 2

        totalViajesRealizados = 0
        totalTiempoViajes = 0
        print(lt.size(valores))
        for dia in lt.iterator(valores):
            totalViajesRealizados += lt.getElement(dia, 1)
            totalTiempoViajes += lt.getElement(dia, 2)
            mapa_estacionOrigen = lt.getElement(dia, 3)
            mapa_estacionDestino = lt.getElement(dia, 4)
            mapa_horasOrigen = lt.getElement(dia, 5)
            mapa_horasDestino = lt.getElement(dia, 6)
            
            # loop mapa_estacionOrigen
            keys = mp.keySet(mapa_estacionOrigen)
            for key in lt.iterator(keys):
                existe = mp.contains(estacionOrigenMasFrecuentada_mapa, key)
                if existe:
                    value_lst = me.getValue(mp.get(estacionOrigenMasFrecuentada_mapa, key))
                    info = lt.getElement(value_lst, 2)
                    lt.changeInfo(value_lst, 2, info + me.getValue(mp.get(mapa_estacionOrigen, key)))
                else:
                    lst = lt.newList()
                    lt.addLast(lst, key)
                    lt.addLast(lst, me.getValue(mp.get(mapa_estacionOrigen, key)))
                    lt.addLast(estacionOrigenMasFrecuentada, lst)
                    mp.put(estacionOrigenMasFrecuentada_mapa, key, lst)
            
            keys = mp.keySet(mapa_estacionDestino)
            for key in lt.iterator(keys):
                existe = mp.contains(estacionDestinoMasFrecuentada_mapa, key)
                if existe:
                    value_lst = me.getValue(mp.get(estacionDestinoMasFrecuentada_mapa, key))
                    info = lt.getElement(value_lst, 2)
                    lt.changeInfo(value_lst, 2, info + me.getValue(mp.get(mapa_estacionDestino, key)))
                else:
                    lst = lt.newList()
                    lt.addLast(lst, key)
                    lt.addLast(lst, me.getValue(mp.get(mapa_estacionDestino, key)))
                    lt.addLast(estacionDestinoMasFrecuentada, lst)
                    mp.put(estacionDestinoMasFrecuentada_mapa, key, lst)

            keys = mp.keySet(mapa_horasOrigen)
            for key in lt.iterator(keys):
                existe = mp.contains(horaDelDiaMasViajesInician_mapa, key)
                if existe:
                    value_lst = me.getValue(mp.get(horaDelDiaMasViajesInician_mapa, key))
                    info = lt.getElement(value_lst, 2)
                    lt.changeInfo(value_lst, 2, info + me.getValue(mp.get(mapa_horasOrigen, key)))
                else:
                    lst = lt.newList()
                    lt.addLast(lst, key)
                    lt.addLast(lst, me.getValue(mp.get(mapa_horasOrigen, key)))
                    lt.addLast(horaDelDiaMasViajesInician, lst)
                    mp.put(horaDelDiaMasViajesInician_mapa, key, lst)

            keys = mp.keySet(mapa_horasDestino)
            for key in lt.iterator(keys):
                existe = mp.contains(horaDelDiaMasViajesTerminan_mapa, key)
                if existe:
                    value_lst = me.getValue(mp.get(horaDelDiaMasViajesTerminan_mapa, key))
                    info = lt.getElement(value_lst, 2)
                    lt.changeInfo(value_lst, 2, info + me.getValue(mp.get(mapa_horasDestino, key)))
                else:
                    lst = lt.newList()
                    lt.addLast(lst, key)
                    lt.addLast(lst, me.getValue(mp.get(mapa_horasDestino, key)))
                    lt.addLast(horaDelDiaMasViajesTerminan, lst)
                    mp.put(horaDelDiaMasViajesTerminan_mapa, key, lst)
            
        sa.sort(estacionOrigenMasFrecuentada, cmpGeneral3)
        sa.sort(estacionDestinoMasFrecuentada, cmpGeneral3)
        sa.sort(horaDelDiaMasViajesInician, cmpGeneral3)
        sa.sort(horaDelDiaMasViajesTerminan, cmpGeneral3)

        estacionDeOrigenMasFrecuentada = lt.getElement(estacionOrigenMasFrecuentada, 1)
        estacionDeDestinoMasFrecuentada = lt.getElement(estacionDestinoMasFrecuentada, 1)
        horaDiaMasViajesInician = lt.getElement(horaDelDiaMasViajesInician, 1)
        horaDiaMasViajesTerminan= lt.getElement(horaDelDiaMasViajesTerminan, 1)

        return (totalViajesRealizados, totalTiempoViajes, lt.getElement(estacionDeOrigenMasFrecuentada, 1), lt.getElement(estacionDeOrigenMasFrecuentada, 2), lt.getElement(estacionDeDestinoMasFrecuentada, 1), lt.getElement(estacionDeDestinoMasFrecuentada, 2), lt.getElement(horaDiaMasViajesInician, 1), lt.getElement(horaDiaMasViajesTerminan, 1))



                



# los que llegan asi mismo y los que no tienen duracion (o los que tienen duracion 0)