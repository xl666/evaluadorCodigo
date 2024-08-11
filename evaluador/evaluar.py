import subprocess
import sys

CASE_BREAK = '$$$$$$'
INPUT_BREAK = '!!!!!!'

encoding = sys.getdefaultencoding()

def evaluar(programa, arCasos, maxTime=5):
    entrada = ''
    salida = []
    salidaEsperada = ''
    outputEval = False
    res = ""
    for line in open(arCasos):
        messyLine = line #no quitar saltos de línea ni nada, para comparar con salida esperada (tienen que ser exactametne iguales)
        line = line.strip() #quitar saltos de línea al final así como espacios extra, para evitar posibles errores en el input y facilitar el proceso

        if(line == CASE_BREAK and salida == []): #es la primera línea
            continue

        if(line == ''): #ignorar líneas vacías
            continue

        if line == INPUT_BREAK: #dejar de llenar la entrada he inyectar
            salida = evaluar_caso(programa, entrada, maxTime)
            outputEval = True
            entrada = '' #restart input

        elif line == CASE_BREAK: #cambiar banderas y evaluar
            outputEval = False
            if salida[1] != 0: # 0 es sin errores
                res += str(salida[0]) + "$#"
            elif salida[0] == salidaEsperada or salida[0].strip() == salidaEsperada.strip(): #sometimes the new lines must be preserved
                res += "true$#"
            else:
                res += "false$#"
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

def evaluar_caso(programa, entrada, maxTime=2):
    print(f'programa: {programa}  entrada: {entrada}')
    partes = programa.split('.') #ver si el programa tiene una extension
    if len(partes) > 0:
        if(partes[-1] == 'fasl'): #sbcl lisp
            programa = 'sbcl --noinform --load %s --quit --disable-debugger --end-toplevel-options $@' % programa
        elif(partes[-1] == 'py'): #python
            programa = 'python %s' % programa
        elif(partes[-1] == 'prolog'): #prolog
            programa = 'swipl -f %s -t main -q' % programa
        elif(partes[-1] == 'class'):
            #quitar .class
            programa = programa[:programa.index('.class')]
            #crear classpath
            pps = programa.split('/')
            dire = ''
            for pp in pps[:-1]:
                dire += (pp + '/')
            programa = pps[-1]
            programa = 'java -cp %s %s' % (dire, programa)
    try:
        process = subprocess.Popen(programa.split(), stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
        tup = process.communicate(bytes(entrada, encoding), maxTime)
        output = str(tup[0], encoding) #0 es la salida por defecto
        if process.returncode != 0: #an error ocurred in child process
            #return (str(tup[1],encoding),1) #1 means an error, tup[1] is the error stream
            print(tup[1])
            return ('Runtime error',1)
    except subprocess.TimeoutExpired: #the process is taking too long
        process.kill() #the process must be killed if don't it keps running
        return ('Time exceeded',1)
    except:
        return (sys.exc_info()[0], 1) #any error
    if(partes[-1] == 'fasl'): #sbcl lisp
        output = output.strip() #for some reason sbcl print always ads a \n at the begining and space at the end
    return (output,0) # 0 means no errors