"""
 * Copyright 2020, Departamento de sistemas y Computación
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
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 * Contribución de:
 *
 * Dario Correal
 *
 """
import config
from DISClib.ADT.graph import gr
from DISClib.ADT import map as m
from DISClib.ADT import list as lt
from DISClib.DataStructures import listiterator as it
from DISClib.Algorithms.Graphs import scc
from DISClib.Algorithms.Graphs import dijsktra as djk
from DISClib.Utils import error as error
assert config

"""
En este archivo definimos los TADs que vamos a usar y las operaciones
de creacion y consulta sobre las estructuras de datos.
"""

# -----------------------------------------------------
#                       API
# -----------------------------------------------------
def newAnalyzer():
    """ Inicializa el analizador
    Crea una lista vacia para guardar todos los accidentes
    Se crean indices (Maps) por los siguientes criterios:
    -Fechas
    Retorna el analizador inicializado.
    """
    try:
        chicago = {
                    'stops': None,
                    'connections': None,
                    'components': None,
                    'paths': None,
                    'graph':None,
                    'distance':None,
                    
                    }

        chicago['stops'] = m.newMap(numelements=14000,
                                     maptype='PROBING',
                                     comparefunction=compareStopIds)

        chicago['connections'] = gr.newGraph(datastructure='ADJ_LIST',
                                              directed=True,
                                              size=14000,
                                              comparefunction=compareStopIds)
        chicago['graph']=gr.newGraph(datastructure="ADJ_LIST",
             directed=True,
             size=54140,
             comparefunction=compareStations
        
             )       
        chicago['distance']=m.newMap(numelements=14000,
                                     maptype='PROBING',
                                     comparefunction=compareStopIds) 
        
       
                                             
        return chicago
    except Exception as exp:
        error.reraise(exp, 'model:newAnalyzer')



# Funciones para agregar informacion al grafo
def addTrip(analyzer, trip):
    """
    """
    taxiId = trip['taxi_id']
    duration=trip['trip_seconds']
    distance=trip['trip_miles']
    company=trip['company']
    origin=trip['dropoff_community_area']
    destination=trip['pickup_community_area']
    tarifa=trip['fare']
    tarifafinal=trip['trip_total']

    addStation(analyzer, origin)
    addStation(analyzer, destination)
    #addStation(analyzer, destination)
    #addConnection(analyzer, origin, destination, duration)
    #addDistance(analyzer,origin,latitude,longitude)
    

def addStation(taxis, stationid):
    """
    Adiciona una estación como un vertice del grafo
    """
    if not gr.containsVertex(taxis['graph'], stationid):
            gr.insertVertex(taxis['graph'], stationid)
    return taxis
# ==============================
# Funciones de consulta
# ==============================
def totalStops(analyzer):
    """
    Retorna el total de estaciones (vertices) del grafo
    """
    return gr.numVertices(analyzer['graph'])

def totalConnections(analyzer):
    """
    Retorna el total arcos del grafo
    """
    return gr.numEdges(analyzer['graph'])



def tripsSize(analyzer):
    """
    Número de accidentes leidos
    """
    return None
# ==============================
# Funciones Helper
# ==============================



def dinstancefunction(lat1,lon1,lat2,lon2):
    R=3958.8
    return np.arccos(np.sin(lat1)*np.sin(lat2)+np.cos(lat1)*np.cos(lat2)*np.cos(lon1-lon2))*R

# ==============================
# Funciones de Comparacion
# ==============================
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

def compareStopIds2(stop, keyvaluestop):
    """
    Compara dos estaciones
    """
    stopcode = keyvaluestop['key']
    if (stop == stopcode):
        return 0
    elif (stop < stopcode):
        return 1
    else:
        return -1

def compareStations(stop, keyvaluestop):
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

def compareroutes(route1, route2):
    """
    Compara dos rutas
    """
    if (route1 == route2):
        return 0
    elif (route1 > route2):
        return 1
    else:
        return -1
