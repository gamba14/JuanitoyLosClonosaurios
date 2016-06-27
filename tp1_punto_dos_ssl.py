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


def pasarADeteministico(asf):
    """ Obtiene un automata deterministico de un automata"""

    q0 = sorted(uno.cllambda(asf, { asf["init"] }))

    states = [q0]
    states_marcados = [False for s in states]

    transacciones = {}

    c = 0
    while (any(False == marcado for marcado in states_marcados)):
        t = states[c]
        states_marcados[c] = True

        for a in sorted(asf["inputs"]):
            u = uno.mover(asf, set(t) , a)

            us = sorted(u)
            
            if (not (us in states)):
                states.append(us)
                states_marcados.append(False)


            transaccion_aux = transacciones.get(str(t), {})

            transaccion_aux[a] = str(sorted(u))

            transacciones[str(t)] = transaccion_aux


        c += 1

    finales = filter(lambda x: any(map(lambda y: y in asf['final'], x)), states)

    return (states, asf["inputs"], q0, finales, transacciones)


def pasarADeteministicoLegible(asf):
    """ Construye un automata con los resultados de obtenerDetemistico """
    estados, entradas, inicial, finales, transacciones = pasarADeteministico(asf)

    deterministico = {
        "states": set([]),
        "inputs": set([]),
        "init": -1,
        "final": set([]),
        "transtion": {}
    }

    deterministico['inputs'] = entradas

    # original to 'pretty'
    o_to_p = {}

    # 'pretty' to orginal
    p_to_o = {}


    aux = [] 
    c = 0
    for x in estados:

        o_to_p[str(x)] = c
        p_to_o[c] = str(x)
        
        aux.append(c)

        c += 1

    deterministico['states'] = set(aux)


    deterministico['init'] = o_to_p[str(inicial)]


    aux = []
    for x in finales:
        aux.append(o_to_p[str(x)])

    deterministico['final'] = set(aux)



    deterministico['transtion'] = {}
    for estado in estados:
        
        sEstado = str(estado)

        transaccion_aux = {}

        for entrada in entradas:
            transaccion_aux[entrada] = o_to_p[ str(transacciones[sEstado][entrada]) ]

        deterministico['transtion'][o_to_p[sEstado]] = transaccion_aux


    print ('determistico', deterministico)
    return deterministico


def conjuntoToStr(lista):
    """ Pasa una lista a un string con los elementos encerrrados entre corchetes """
    newStr = "{"

    if (len(lista) != 0):
        for elem in lista[0:-1]:

            newStr += str(elem) + ","

        newStr += str(lista[-1])
        
    
    newStr = newStr + '}\n'
    
    return newStr


def transaccionesToStr(determ):
    """ Convierte las transacciones a string """
    newStr = ""

    delta = determ['transtion']

    for estado in sorted(determ['states']):

        newStr += str(estado)

        for entrada in sorted(determ['inputs']):
            newStr += entrada + str(delta[estado][entrada])

        newStr += "#\n"

    return newStr


def createNew(determ, outPath):
    """ Escribe el automata deterministico en un archivo"""

    parseOut = open(outPath,'w')

    newStr = conjuntoToStr(sorted(determ["states"]))
    parseOut.write(newStr)

    newStr = conjuntoToStr(sorted(determ["inputs"]))
    parseOut.write(newStr)

    newStr = conjuntoToStr([determ["init"]])
    parseOut.write(newStr)

    newStr = conjuntoToStr(sorted(determ["final"]))
    parseOut.write(newStr)

    newStr = transaccionesToStr(determ)
    parseOut.write(newStr)


def existOutputFile(outPath):
    if (outPath != "" and os.path.isfile(outPath)):
    
        # TODO: preguntar se desea sobreescribir
        #print ('El archivo ya existe ¿desea sobre escribirlo? [Y/n]')
        # leer respuesta

        pass #Sobreescribamos por el momento



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

            if (os.path.exists(outPath)):
                # se informa que el path No existe
                print ('La ruta de salida NO es valida')

                # Se finaliza el scritp sin error
                sys.exit()


    existOutputFile(outPath)


    if (os.path.exists(path) and os.path.isfile(path)):

        # Parseo/Interpreto/(?) el archivo (como automata)
        asf = uno.parseFile(path)

        # Imprimo el resultado del parseo (me canse)
        print (asf) 

        # Si NO se ingreso el archivo de salida, su usa uno por defecto
        if (outPath == ""):
            outPath = os.path.realpath(os.path.dirname(__file__)) + "/out.txt"

            existOutputFile(outPath)

        newAsf = pasarADeteministicoLegible(asf)

        # Creo el nuevo archivo
        createNew(newAsf, outPath) 


    else:
        # Si la ruta no es valida o no corresponde a un archivo
        print ("El archivo no es valido") # TODO: mejorar mensaje de error


# Si el scritp es llamado directamente (Osea NO es importado como libreria)
if __name__ == "__main__":
    # Ejecuto el proceso principal con los argumentos exepto el primero que es 
    # el nombre del scritp
    main(sys.argv[1:])
    
    
