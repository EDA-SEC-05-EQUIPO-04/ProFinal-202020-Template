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
import operator
from datetime import datetime
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.ADT import orderedmap as om
from DISClib.DataStructures import mapentry as me
from DISClib.DataStructures import listiterator as it
from DISClib.Algorithms.Sorting import mergesort as ms
assert config


# -----------------------------------------------------
# API del TAD de Taxis
# -----------------------------------------------------


def newAnalyzer():
    """ Inicializa el analizador
    Crea una lista vacia para guardar los nombres de los taxis
    Guarda datos de las compañías en un mapa.
    """
    chicago = {'taxis': None,
               'companies': None,
               "dateIndex": None}

    chicago['taxis'] = []   
    chicago['companies'] = mp.newMap(50,
                                   maptype='PROBING',
                                   loadfactor=0.4,
                                   comparefunction=compareCompanies)
    chicago['dateIndex'] = om.newMap(omaptype='RBT',
                                      comparefunction=compareDates)                                    

    return chicago

# Funciones para agregar informacion sobre viajes

def newCompany(name):
    """
    Crea una nueva estructura para modelar las compañías de taxis,
    su número de servicios y sus taxis afiliados
    """
    companies = {'name': "", 
              "taxis": lt.newList('SINGLE_LINKED', compareTaxiIds),
              "numservices": 0}
    companies['name'] = name
    return companies

def addTrips(chicago, trip):
    """
    """
    if trip["taxi_id"] not in chicago["taxis"]:
       chicago["taxis"].append(trip["taxi_id"])   
    addTaxiDate(chicago, trip)   
    companyname = trip["company"]
    if companyname == "":
       companyname = "Independent Owner" 
    companies = chicago['companies']
    existcompany = mp.contains(companies, companyname)
    if existcompany:
        entry = mp.get(companies, companyname)
        company = me.getValue(entry)
    else:
        company = newCompany(companyname)
        mp.put(companies, companyname, company)  
    if lt.isPresent(company["taxis"], trip["taxi_id"]) == False:    
       lt.addLast(company['taxis'], trip["taxi_id"]) 
    company["numservices"] += 1

def addTaxiDate(chicago, trip):
    """
    """
    occurreddate = trip['trip_start_timestamp']

    tripdate = occurreddate[0:10]

    entry = om.get(chicago["dateIndex"], tripdate)

    if entry is None:
       om.put(chicago["dateIndex"], tripdate, mp.newMap(50,
                                   maptype='PROBING',
                                   loadfactor=0.4,
                                   comparefunction=compareTaxiIds))
    entry = om.get(chicago["dateIndex"], tripdate)                   
    if mp.contains(entry["value"], trip["taxi_id"]) == False:
       taxi_data = me.getValue(entry)
       taxi_data = newTaxi(trip["taxi_id"])
       if trip["trip_miles"] != "" and trip["trip_total"] != "":
          millas = float(trip["trip_miles"])
          dinero = float(trip["trip_total"]) 
          if millas > 0 and dinero > 0:
             taxi_data["millas"] = millas
             taxi_data["dinero"] = dinero
             mp.put(entry["value"], trip["taxi_id"], taxi_data) 
    else:
       taxi_data = me.getValue(entry)
       taxi_data = mp.get(me.getValue(entry), trip["taxi_id"])
       taxi_data = taxi_data["value"]
       if trip["trip_miles"] != "" and trip["trip_total"] != "":
          millas = float(trip["trip_miles"])
          dinero = float(trip["trip_total"])  
          if millas > 0 and dinero > 0:
             taxi_data["millas"] += millas
             taxi_data["dinero"] += dinero      
             taxi_data["numservices"] += 1     
             mp.put(entry["value"], trip["taxi_id"], taxi_data) 

def newTaxi(name):
    """
    """
    taxi_data = {'name': "", 
              "millas": 0,
              "dinero": 0,
              "numservices": 1}
    taxi_data['name'] = name
    return taxi_data

