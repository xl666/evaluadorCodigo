
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
SIMBOLOS = [chr(c) for c in range(65, 91)] + [chr(c) for c in range(97, 123)] + [str(i) for i in range(10)]


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

def lanzar_contenedor(ip, ipsPuertos, token):
    if not token:
        raise Exception('No se puede iniciar el contenedor sin un token')
    comando = 'docker run --rm -d -p %s:7681 -e TOKEN=%s cplus2ttyd'
    ipPuerto = ipInIpsPuertos(ip, ipsPuertos)
    if ipPuerto:
        return ipPuerto
    puerto = get_puerto_libre()
    print('Lanzando contenedor en puerto %s' % puerto)
    os.system(comando % (puerto, token))
    return IpPuerto(ip, puerto)

def gen_token(longitud=10):
    res = ''
    for i in range(longitud):
        res += random.choice(SIMBOLOS)
    return res

def get_token(ip, dictTokens):
    if ip in dictTokens.keys():
        return dictTokens[ip]
    while True:
        token = gen_token()
        if not token in dictTokens.values():
            return token
    assert False # imposible

class Monitor():
    def __init__(self, port=9030):        
        self.port = port
        self.lock = threading.Lock()
        self.ipsPuertos = set()
        self.dictTokens = {}
        
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
            attendThread = WorkThread(conn, self.lock, self.ipsPuertos, self.dictTokens) # se crea un hilo de atención por cliente
            attendThread.start()

            
class WorkThread(threading.Thread):  # it is actually a subprocess
    def __init__(self, conn, lock, ipsPuertos, dictTokens):
        self.conn = conn
        self.lock = lock
        self.ipsPuertos = ipsPuertos
        self.dictTokens = dictTokens
        self.eventos = {'notificar': notificar, 'lanzar': lanzar_contenedor,
                        'darToken': get_token}
        threading.Thread.__init__(self)

    def notificar(self, data):
        data = data[10:]
        self.eventos['notificar'](data)

    def lanzar(self, data):
        data = data[7:]
        self.lock.acquire()
        try:
            ipPuerto = self.eventos['lanzar'](data, self.ipsPuertos, self.dictTokens.get(data.decode('utf-8'), None))
            self.ipsPuertos.add(ipPuerto)
        except:
            raise
        finally:
            self.lock.release()
        self.conn.send(str(ipPuerto.puerto).encode('utf-8'))

    def darToken(self, data):
        data = data[9:]
        self.lock.acquire()
        token = self.eventos['darToken'](data.decode('utf-8'), self.dictTokens)
        self.dictTokens[data.decode('utf-8')] = token
        self.lock.release()
        self.conn.send(token.encode('utf-8'))
        
    def run(self):
        data = b''
        try:
            while not data.endswith(b'$$$'): # read message
                chunck = self.conn.recv(1024)
                data += chunck
                if not chunck: #finished
                    break
            if not data:
                raise RuntimeError("No se transmitieron datos")
            data = data[:-3] # quitar $$$
            
            if data.startswith(b'notificar:'):
                self.notificar(data)
            if data.startswith(b'lanzar:'):
                self.lanzar(data)

            if data.startswith(b'darToken:'):
                self.darToken(data)
        except:
            raise
        finally:
            self.conn.close()

if __name__ == '__main__':
    dem = Monitor()
    dem.run()

