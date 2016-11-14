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
# ANIO 2016                                   #
###############################################   

import os.path
import fileinput
import sys, getopt

import tp1_punto_uno_ssl as tp1

from functools import partial

# Contenido del archivo a parsear: 
# {A,B}
# {a,b,c,(,)}
# {A}
# A->(A)Ba
# A-> Bb
# B->a
# B->b
# B->ccc

# Explicacion:
#   De la linea 1 a la 3 son elementos fijos :
#       Conjunto de No terminales
#       Conjunto de Terminales
#       Simbolo destacado - Simbolo inicial
#   Las demas lineas son Producciones

def findArrow(string):
    """ 
    Devuelve la posicion donde empieza y donde termina la '->' y
    verifica que el string no empice con la flecha
    """
    # Busco el primer resulatdo de ->
    begin = string.find("->")

    # calculo la posicion del segundo caracter
    end = begin + 1

    # Si no se encontro la flecha o no hay nada antes
    if (begin <= 0):
        #Se devuelve un valor absurdo
        return (-1, -1)

    # Si todo va bien devuelvo los valores encontrados
    return (begin, end)



def parseV(cjtoDestino, gramatica,line):
    """ Extraigo el conjunto de simbolos de la linea """
    
    # Busco la posiciones de las llaves
    begin, end = tp1.findBraces(line)
    
    # Si el resultado NO es un valor absurdo 
    if (begin != -1):

        # Obtengos los valores de la sub cadena comprendida entre las llaves
        # y la almaceno como un conjunto en la gramatica
        gramatica[cjtoDestino]= set( tp1.parseValues(line[begin + 1:end]) )


def parseInitState(gramatica, line):
    """Obtengo el simbolo inicial desde la linea"""

    # Busco la posiciones de las llaves
    begin, end = tp1.findBraces(line)
    
    # Si el resultado NO es un valor absurdo 
    if (begin != -1):

        # Obtengo el valor del simbolo inicial desde la sub cadena comprendida
        # entre las llaves y la convierto a un numero entero
        init = line[begin + 1:end].strip()
        
        # Verifico que el valor obtenido sea un elemento del conjunto de estados
        if init in gramatica["VN"]:

            # Almaceno el estado inicial en gramatica["init"]
            gramatica["sInit"] = init

        else:
            pass #TODO: hacer algo cuando el formato no coincida

    else:
        pass # TODO: hacer algo cuando el formato no coincida
    

def parseProducciones(meta, prodsNumeradas, gramatica, line):
    """ Obtengo las producciones desde la linea """
    
    # Busco la posiciones de la flecha
    begin, end = findArrow(line)

    # Si el resultado NO es un valor absurdo 
    if (begin != -1):

        # Hago un chache de VN y VT
        vn = gramatica["VN"]
        vt = gramatica["VT"]

        # Creo la union de VN y VT
        v  = vn.union(vt)

        # Hago cache a la cantidad Producciones
        cantProds = meta["cantProds"]

        # Obtengo el lado izquierdo
        ladoIzquierdo = line[0:begin].strip()

        # Obtengo el lado derecho
        ladoDerecho = line[(end + 1):].strip()

        # Si el lado izquierdo NO es una cadena vacia y 
        # pertenece a los simbolos NO terminales
        if (ladoIzquierdo != '') and ( ladoIzquierdo in vn ):

            # Obtengo las producciones asociadas a este lado izquierdo
            # Si NO es encuentra obtengo una lista vacia
            li_prods = gramatica["prods"].get(ladoIzquierdo, [])

            # Si el lado derecho NO es una cadena vacia y 
            # pertenece a los simbolos Terminales
            if (ladoDerecho != '') and all(simbolo in v for simbolo in ladoDerecho ):

                # Si el lado derecho No esta en las producciones assiocadas al lado izquierdo
                if not ladoDerecho in li_prods:

                    # Agregro el lado derecho a las produciones
                    li_prods.append(ladoDerecho)

                    # Actualizo la lista de producciones asoiciadas
                    gramatica["prods"][ladoIzquierdo] = li_prods

                    # Incremento la cantidad de producciones
                    cantProds += 1

                    # Agrego la nueva produccion numerada
                    prodsNumeradas[cantProds] = (ladoIzquierdo, ladoDerecho)

                    # Almaceno el estado la nueva cantidad de producciones
                    meta["cantProds"] = cantProds


            else:
                pass # TODO: tirar error cuando el formato NO coincida

        else:
            pass # TODO: tirar error cuando el formato NO coincida


