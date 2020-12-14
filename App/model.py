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
from DISClib.DataStructures import mapentry as me
from datetime import timedelta  
from DISClib.ADT import orderedmap as om
import datetime
from DISClib.DataStructures import mapentry as me
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
                    'hourIndex':None
                    
                    }

        chicago['stops'] = m.newMap(numelements=14000,
                                     maptype='PROBING',
                                     comparefunction=compareStopIds)

        chicago['connections'] = m.newMap(numelements=2000,
                                     maptype='PROBING',
                                     comparefunction=compareStopIds)
        chicago['graph']=gr.newGraph(datastructure="ADJ_LIST",
             directed=True,
             size=54140,
             comparefunction=compareStopIds
        
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
    if duration != ""and duration!="0":
        duration=float(duration)
    else:
        duration=float('inf')
    distance=trip['trip_miles']
    company=trip['company']
    origin=trip['pickup_community_area']
    destination=trip['dropoff_community_area']
    tarifa=trip['fare']
    tarifafinal=trip['trip_total']
    time=trip['trip_start_timestamp']
    tripdate = datetime.datetime.strptime(time, '%Y-%m-%dT%H:%M:%S.%f')
    time=tripdate.time()
    addStation(analyzer, origin)
    addStation(analyzer, destination)
    if origin!="" and destination!="":
        addConnection(analyzer, origin, destination, duration,time)
    
    #addStation(analyzer, destination)
    
    #addDistance(analyzer,origin,latitude,longitude)
    

def addStation(taxis, stationid):
    """
    Adiciona una estación como un vertice del grafo
    """
    if not gr.containsVertex(taxis['graph'], stationid):
            gr.insertVertex(taxis['graph'], stationid)
    return taxis

def addConnection(taxis, origin, destination, duration,time):
    """
    Adiciona un arco entre dos estaciones
    """
    edge = gr.getEdge(taxis['graph'], origin, destination)
    if edge is None:
        gr.addEdge(taxis['graph'], origin, destination, duration)

    mapa= m.get(taxis['connections'],origin+"-"+destination)
    if mapa is None:
       
        mapaordenado2=om.newMap( comparefunction=compareDates)
       
        om.put(mapaordenado2,time,duration)
        m.put(taxis['connections'],origin+"-"+destination,mapaordenado2)
    else:
        value=me.getValue(mapa)
        duration1=om.get(value,time)
        if duration1 is None:
            om.put(value,time,duration)
            m.put(taxis['connections'],origin+"-"+destination,value)    
        else:
            duration1=me.getValue(duration1)
            if duration1=="":
                duration1=0
            if duration=="":
                duration=duration1
            om.put(value,time,(float(duration)+float(duration1)))
            m.put(taxis['connections'],origin+"-"+destination,value)
    return taxis

# ==============================
# Funciones de consulta
# ==============================
def firstRequirement(analyzer):
    return None

def secondRequirement(analyzer):
    return None

def thirdRequirement(cont,inicio,llegada,inicial,final):
    grafo=cont['graph']
    road=djk.Dijkstra(grafo,inicio)
    primera=inicio
    if djk.hasPathTo(road,llegada):
        ruta=djk.pathTo(road,llegada)
        lista=generarlistarango(inicial,final)
        ref=float('inf') 
        iterator=it.newIterator(lista)
        hora=inicial
        rutanueva=""
        while it.hasNext(iterator):
            element=it.next(iterator)
            iterator2=it.newIterator(ruta)
            tiempo=0
            todos=True
            rutanueva=primera
            while it.hasNext(iterator2):
                path=it.next(iterator2)
                rutanueva+="-"+path['vertexB']
                inicio=path['vertexA']
                llegada=path['vertexB']
                if m.get(cont['connections'],inicio+"-"+llegada) is not None:  
                    if om.get(me.getValue(m.get(cont['connections'],inicio+"-"+llegada)),element.time()) is not None:
                        tiempo+=float(me.getValue(om.get(me.getValue(m.get(cont['connections'],inicio+"-"+llegada)),element.time())))
                    else:
                        todos=False
                else:
                    todos=False
            
            if tiempo<ref and todos:
                hora=element.time()
                ref=tiempo
        if ref !=float('inf'):
            hora=str(hora.strftime("%H:%M:%S"))
            dat=hora.split(":")
            print("Se recomienda ir a las {} horas con {} minutos con un tiempo estimado de {} segundos. La ruta es: {}".format(dat[0],dat[1], ref,rutanueva))

        else:
            print("No se encontró información concluyente. Se recomienda ir a las {}. Es mejor llegar temprano que tarde! La ruta es: {}".format(inicial.time(),rutanueva))


    else:
        print("No se encontró información concluyente. Se recomienda ir a las {}. Es mejor llegar temprano que tarde! La ruta es: {}-{}".format(inicial.time(),primera,llegada))



def generarlistarango(inicial,final):
    inicial1=str(inicial.strftime("%H:%M:%S"))
    final1=str(final.strftime("%H:%M:%S"))
    time=inicial
    lista=lt.newList()
    data=str((final-inicial)).split(':')
    i=int(data[0])*4+int(int(data[1])/15)
    while i>=0:
        time=inicial+timedelta(minutes=i*15)
        lt.addLast(lista,time)
        i-=1
    return lista



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

def compareDates(date1, date2):
    
    if (date1 == date2):
        return 0
    elif (date1 > date2):
        return 1
    else:
        return -1

def roundingtime(x,base=15):
    var=x.split(":")
    if round(int(var[1])/15)==0 :
        x="{:02d}".format(int(var[0]))+":"+"00"
    elif round(int(var[1])/15)==1:
        x="{:02d}".format(int(var[0]))+":"+str(15)
    elif round(int(var[1])/15)==2:
        x="{:02d}".format(int(var[0]))+":"+str(30)
    elif round(int(var[1])/15)==3:
        x="{:02d}".format(int(var[0]))+":"+str(45)
    else:
        x="{:02d}".format(int(var[0]))+":"+"00"
    return x
