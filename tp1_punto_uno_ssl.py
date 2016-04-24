#!/usr/bin/python

import os.path
import fileinput
import sys, getopt

# Contenido del archivo a parsear:
# {0,1,2}
# {a,b}
# {0}
# {1,2}
# 0a1b2&0#
# 1a1b0#
# 2a2b2#

# Explicacion:
# De la linea 1 a 4 se dan los elementos fijos que son 
# linea 1 : el conjunto de estado
# linea 2: el conjunto de entradas
# linea 3 : el estado inicial
# linea 4 : los estados aceptados

def findBraces(string):
    """
    Devuelve las posiciones de cada una de las llaves y verifica que no se 
    habra una nueva antes de cerrar la ya abierto
    """
    
    # Busco el primer resulatdo de '{'
    begin = string.find('{')

    # Busco el primer resulatdo de '}'
    end   = string.find('}')
    
    # Si cualquiera de los resultados es -1 No encontro el simbolo
    # y verifica que la posicion de '{' este antes de '}'
    if ((begin != -1) and (end != -1) and (begin < end)):

        #Verifica que No se habra una nueva llave antes de cerrar la ya abierta
        if (string.find('{', begin, end) != -1):
            # Devuelvo un par ordenado con las posiciones de las llaves
            return (begin, end)
    
    # Si todo lo demas falla devuelvo un valor absurdo para indicar que tiene
    # un formato invalido
    return (-1, -1) # Valor absurdo


def parseValues(string):
    """
    Devuelve los valores separados por coma del string 
    y sin incluir los espacios
    """
    # Lista valores encontrados
    values = []
    
    # valor encontrado entre cada ','
    aux = ''

    # Por cada caracter en la cadena
    for c in string: 

        # Si el caracter es ',' termina obtener ese elemento
        if c == ',':

            # Verifico que el elemento obtenido, sin los espacios aledanios,
            # no sea una cadena vacia
            if aux.strip() != '':

                # Agrego el elemento obtenido, sin los espacios aledanios, a la
                # lista de valores encontrados
                values.append(aux.strip())
            
            # Reseteo la cadena del elemento obtenido
            aux = ''
        else:
            # Si el caracter NO es ',' lo agrego a la cadena del elemento
            aux += c
            
    # Verifico que el ultimo elemento, sin espacios aledanios, no sea una 
    # cadena vacia
    if aux.strip() != '':
        # Agrego el ultimo elemento sin los espacios aledanios a la lista de
        # valores encontrados
        values.append(aux.strip())

    # Devuelvo la lista de valores encontrados        
    return values


def parseStates(asf, line):
    """Extraigo el conjunto de estado del la linea"""
    
    # Busco la posiciones de las llaves
    begin, end = findBraces(line)
    
    # Si el resultado NO es un valor absurdo 
    if (begin != -1):

        # Obtengos los valores de la sub cadena comprendida entre las llaves
        aux = parseValues(line[begin + 1:end])
        
        try:
            # Convierto cada valor encontrado a un numero entero y lo almaceno
            # como un conjunto en asf["states"]
            asf["states"]= set(map(int, aux))
            
        except ValueError:
            # Si NO se pueve convertir algun elemento de la lista en numero
            # aviso que el formato NO es valido y termino el script
            return False 



def parseInputs(asf, line):
    """Obtengo el conjunto de entradas desde la linea"""

    # Busco la posiciones de las llaves
    begin, end = findBraces(line)
    
    # Si el resultado NO es un valor absurdo 
    if (begin != -1):

        # Obtengos los valores de la sub cadena comprendida entre las llaves
        # y la almaceno como un conjunto en asf["inputs"] 
        asf["inputs"] = set(parseValues(line[begin + 1:end]))


def parseInitState(asf, line):
    """Obtengo el estado inicial desde la linea"""

    # Busco la posiciones de las llaves
    begin, end = findBraces(line)
    
    # Si el resultado NO es un valor absurdo 
    if (begin != -1):

        # Obtengo el valor del estado inicial desde la sub cadena comprendida
        # entre las llaves y la convierto a un numero entero
        init = int(line[begin + 1:end]) # TODO: poner un try
        
        # Verifico que el valor obtenido sea un elemento del conjunto de estados
        if init in asf["states"]:

            # Almaceno el estado inicial en asf["init"]
            asf["init"] = init

        else:
            pass #TODO: hacer algo cuando el formato no coincida

    else:
        pass # TODO: hacer algo cuando el formato no coincida
    