def parseFile(path):
    """ 
    Leeo la gramatica desde el archivo y la valido
    Devuelvo dicionario con la gramatica y diccionario con las producciones numeradas
    """

    gramatica = {
        "VN": set([]), # no terminales
        "VT": set([]), # terminales
        "sInit": "",   # simbolo inicial
        "prods": {}    # producciones: {ladoIzquierdo: [ladosDerechos] }
    }

    # ProduccionesNumeradas {numero: produccionN}
    # ProduccionN (ladoIzquierdo, ladosDerechos)
    prodsNumeradas = {}

    # Numero de producciones encontradas hasta el momento
    # uso diccionario como wapper para que sea mutable
    meta = { "cantProds": 0 }

    # Defino un dicionario por python no soporta el swich case 
    # y porque son cool
    parsers = {
        # Cuando sea la primera linea del archivo, busco Simbolos NO terminales
        0: partial(parseV, "VN"), # aplicacion parcial para el primer termino

        # Cuando sea la segunda linea del archivo, busco Simbolos Terminales
        1: partial(parseV, "VT"), # aplicacion parcial para el primer termino

        # Cuando sea la tercera linea del archivo, busco el simbolo incial
        2: parseInitState,

        # Solamento las primera tres lineas van a estar en el dicionario,
        # las demas se consideran definiciones de producciones
    }

    # Asocio cada linea del archivo a un numero empezando por cero (0) 
    # y recorro cada linea interpretandola (?)
    for lineNumber, line in enumerate(fileinput.input(path)):
        
        # Busco el interprete(?) correspondiente para el numero de linea en el
        # dicionario. Si NO se encuentra se usa parseProducciones
        # uso una aplicacion pracial en parseProducciones
        parser = parsers.get(lineNumber, partial(parseProducciones, meta, prodsNumeradas))

        # Ejecuto el interprete(?) correspondiente para la linea
        parser(gramatica, line)

    # Devuelvo el automata
    return (gramatica, prodsNumeradas)


def clausure(gramatica, cjtoItems):
    """ Genera la clasura del conjuntu de items de salida """

    # formato de items (lado izquierdo, lado derecho, posicion punto)

    # cacheo los valores y redusco la verbosidad
    vn    = gramatica.get("VN")
    prods = gramatica.get("prods")
    
    # Creo una lista ordenada con los items del conjunto
    listaItems = sorted(cjtoItems)
    
    # un indice para indicar que item estoy analizando
    idx = 0

    ##
    # "Mientras alla items sin marcar" 
    # - Teoria
    #
    # "Mientras el NO alla finalizado de recorrer la lista mutable y
    # NO alla explotado la memoria en un loop infinto inentencional (?)"
    # - Practica
    ##
    while (idx < len(listaItems)):
        
        # Creo un alias al item apuntado
        item = listaItems[idx]

        # Hago legible para mi mente los valores del item que voy a usar
        ladoDerecho = item[1]
        posPunto    = item[2]

        # Mientras NO sea un item completo
        if ( posPunto < len(ladoDerecho) ): 

            # obtengo el simbolo que le sigue al punto
            simboloApuntado = ladoDerecho[posPunto]

            # Si el simbolo esta en el conjunto de los NO Terminales
            if ( simboloApuntado in vn ):

                # Obtengo todos los lados derechos de las producciones 
                # del simbolo apuntado (NO Terminal)
                ladosDerechos = prods.get(simboloApuntado)

                # Para todos los lados derechos
                for ld in ladosDerechos:

                    # Creo un item
                    nuevoItem = (simboloApuntado, ld, 0)

                    # Si el item NO esta en la lista de items
                    if ( not nuevoItem in listaItems ):

                        # Lo agrego a la lista
                        listaItems.append(nuevoItem)
                
        # Incremento idx sino explota todo
        idx += 1

    # TODO: Probar, testear, test me, cosa

    # Convierto la lista en un conjunto
    return set(listaItems)


