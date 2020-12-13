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


import sys
import config
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from App import controller
assert config
import timeit

"""
La vista se encarga de la interacción con el usuario.
Presenta el menu de opciones  y  por cada seleccion
hace la solicitud al controlador para ejecutar la
operación seleccionada.
"""

# ___________________________________________________
#  Ruta a los archivos
# ___________________________________________________

pequeno = 'taxi-trips-wrvz-psew-subset-small.csv'

# ___________________________________________________
#  Menu principal
# ___________________________________________________


def printMenu():
    print("\n")
    print("*******************************************")
    print("Bienvenido")
    print("1- Inicializar Analizador")
    print("2- Cargar información")
    print("R1- Requerimiento 1")
    print("R2- Requerimiento 2")
    print("R3- Requerimiento 3")
    print("0- Salir")
    print("*******************************************")

def optionTwo():
    print("\nCargando información de taxis....")
    if archivo == 1:
       controller.loadData(cont, pequeno)   


def optionThree():
    return controller.firstRequirement(cont)

def optionFour():
    res = controller.secondRequirement(cont, initialDate, finalDate, int(num_taxis))
    print("Taxis con más puntos: ", res)

def optionFive():
    return controller.thirdRequirement(cont)

"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n>')

    if inputs[0] == "1":
        print("\nInicializando....")
        cont = controller.init()

    elif inputs[0] == "2":
        print("¿Que tamaño de archivos desea cargar?")
        print("1- Pequeño (25 Mb)")
        print("2- Mediano (100 Mb)")
        print("3- Grande (1 Gb)")
        archivo = int(input("Escriba el numero correspondiente al archivo a utilizar: "))
        executiontime = timeit.timeit(optionTwo, number=1)
        print("Tiempo de ejecución: " + str(executiontime))

    elif inputs == "R1":
        executiontime = timeit.timeit(optionThree, number=1)
        print("Tiempo de ejecución: " + str(executiontime))

    elif inputs == "R2":
        initialDate = input("Introduzca la fecha inicial (Formato: AA-MM-DD): ")
        finalDate = input("Introduzca la fecha final ó deje el espacio en blanco si no desea agregar una fecha final: ")
        if finalDate == "":
           finalDate = initialDate 
        num_taxis = input("Número de taxis a retornar con más puntos: ")
        executiontime = timeit.timeit(optionFour, number=1)
        print("Tiempo de ejecución: " + str(executiontime))

    elif int(inputs[0]) == "R3":
        executiontime = timeit.timeit(optionFive, number=1)
        print("Tiempo de ejecución: " + str(executiontime))
    else:
        sys.exit(0)
sys.exit(0)
