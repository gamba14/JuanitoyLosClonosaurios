#!/usr/bin/python
###############################################
# T R A B A J O  P R A C T I C O   1          #
# SINTAXIS Y SEMANTICA DE LOS LENGUAJES       #
# UTN FACULTAD REGIONAL DELTA                 #  
# GRUPO                                       #
# INTEGRANTES :                               #
#                POSADAS LIAUDAT, EMMANUEL    #
#                GAMBIRASSI, AGUSTIN          #
#                CALVI, RAFFI                 #
# AÑO 2016                                    #
###############################################   


import os.path
import fileinput
import sys, getopt

import tp1_punto_uno_ssl as uno

# TODO Definir funciones y escribir el comportamiento esperado
# TODO cambiar los comentarios donde corresponda
# TODO cambiar comportamiento

def createNew(asf):

    # outputPath = out # sera la variable que contenga la ruta al archivo

    # parseOut = open(out+'/out_ej2.txt','w') #creo y asigno el archivo a la variable parseOut

    parseOut = open('testing_punto2.txt','w') #as it says "proposito de pruebas"

    states = sorted(asf["states"])

    init  = asf["init"]

    final = sorted(asf["final"])

    transtions = asf["transtion"]

    states = uno.cllambda(asf, set([asf["init"]]))

    newStates = []

    for caracter in sorted(asf["inputs"]):

        newState = uno.mover(asf, states, caracter)

        newStates.append(newState)


    # for elem in 

    print(newStates)


    newStr = "{"

    for elem in sorted(asf["inputs"]):

        newStr = newStr + elem + ","
    
    newStr = newStr + '}'

    parseOut.write(newStr)



def main(argv):
    """Proceso principal"""

    # Variables que van a contener la informacion obtenida de los parametros
    path = ""
    inputString = ""
    outPath = ""

    # Interpreto/Parseo/(?) los parametros
    try:
        # Obtiene las opciones (-h, -i, --input, -o, --output)
        # los argumentos correspondientes a cada uno de ellos
        opts, args = getopt.getopt(argv,"hi:o:",["input=","output="])

    except getopt.GetoptError:
        # Si hay alguna opcion invalida

        # Se informa la forma correcta de uso
        print ('tp1_punto_dos_ssl.py -i <inputfile> -o <outputfile>')
        
        # Y se finaliza el scritp informando un error 
        # Cuando se finaliza con cualquier nuemero distinto de 0 se considerar
        # que el programa finalizo con errores, en esta caso 2
        sys.exit(2)

    # Por cada par ordenado de opciones-argumentos obtenidos
    for opt, arg in opts:

        # Si la opcion es '-h' 
        if opt == '-h':

            # se informa la forma de uso correcto
            print ('tp1_punto_dos_ssl.py -i <inputfile> -o <outputfile>')

            # Se finaliza el scritp sin error
            sys.exit()

        # Si la opcion es '-i' o '--input'
        elif opt in ("-i", "--input"):
            # el argumento asociado es la ruta al archivo txt con el automata
            # a parsear/interpretar/(?)
            path = arg

        # Si la opcion es '-o' o '--output'
        elif opt in ("-o", "--output"):
            # propociona un archivo de salida
            outPath = arg

    if (os.path.exists(path) and os.path.isfile(path)):

        # Parseo/Interpreto/(?) el archivo (como automata)
        asf = uno.parseFile(path)

        # Imprimo el resultado del parseo (me canse)
        #print (asf) 
        createNew(asf)

    else:
        # Si la ruta no es valida o no corresponde a un archivo
        print ("El archivo no es valido") # TODO: mejorar mensaje de error


# Si el scritp es llamado directamente (Osea NO es importado como libreria)
if __name__ == "__main__":
    # Ejecuto el proceso principal con los argumentos exepto el primero que es 
    # el nombre del scritp
    main(sys.argv[1:])
    
    