def calcuarSimbolosDeDesplazamiento(gramatica, cjtoItems):
    """ Calcula el subconjunto de V cuyos elementos pueden ser usados con gotoL """

    # formato de items (lado izquierdo, lado derecho, posicion punto)

    # cacheo los valores y redusco la verbosidad
    vt    = gramatica.get("VT")
    vn    = gramatica.get("VN")
    
    # Creo una lista ordenada con los items del conjunto
    listaItems = sorted(cjtoItems)

    # creo un conjunto vacio
    resultado = set()

    # Para cada item en el conjunto
    for item in cjtoItems:
        
        # Hago legible para mi mente los valores del item que voy a usar
        ladoDerecho = item[1]
        posPunto    = item[2]

        # Mientras NO sea un item completo
        if ( posPunto < len(ladoDerecho) ): 

            # Obtengo el simbolo apuntado
            simbolo = ladosDerechos[posPunto]

            # Agrego el item al conjunto
            resultado.add(simbolo)

    # Un poco de paranoia no hace mal :V
    assert resultado.issubset( vn.union(vt) ), "El resultado N= es un subconjunto de V!"
    
    # TODO: probar, testear, test me, cosa

    # Devuelvo el resultado Duh!
    return resultado


def goto(cjtoItems,caracter):
    
    #defino una variable donde voy a poner los items finales que van a estar en la clausura
    listaAClausurar = []
    
    #defino una variable auxiliar donde voy a poner todos los items pertenecientes al conjunto en los cuales el punto este antes del caracter
    aux = []

    #para todos los items del conjunto
    for item in cjtoItems:
        
        #pregunto si el caracter esta adelante del punto
        if item[1][item[2]]== caracter:
            
            #agrego el item a un conjunto para seguirlo analizando despues
            aux.append(item)

    #para todos los items que cumplen la condicion
    for item in aux:
        
        #le adelanto el punto al item
        itemAAnalizar = (item[0],item[1],item[2]+1)

        #agrego este nuevo item a la lista que se va a clausurar
        listaAClausurar.append(itemAAnalizar)

    #hago la clausura de este conjunto que tiene todos los items con el punto adelante del caracter con el que estamos haciendo el goto
    return clausure(gramatica,listaAClausurar)


def agregarProduccionAuxiliar(gramatica, prodsNumeradas):
    """
    Agrego una produccion auxiliar del tipo: E' -> E#
    """

    # cacheo VN y VT
    vn = gramatica["VN"]
    vt = gramatica["VT"]

    # genero V
    v = vt.union(vn)

    # para almacener el No Terminal auxiliar
    nuevoVN = ''

    # Busco un simbolo libre para usar de auxiliar
    if not 'E' in v:
        nuevoVN = 'E'

    elif not 'S' in v:
        nuevoVN = 'S'

    elif not '$' in v:
        nuevoVN = '$'

    elif not '&' in v:
        nuevoVN = '&'

    else:
        print("Que gramatica mas jodida :V")

        # TODO: reemplazar esto con una excepcion(?) o lo que corresponda
        assert False, "NO se encontro un caracer libre para el auxiliar"

    # Agrego el auxiliar a VN
    gramatica["VN"].update(nuevoVN)

    # guardo el simbolo incial original 
    sInit = gramatica["sInit"]    
    
    # Verifico que # no se encuentre definida en la gramatica original
    assert not '#' in v, "# ya esta definida en la gramatica original"

    # Genero el lado derecho de la produccion auxiliar
    ladoDerecho = sInit + '#'

    # Agrego la produccion auxiliar
    gramatica["prods"][nuevoVN] = [ladoDerecho]

    # Cambio el simbolo inicial
    gramatica["sInit"] = nuevoVN

    # Agrego la produccion numera en un lugar que se que esta vacio
    prodsNumeradas[-1] = (nuevoVN, ladoDerecho)