def parseFinalStates(asf, line):
    """Obtengo de la linea el conjunto de estados finales/aceptados"""

    # Busco la posiciones de las llaves
    begin, end = findBraces(line)
    
    # Si el resultado NO es un valor absurdo 
    if (begin != -1):

        # Obtengos los valores de la sub cadena comprendida entre las llaves
        aux = parseValues(line[begin + 1:end])

        try:
            # Convierto cada valor encontrado en un numero entero y lo almaceno
            # en un conjunto
            final = set(map(int, aux))
            
            # Si todos los valores encontrados pertenecen al conjunto 
            # de estados
            if all(estado in asf["states"] for estado in final):
                # Almaceno el resultado en asf["final"]
                asf["final"] = final

            else:
                # los valores encontrados No estan en el conjunto de estados
                # aviso que el formato NO es valido y termino el script
                pass # TODO implementar el caso en que no coincidan
                
        except ValueError:
            # Si algun valor no se puede convertir en numero, aviso que el
            # formato no es valido y termino con el script
            pass # TODO: implementar


def parseTransition(asf, line):
    """Obtengo de la linea la funcion de transicion"""
    """Creo por cada estado un nuevo diccionario con las transiciones"""
    cstates = 0
    state=line[1]
    nrstate='state'+str(state)
    nrstate={}
    for i in xrange(2,len(line)):
    	sigma = line[i+cstates] 
    	state_new = line [i+1+cstates]
    	nrostate[sigma]=state_new
    	cstates= cstates + 2 
    	if states >= len(line) :
    	    break

def parseFile(path):
    """
    Interpreta(?) el archivo, la ruta 'path' debe apuntar a un archivo
    de texto existente
    """

    # Defino un dicionario que representa al automata
    # TODO: buscar otro tipo de dato que contenga estos valores 
    # ¿una clase/objeto?
    asf = { 
        "states": set([]),
        "inputs": set([]),
        "init": -1,
        "final": set([]),
        "transtion": []
    }

    # Defino un dicionario por python no soporta el swich case 
    # y porque son cool
    parsers = {
        # Cuando sea la primera linea del archivo, busco estados
        0: parseStates,

        # Cuando sea la segunda linea del archivo, busco la entradas
        1: parseInputs,

        # Cuando sea la tercera linea del archivo, busco el estado incial
        2: parseInitState,

        # Cuando sea la cuarta linea del archivo, busco los estado finales
        3: parseFinalStates 

        # Solamento las primera cuatro lineas van a estar en el dicionario,
        # las demas se consideran definiciones de transiciones para la funcion 
        # de estado
    }

    # Asocio cada linea del archivo a un numero empezando por cero (0) 
    # y recorro cada linea interpretandola (?)
    for lineNumber, line in enumerate(fileinput.input(path)):
        
        # Busco el interprete(?) correspondiente para el numero de linea en el
        # dicionario. Si NO se encuentra se usa parseTransition
        parser = parsers.get(lineNumber, parseTransition)

        # Ejecuto el interprete(?) correspondiente para la linea
        parser(asf, line)

    # Devuelvo el automata
    return asf


#def cllambda (estados):
#   """ Funcion clausura lambda """
#    pass
#    #l=estados
#    #while length(l) > 0: #aca quiero asumir que la lista l se ira consumiendo a medida que itere
#    #  estados.pop([])


def mover (estado,sigma): #sea sigma un elemento de sigma :P
    """ funcion mover """
    # TODO: implementar
    pass
    

def isValid(asd, input):
    """Check if the input string is acepted by the Automata"""
    # TODO: implementar, devolver True o False
    pass


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
        print ('tp1_punto_uno_ssl.py -i <inputfile> -o <outputfile>')
        
        # Y se finaliza el scritp informando un error 
        # Cuando se finaliza con cualquier nuemero distinto de 0 se considerar
        # que el programa finalizo con errores, en esta caso 2
        sys.exit(2)

    # Por cada par ordenado de opciones-argumentos obtenidos
    for opt, arg in opts:

        # Si la opcion es '-h' 
        if opt == '-h':

            # se informa la forma de uso correcto
            print ('tp1_punto_uno_ssl.py -i <inputfile> -o <outputfile>')

            # Se finaliza el scritp sin error
            sys.exit()

        # Si la opcion es '-a' o '--automata'
        elif opt in ("-a", "--automata"):
            # el argumento asociado es la ruta al archivo txt con el automata
            # a parsear/interpretar/(?)
            path = arg

        # Si la opcion es '-s' o '--string'
        elif opt in ("-s", "--string"):
            # el argumento asociado es la cadena que se debe verificar si es 
            # aceptada por el automata
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
                print ("La cadena es aceptada por el automata") #TODO: mejorar el mensaje

            else:
                # Informo que NO es aceptada
                print ("La cadena NO es aceptada por el automata") #TODO: mejorar el mensajepyt
        else:
            # leer las cadena que ingresa el usuario y chekear si cada una es 
            # aceptada por el automata
            print ("implementame (?)") # TODO implementar

    else:
        # Si la ruta no es valida o no corresponde a un archivo
        print ("El archivo no es valido") # TODO: mejorar mensaje de error


# Si el scritp es llamado directamente (Osea NO es importado como libreria)
if __name__ == "__main__":
    # Ejecuto el proceso principal con los argumentos exepto el primero que es 
    # el nombre del scritp
    main(sys.argv[1:])
    
    
