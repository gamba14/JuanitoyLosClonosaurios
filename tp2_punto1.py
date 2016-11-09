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

def parseFile(path):
    """ Leeo la gramatica desde el archivo y la valido """

    gramatica = {
        "VN": set([]), # no terminales
        "VT": set([]), # terminales
        "sInit": "",   # simbolo inicial
        "prods": []    # produciones: {ladoIzquiendo: [ladosDerechos] }
    }

    # TODO: implementar. (llenar el dicionario anterior)

    pass


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


def gotoL(gramatica, cjtoItems, simbolo):
    """ Calcula el siguiente conjunto de items para el simbolo de entrada """

    #TODO: implementar. (conjunto de items)
    	for item in cjtoItems:

      		if length(item[1]) > (item[2]):

    			pass #TODO aca me tiene que devolver el item sin variar
    				#ya que es un item completo
    		else:		
    			#como no era un item completo
    			#corro el punto un lugar a la derecha
    			item[2] += 1

    			#ahora me quiero quedar con las partes que me interesan
    			#para hacer la clausura

    			ladoIzquierdo=item[0]
    			ladoDerecho=item[1]

    			next = ladoDerecho[item[2]]

    			#TODO la clausra con next y el simbolo que entro
    			# es recursivo?






    


def estrategiaIncreible(gramatica):
    """ Genera "LA TABLA" """

    # TODO: implementar. (devolver tabla)
    # Tabla (dicionarios de diccionarios): {"estado": { simboloA: accion, simboloB: accion }}

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
        gramatica = parseFile(path)

        # Imprimo el resultado del parseo (me canse)
        print (gramatica) 

        # Genero "LA TABLA"
        laTabla = estrategiaIncreible(gramatica)

        # Imprimo la tabla generada
        print (laTabla)

        # Si se dispone a cadena a comprobar
        if (withString):

            # Verifico que la cadena sea aceptada
            if (evaluarCadena(gramatica, laTabla, inputString)):
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

    