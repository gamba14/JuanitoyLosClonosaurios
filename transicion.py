cero = { 'a' : 1 , 'b' : 2 ,'&' : 0 }
uno  = { 'a' : 1 , 'b' : 0 }
dos  = { 'a' : 2 , 'b' : 2 }
states = [cero ,uno ,dos ]
#supongo que esto ya viene parseado desde el archivo inicial
cadena=input()
state_i= 0

for c in cadena :
    aux=states[state_i][c]
    state_i = aux
if state_i == 1 or 2:
	print("cadena valida")
else:
	print("cadena no valida")




    