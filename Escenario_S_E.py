# Ejercicio numero 1

"""
Funcion DNI : Esta funcion toma como argumento la trama de datos obtenida mediante la lectura de un QR y devuelve el DNI del usuario,
retorna 2 listas ,la primera lista son las posiciones donde se encuentra la palabra 'COL',la segunda lista es  la posicion donde se encuentra el string 
'<2', y retorna el valor ingresado como parametro inicial.

Args: string.

Returns : 2 listas y el valor que se ingreso como parametro inicial.

"""
def DNI(value):

    posicion = -1
    posiciones = []

    while True:
        posicion = value.find('COL', posicion + 1)
        if posicion == -1:
            break
        posiciones.append(posicion)

    posc_2 = -1
    posc = []

    while True:
        posc_2 = value.find('<2',posc_2 + 1)
        if posc_2 == -1:
            break
        posc.append(posc_2)
    return posiciones,posc,value


# Se guarda en variables indepenientes los valores que retorno la funcion DNI donde:
# value_DNI tomara la lista donde se encuentra el string 'COL'
# end_DNI tomara la lista donde se encuentra el string '<2'
# value_Inicial tomara el parametro inicial 
value_DNI,end_DNI,value_Inicial = DNI("01ICCOLO01121047415001<<<<<<<<<< 9210181M3110278COL1030432234<2 PEPITO<PEREZ<<DIOMEDES<DANIEL<<<<")

# Se realiza un recorte del string almacenado en 'value_Inicial' entre el valor que tiene la lista value_DNI en la posicion 1 y el valor
# alamacenado en end_DNI en la posicion 0 
x=value_Inicial[(value_DNI[1]+3):end_DNI[0]]

# Imprime el valor obtenido despues del recorte realizo 
print(f"El DNI del usuario es: {x}")

"""
Elabore un script en su lenguaje preferido para simular la comunicación entre un dispositivo IoT y el sistema Cloud explicando la lógica 
para enviar datos.


"""