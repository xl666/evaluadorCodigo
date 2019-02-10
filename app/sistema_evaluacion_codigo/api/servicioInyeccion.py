#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
import socket
import multiprocessing
import subprocess
import datetime
import sys
# import daemon
# import lockfile

class Monitor():
    def __init__(self, port=9030):
        self.port = port
        self.lock = multiprocessing.Lock()


    def run(self):
        """
        crear socket de servicio
        """
        mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        mySocket.bind(('', int(self.port)))  # binds to any available interface
        print('recibiendo peticiones en puerto: %s' % self.port)
        mySocket.listen(5)
        while True:
            conn, addr = mySocket.accept()
            attendThread = WorkThread(conn, addr) # se crea un hilo de atención por cliente
            attendThread.start()


class WorkThread(multiprocessing.Process):  # it is actually a subprocess
    def __init__(self, conn, addr):
        self.conn = conn
        self.addr = addr
        multiprocessing.Process.__init__(self)

    def run(self):
        data = ''
        # Se reciben 3 cosas en la serializacion: ruta programa, entrada, tiempoMaximo
        # Cada parte se separa por &&
        # El final de la cadena es $$$
        while not data.endswith('$$$'): # read message
            chunck = self.conn.recv(1024).decode()
            data += chunck
            if not chunck: #finished
                break
        if not data:
            raise RuntimeError("No se transmitieron datos")
            self.conn.sendall("('API error', 1)$$$".encode())
            return
        data = data[:-3] # quitar $$$
        partes = data.split('&&')
        if not len(partes) == 3:
            self.conn.sendall("('API error', 1)$$$".encode())
            return
        programa, entrada, maxTime = tuple(partes)
        try:
            tiempo = int(maxTime)
        except:
            self.conn.sendall("('API error', 1)$$$".encode())
            return
        salida = inyect(programa, entrada, int(maxTime))
        # responder algo
        mensaje = str(salida) + '$$$'
        self.conn.sendall(mensaje.encode())

#usar el encoding por defecto
encoding = sys.getdefaultencoding()


def inyect(programa, entrada, maxTime=2): # 2 segundos máximos
    """
    Inyecta una entrada a un programa dado y regresa una tupla con la salida y un codigo de salida
    Hace un chequeo para saber si ejecutarlo con un interprete
    """
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


if __name__ == '__main__':
    dem = Monitor(sys.argv[1])
    dem.run()
        
