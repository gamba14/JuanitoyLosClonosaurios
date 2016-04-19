# {0,1,2}
# {a,b}
# {0}
# {1,2}
# 0a1b2&0#
# 1a1b0#
# 2a2b2#
# de la linea 1 a 4 se dan los elementos fijos que son 
# linea 1 : el conjunto de estado
# linea 2: el conjunto de entradas
# linea 3 : el estado inicial
# linea 4 : los estados aceptados
###################################################################################################
# a continuacion abro el archivo de texto 
###################################################################################################
entrada = open("ej-especif-aut.txt", "r")
###################################################################################################



#deberia definir como son las transiciones ya que las voy a necesitar cuando haga clausura lambda


###################################################################################################
#funcion clausura lambda
###################################################################################################
def cllambda (estados):
    l=estados
    while length(l) > 0: #aca quiero asumir que la lista l se ira consumiendo a medida que itere
    	estados.pop([])



###################################################################################################
# funcion mover
###################################################################################################
def mover (estado,sigma): #sea sigma un elemento de sigma :P


#sabiendo que de la linea 1 a 4 estan los datos que son fijos hacer (va mas arriba lo se)
for i in range (4):
    content=entrada.readline()
    print content
# parseo la funcion de transicion
# se que el eol es un hash
    