# ==============================
# Funciones de consulta
# ==============================


def firstRequirement(analyzer, m, n):

    lstcompanies = lt.newList(datastructure='SINGLE_LINKED', cmpfunction=None)
#POR TAXIS

    companies = analyzer["companies"]
    iterador = it.newIterator(mp.valueSet(companies))
    while it.hasNext(iterador):
        x = it.next(iterador)
        lt.addFirst(lstcompanies, (x["name"], lt.size(x["taxis"])))
    
    ms.mergesort(lstcompanies, compareR1)

    print("-----Por Número de taxis-----")
    servicios = lt.subList(lstcompanies, 0, m)
    iteradorserv = it.newIterator(servicios)
    while it.hasNext(iteradorserv):
        x = it.next(iteradorserv)
        print("Compañía: ",x[0],", Taxis: ",x[1])

    lstservices = lt.newList(datastructure='SINGLE_LINKED', cmpfunction=None)
#POR SERVICIOS

    companies = analyzer["companies"]
    iterador = it.newIterator(mp.valueSet(companies))
    while it.hasNext(iterador):
        x = it.next(iterador)
        lt.addFirst(lstservices, (x["name"], x["numservices"]))
    
    ms.mergesort(lstservices, compareR1)

    print("-----Por Servicios ofrecidos-----")
    servicios = lt.subList(lstservices, 0, n)
    iteradorserv = it.newIterator(servicios)
    while it.hasNext(iteradorserv):
        x = it.next(iteradorserv)
        print("Compañía: ",x[0],", Servicios: ",x[1])

 
    

    return None

def secondRequirement(chicago, initialDate, finalDate, numN):
    """
    """
    lst = om.values(chicago['dateIndex'], initialDate, finalDate)
    dicc_taxi = {}
    for i in range(lt.size(lst)):
        date = lt.getElement(lst, i)
        for taxi_name in chicago["taxis"]:
            taxi_data = mp.get(date, taxi_name)
            if taxi_data != None:
               millas = taxi_data["value"]["millas"]
               dinero = taxi_data["value"]["dinero"]
               numservices = taxi_data["value"]["numservices"]
               if taxi_name not in dicc_taxi:
                  dicc_taxi[taxi_name] = [millas, dinero, numservices]
               else:
                  millas2 = dicc_taxi[taxi_name][0]
                  dinero2 = dicc_taxi[taxi_name][1]
                  numservices2 = dicc_taxi[taxi_name][2]
                  dicc_taxi[taxi_name] = [millas + millas2, dinero + dinero2, numservices + numservices2]   
    for taxi_name in chicago["taxis"]:
        if taxi_name in dicc_taxi:
           alfa = (dicc_taxi[taxi_name][0] / dicc_taxi[taxi_name][1]) * dicc_taxi[taxi_name][2]       
           dicc_taxi[taxi_name] = alfa
    top_alfa = sorted(dicc_taxi.items(), key=operator.itemgetter(1), reverse=True)   
    return top_alfa[0:numN]      

def thirdRequirement(analyzer):
    return None


# ==============================
# Funciones de Comparacion
# ==============================

def compareR1(thing1, thing2):
    """
    Compara datos en tupla.
    """
    if (int(thing1[1]) == int(thing2[1])):
        return 0
    elif (int(thing1[1]) > int(thing2[1])):
        return 1
    else:
        return -1 

def compareDates(date1, date2):
    """
    Compara fechas
    """
    if (date1 == date2):
        return 0
    elif (date1 > date2):
        return 1
    else:
        return -1 

def compareTaxiIds(id1, id2):
    """
    Compara ids de taxis
    """
    if not isinstance(id2, str):
       id2 = me.getKey(id2)
    if (id1 == id2):
        return 0
    elif id1 > id2:
        return 1
    else:
        return -1


def compareCompanies(id, entry):
    """
    Compara compañías
    """
    identry = me.getKey(entry)
    if id == identry:
        return 0
    elif id > identry:
        return 1
    else:
        return -1