def seguimiento(produccionesNumeradas, tabla, cadena):
    """ devuelve true o false si la acepta o no """

    # El numero de las producciones usadas
    produccionesUsadas = []

    # Flag con el resultado del analisis
    cadenaEsAcepta = False

    # Flag de error
    error = False

    # Inicio la pila en q0
    pila = [0]

    #para cada caracter de la cadena
    for contador, carcater in enumerate(cadena):
        
        desplazar = False

        # En caso de error
        if error:
            # Rompo el for loop
            break

        # Assercion por la NO se termino de recorrer la cadena y se indico como aceptada
        assert cadenaEsAcepta, "La cadena ya esta aceptada NO debiria seguir ejecutandose"

        # para NO avanazar hasta que el la flad diga lo contrario
        while not desplazar and not error:

            # Me fijo en el tope de la tabla
            estado = pila[-1]

            #me fijo que es lo que tengo que hacer cuando estoy en ese estado y me entra ese caracter
            #esto devuelve el par que mande por whatsapp
            accion = tabla(estado, caracter)

            # Asercion, un estado y un terminal nunca puede dar una accion 'm'
            assert accion[0] != 'm', "La accion mover nunca debe ser usada en este punto"
        
            if accion[0] == 'd':
                # Agrego el estado a la pila
                pila.append(accion[1])

                # Avanzo al siguiente elemento de la cadena
                desplazar = True

            elif accion[0] == 'r':  
                #reducir:       

                # Obtengo las producciones
                produccion = produccionesNumeradas[accion[1]]

                # Obtegengo el lado derecho de la produccion
                ladoDerecho = producion[1]

                # Obtengo la longitud del lado derecho
                n = len(ladoDerecho)

                # elemino los n ultimos de la pila
                for i in xrange(n):
                    pila.pop()

                # Agrego el numero de la produccion usada para la reduccion
                produccionesUsadas.append(accion[1])

                # Obtegengo el lado izquierdo de la produccion
                ladoIzquierdo = producion[0]

                # Obtengo la accion para el lado izquierdo
                accion = tabla(estado, ladoIzquierdo)

                # Asercion, la accion 'm' solo se debe usar aca
                assert accion[0] == 'm', "la accion siempre tiene que ser mover en este punto"

                # Agrego el estado a la pila
                pila.append(accion[1])

                # indico que NO me deplazo
                desplazar = False
                
            elif accion[0] == 'a':
                #aceptar
                cadenaEsAcepta = True

                # Para romper el while loop
                desplazar = True

            else : 
                #cancelar
                cadenaEsAcepta = False

                # Para romper el while loop
                error = True
                

    # Devuelvo si la cadena es aceptado y las producciones usadas para crear la cadena (si corresponde)
    return (cadenaEsAcepta, produccionesUsadas)


def estrategiaIncreible(gramatica, prodsNumeradas):
    """ Genera "LA TABLA" """

    # TODO: implementar. (devolver tabla)
    # ProduccionesNumeradas {numero: produccion}
    # Produccion (ladoIzquierdo, ladosDerechos)
    # Tabla (dicionarios de diccionarios): {"estado": { simboloA: accion, simboloB: accion }}
    # Accion ("incial de la accion", "item o produccion sobre la cual hacer la accion")

    pass


def evaluarCadena(gramatica, laTabla, cadena):
    """ Evalua la cadena de entrada y muestra que producciones se usaron para crearla """

    # TODO: implementar. (devolver como se derivo de la cadena, indicando producciones usadas)

    pass


def main(argv):
    """Proceso principal"""

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
        gramatica, produccionesNumeradas = parseFile(path)

        # Imprimo el resultado del parseo (me canse)
        print (gramatica) 
        print ('')
        print (produccionesNumeradas)
        print ('')

        # Agrego la produccion auxiliar
        agregarProduccionAuxiliar(gramatica, produccionesNumeradas)

        # Imprimo el resultado (for debug)
        #print ('Gramatica con produccion auxiliar')
        #print (gramatica) 
        #print ('')
        #print (produccionesNumeradas)
        #print ('')

        # Genero "LA TABLA"
        laTabla = estrategiaIncreible(gramatica, produccionesNumeradas)

        # Imprimo la tabla generada
        print (laTabla)

        # Si se dispone a cadena a comprobar
        if (withString):

            # Verifico que la cadena sea aceptada
            if (evaluarCadena(gramatica, laTabla, inputString + '#')):
                # Informo que es aceptada
                print ("La cadena es generada por la gramatica") 

            else:
                # Informo que NO es aceptada
                print ("La cadena NO es generada por la gramatica") 
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

    