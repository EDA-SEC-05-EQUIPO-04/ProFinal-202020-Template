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

import config as cf
from App import model
import csv


"""
El controlador se encarga de mediar entre la vista y el modelo.
Existen algunas operaciones en las que se necesita invocar
el modelo varias veces o integrar varias de las respuestas
del modelo en una sola respuesta.  Esta responsabilidad
recae sobre el controlador.
"""

# ___________________________________________________
#  Inicializacion del catalogo
# ___________________________________________________


def init():
    """
    Llama la funcion de inicializacion.
    """
    analyzer = model.newAnalyzer()
    return analyzer


# ___________________________________________________
#  Funciones para la carga de datos y almacenamiento
#  de datos en los modelos
# ___________________________________________________

def loadData(analyzer, tripsfile):
    """
    Carga los datos de los archivos en el modelo
    """
    loadTrips(analyzer, tripsfile)


def loadTrips(analyzer, tripsfile):
    """
    """
    tripsfile = cf.data_dir + tripsfile
    input_file = csv.DictReader(open(tripsfile, encoding="utf-8"),
                                delimiter=",")
    for trip in input_file:
        model.addTrips(analyzer, trip)


# ___________________________________________________
#  Funciones para consultas
# ___________________________________________________

def firstRequirement(analyzer):
    m= int(input("Top M de compañías por taxis: "))
    n= int(input("Top N de compañías por servicios: "))
    return model.firstRequirement(analyzer, m, n)

def secondRequirement(analyzer, initialDate, finalDate, numN ):
    taxipointsbyrange = model.secondRequirement(analyzer, initialDate, finalDate, numN)
    return taxipointsbyrange

def thirdRequirement(cont):
    return model.thirdRequirement(cont)
