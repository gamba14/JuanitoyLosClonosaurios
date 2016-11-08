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

def parseFile(path):
    """ Leeo la gramatica desde el archivo y la valido """

    gramatica = {
        "VT": set([]), # no terminales
        "VN": set([]), # terminales
        "sInit": "",   # simbolo inicial
        "prods": []    # produciones: [{ladoIzquiendo: ladoDerecho}]
    }

    # TODO: implementar. (llenar el dicionario anterior)

    pass


def clausure(gramatica, cjtoItems):
    """ Genera la clasura del conjuntu de items de salida """
    
    # formato de items (lado izquierdo, lado derecho, posicion prefijo)
    # TODO: implementar. (devolver conjunto de items resultantes)

    pass


def calcuarSimbolosDeDesplazamiento(gramatica, cjtoItems):
    """ Calcula el subconjunto de V cuyos elementos pueden ser usados con gotoL """

    #TODO: implementar. (devolver subconjunto de simbolos V)

    pass


def gotoL(gramatica, cjtoItems, simbolo):
    """ Calcula el siguiente conjunto de items para el simbolo de entrada """

    #TODO: implementar. (conjunto de items)

    pass


def estrategiaIncreible(gramatica):
    """ Genera "la tabla" """

    # TODO: implementar. (devolver tabla)
    # Tabla (dicionarios de diccionarios): {"estado": { simboloA: accion, simboloB: accion }}

    pass


def main(argv):
    """Proceso principal"""

    # TODO: adapatar para este practico

    # Variables que van a contener la informacion obtenida de los parametros
    path = ""
    inputString = ""
    withString  = False

    # Interpreto/Parseo/(?) los parametros
    try:
        # Obtiene las opciones (-h, -i, --input, -s, --string)
        # los argumentos correspondientes a cada uno de ellos
        opts, args = getopt.getopt(argv,"hi:s:",["input=","string="])

    except getopt.GetoptError:
        # Si hay alguna opcion invalida

        # Se informa la forma correcta de uso
        print ('tp2_punto1.py -i <archivo_de_entrada> -s <cadena>')
        
        # Y se finaliza el scritp informando un error 
        # Cuando se finaliza con cualquier nuemero distinto de 0 se considerar
        # que el programa finalizo con errores, en esta caso 2
        sys.exit(2)

    # Por cada par ordenado de opciones-argumentos obtenidos
    for opt, arg in opts:

        # Si la opcion es '-h' 
        if opt == '-h':

            # se informa la forma de uso correcto
            print ('tp2_punto1.py -i <archivo_de_entrada> -s <cadena>')

            # Se finaliza el scritp sin error
            sys.exit()

        # Si la opcion es '-a' o '--automata'
        elif opt in ("-i", "--input"):
            # el argumento asociado es la ruta al archivo txt con la gramatica
            # a parsear/interpretar/(?)
            path = arg

        # Si la opcion es '-s' o '--string'
        elif opt in ("-s", "--string"):
            # el argumento asociado es la cadena que se debe verificar si es 
            # generada por la gramatica
            inputString = arg

            # Uso una bandera para informar que la cadena ya fue proporcionada 
            # via argumento
            withString  = True

    # Si la ruta es valida y corresponde a un archivo
    if (os.path.exists(path) and os.path.isfile(path)):

        # Parseo/Interpreto/(?) el archivo (como automata)
        asf = parseFile(path)

        # Imprimo el resultado del parseo (me canse)
        print (asf) 

        # Si se dispone a cadena a comprobar
        if (withString):

            # Verifico que la cadena sea aceptada
            if (isValid(asf, inputString)):
                # Informo que es aceptada
                print ("La cadena es aceptada por el automata") 

            else:
                # Informo que NO es aceptada
                print ("La cadena NO es aceptada por el automata") 
        else:
            # leer las cadena que ingresa el usuario y chekear si cada una es 
            # aceptada por el automata
            print ("implementame (?)") 

    else:
        # Si la ruta no es valida o no corresponde a un archivo
        print ("El archivo no es valido") 



# Si el scritp es llamado directamente (Osea NO es importado como libreria)
if __name__ == "__main__":
    # Ejecuto el proceso principal con los argumentos exepto el primero que es 
    # el nombre del scritp
    main(sys.argv[1:])

    