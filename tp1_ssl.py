# {0,1,2}
# {a,b}
# {0}
# {1,2}
# 0a1b2&0#
# 1a1b0#
# 2a2b2#
# especificacion del automata
# deberia poder parsear el texto que se da como entrada
# de la linea 1 a 4 se dan los elementos fijos que son 
# linea 1 : el conjunto de estado
# linea 2: el conjunto de entradas
# linea 3 : el estado inicial
# linea 4 : los estados aceptados
# a continuacion abro el archivo de texto y comiendo a parsear
entrada = open("ej-especif-aut.txt", "r") 
#sabiendo que de la linea 1 a 4 estan los datos que son fijos hacer
for i in range (4):
    content=entrada.readline()
    print content
# parseo la funcion de transicion
# se que el eol es un hash

    
