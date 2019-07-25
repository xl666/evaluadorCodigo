
"""
"""

import socket
import threading
import subprocess
import datetime
from collections import namedtuple
import os
import random

IpPuerto = namedtuple('IpPuerto', 'ip puerto')

def notificar(data):
    mensaje = '%s: %s' % (datetime.datetime.now(), data)
    subprocess.call(['kdialog', '--msgbox', mensaje])
    print(mensaje)

def ipInIpsPuertos(ip, ipsPuertos):
    elementos = list(filter(lambda x: ip in x, ipsPuertos))
    if elementos:
        return elementos[0]
    return None

def get_puertos_usados():
    salida = subprocess.Popen('nmap -sT -T 5 -p - localhost | egrep -o "^[0-9]{1,4}"',
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    stdout, _ = salida.communicate()
    partes = stdout.split(b'\n')
    return [int(puerto) for puerto in partes if puerto]

def get_puerto_libre():
    usados = get_puertos_usados()
    todos = range(65536)
    while True:
        puerto = random.choice(todos)
        if not puerto in usados:
            return puerto

def lanzar_contenedor(ip, ipsPuertos):
    comando = 'docker run --rm -d -p %s:7681 cplus2ttyd'
    ipPuerto = ipInIpsPuertos(ip, ipsPuertos)
    if ipPuerto:
        return ipPuerto
    puerto = get_puerto_libre()
    print('Lanzando contenedor en puerto %s' % puerto)
    os.system(comando % puerto)
    return IpPuerto(ip, puerto)

class Monitor():
    def __init__(self, port=9030):        
        self.port = port
        self.lock = threading.Lock()
        self.ipsPuertos = set()
        
        
    def run(self):
        """
        crear socket de servicio
        """
        mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        mySocket.bind(('', int(self.port)))  # binds to any available interface
        print('listenning on port: %s' % self.port)
        mySocket.listen(5)
        while True:
            conn, _ = mySocket.accept()
            attendThread = WorkThread(conn, self.lock, self.ipsPuertos) # se crea un hilo de atención por cliente
            attendThread.start()

            
class WorkThread(threading.Thread):  # it is actually a subprocess
    def __init__(self, conn, lock, ipsPuertos):
        self.conn = conn
        self.lock = lock
        self.ipsPuertos = ipsPuertos
        self.eventos = {'notificar': notificar, 'lanzar': lanzar_contenedor}
        threading.Thread.__init__(self)

    def run(self):
        data = b''
        while not data.endswith(b'$$$'): # read message
            chunck = self.conn.recv(1024)
            data += chunck
            if not chunck: #finished
                break
        if not data:
            raise RuntimeError("No se transmitieron datos")
        data = data[:-3] # quitar $$$
        
        if data.startswith(b'notificar:'):
            data = data[10:]
            self.eventos['notificar'](data)

        if data.startswith(b'lanzar:'):
            data = data[7:]
            ipPuerto = self.eventos['lanzar'](data, self.ipsPuertos)
            self.lock.acquire()
            self.ipsPuertos.add(ipPuerto)
            self.lock.release()
            self.conn.send(str(ipPuerto.puerto).encode('utf-8'))

if __name__ == '__main__':
    dem = Monitor()
    dem.run()

