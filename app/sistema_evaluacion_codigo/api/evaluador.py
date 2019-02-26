
from . import inyectar


CASE_BREAK = '$$$$$$'
INPUT_BREAK = '!!!!!!'

def evaluar(programa, arCasos, maxTime=5, puertoInyeccion=9030):
    """
    Programa ya es el compilado o script
    maxTime es para establecer en segundos el tiempo máximo de ejecución
    Cada caso se separa por la cadena especiasl $$$$$$$
    La entrada se separa de la salida por la cadena especial !!!!!!
    """
    entrada = '' #la cadena total que se enviara
    salida = [] #para tenerla declarada por si el scope
    salidaEsperada = '' #para ir guardando lo que se lee en el archivo
    outputEval = False #se activa cuando se evalua el output
    res = []  #para guardar los resultados de cada caso
    for line in open(arCasos):
        messyLine = line #no quitar saltos de línea ni nada, para comparar con salida esperada (tienen que ser exactametne iguales)
        line = line.strip() #quitar saltos de línea al final así como espacios extra, para evitar posibles errores en el input y facilitar el proceso

        if(line == CASE_BREAK and salida == []): #es la primera línea
            continue

        if(line == ''): #ignorar líneas vacías
            continue

        if line == INPUT_BREAK: #dejar de llenar la entrada he inyectar
            salida = inyectar.inyect(programa, entrada, maxTime, puertoInyeccion)
            outputEval = True
            entrada = '' #restart input

        elif line == CASE_BREAK: #cambiar banderas y evaluar
            outputEval = False
            if salida[1] != 0: # 0 es sin errores
                res.append(salida[0]) #el tipo de error
            elif salida[0] == salidaEsperada or salida[0].strip() == salidaEsperada.strip(): #sometimes the new lines must be preserved
                res.append(True)
            else:
                res.append(False)
            salidaEsperada = '' #restart output

        elif outputEval:
            salidaEsperada += messyLine

        else: #input reconstruction
            if line.strip().startswith('['): #si es una lista prolog no se quieren saltos de linea
                entrada += line + '\n'
            else:
                for elem in line.split(','):
                    entrada += elem + '\n'

    return res



