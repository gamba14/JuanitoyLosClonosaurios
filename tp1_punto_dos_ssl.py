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
#!/usr/bin/python

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
    withString  = False

    # Interpreto/Parseo/(?) los parametros
    try:
        # Obtiene las opciones (-h, -a, --automata, -s, --string)
        # los argumentos correspondientes a cada uno de ellos
        opts, args = getopt.getopt(argv,"ha:s:",["automata=","string="])

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
            print ('tp1_punto_dos_ssl.py -a <archivo_automata> -s <cadena>')

            # Se finaliza el scritp sin error
            sys.exit()

        # Si la opcion es '-a' o '--automata'
        elif opt in ("-a", "--automata"):
            # el argumento asociado es la ruta al archivo txt con el automata
            # a parsear/interpretar/(?)
            path = arg

        # Si la opcion es '-s' o '--string'
        elif opt in ("-o", "--output"):
            # propociona un archivo de salida
            outputPath = arg

            # Uso una bandera para informar que el path ya fue proporcionado 
            # via argumento
            withString  = False

    # Si la ruta es valida y corresponde a un archivo
    if (os.path.exists(path) and os.path.isfile(path)):

        # Parseo/Interpreto/(?) el archivo (como automata)
        asf = uno.parseFile(path)

        # Imprimo el resultado del parseo (me canse)
        #print (asf) 
        createNew(asf)

        # Si se dispone a cadena a comprobar
        #if (withString):
#
#        #    # Verifico que la cadena sea aceptada
#        #    if (isValid(asf, inputString)):
#        #        # Informo que es aceptada
#        #        print ("La cadena es aceptada por el automata") #TODO: mejorar el mensaje
#
#        #    else:
#        #        # Informo que NO es aceptada
#        #        print ("La cadena NO es aceptada por el automata") #TODO: mejorar el mensajepyt
#        #else:
#        #    # leer las cadena que ingresa el usuario y chekear si cada una es 
#        #    # aceptada por el automata
        #    print ("implementame (?)") # TODO implementar

    else:
        # Si la ruta no es valida o no corresponde a un archivo
        print ("El archivo no es valido") # TODO: mejorar mensaje de error


# Si el scritp es llamado directamente (Osea NO es importado como libreria)
if __name__ == "__main__":
    # Ejecuto el proceso principal con los argumentos exepto el primero que es 
    # el nombre del scritp
    main(sys.argv[1:])
    
    
