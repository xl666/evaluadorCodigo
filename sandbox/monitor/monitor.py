
import accessPointInfo

import socket
import threading
import subprocess
import datetime
from collections import namedtuple
import os
import random
import sys

MacPuerto = namedtuple('MacPuerto', 'mac puerto')
SIMBOLOS = [chr(c) for c in range(65, 91)] + [chr(c) for c in range(97, 123)] + [str(i) for i in range(10)]

class AlumnoInexistente(Exception):
    pass


def getMacIp(ip):
    ipMacs = accessPointInfo.getIPMacsConectados()
    mac = accessPointInfo.getMacIp(ip, ipMacs)
    return mac

def notificar(data):
    mensaje = '%s: %s' % (datetime.datetime.now(), data)
    subprocess.call(['kdialog', '--msgbox', mensaje])
    print(mensaje)

def macInmacsPuertos(mac, macsPuertos):
    elementos = list(filter(lambda x: mac in x, macsPuertos))
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

def lanzar_contenedor(mac, macsPuertos, token, directorio):
    if not token:
        raise Exception('No se puede iniciar el contenedor sin un token')
    comando = 'docker run --rm -d -p %s:7681 -e TOKEN=%s -v "%s:/code" cplus2ttyd'
    macPuerto = macInmacsPuertos(mac, macsPuertos)
    if macPuerto:
        return macPuerto
    puerto = get_puerto_libre()
    print('Lanzando contenedor en puerto %s' % puerto)
    os.system(comando % (puerto, token, directorio))
    return MacPuerto(mac, puerto)

def gen_token(longitud=10):
    res = ''
    for i in range(longitud):
        res += random.choice(SIMBOLOS)
    return res

def get_token(mac, dictTokens):
    if mac in dictTokens.keys():
        return dictTokens[mac]
    while True:
        token = gen_token()
        if not token in dictTokens.values():
            return token
    assert False # imposible

class Monitor():
    def __init__(self, pathMacs, pathDirs, port=9048):        
        self.port = port
        self.pathDirs = pathDirs
        self.lock = threading.Lock()
        self.macsPuertos = set()
        self.dictTokens = {}
        self.pathMacs = pathMacs
        
    def run(self):
        """
        crear socket de servicio
        """
        mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        mySocket.bind(('', int(self.port)))  # binds to any available interface
        print('listenning on port: %s' % self.port)
        mySocket.listen(5)
        try:
            while True:
                conn, _ = mySocket.accept()
                attendThread = WorkThread(conn, self.lock, self.macsPuertos, self.dictTokens, self.pathMacs, self.pathDirs) # se crea un hilo de atención por cliente
                attendThread.start()
        except:
            pass
        finally:
            mySocket.close()

            
class WorkThread(threading.Thread):  # it is actually a subprocess
    def __init__(self, conn, lock, macsPuertos, dictTokens, pathMacs, pathDirs):
        self.conn = conn
        self.lock = lock
        self.macsPuertos = macsPuertos
        self.dictTokens = dictTokens
        self.pathMacs = pathMacs
        self.pathDirs = pathDirs
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
            users = accessPointInfo.getUsers(pathMacs)
            mac = getMacIp(data.decode('utf-8'))
            if not mac:
                raise Exception('La mac no existe para la ip dada')
            nombre = accessPointInfo.getNameMac(mac, users)
            if not nombre:
                raise AlumnoInexistente('El estudiante %s no está registrado en la lista de MACS' % mac)
            directorio = '%s/%s' % (self.pathDirs, nombre)
            macPuerto = self.eventos['lanzar'](mac, self.macsPuertos, self.dictTokens.get(mac, None), directorio)
            self.macsPuertos.add(macPuerto)
        except Exception as e:
            print(e)
            raise
        finally:
            self.lock.release()
        self.conn.send(str(macPuerto.puerto).encode('utf-8'))

        
    def darToken(self, data):
        data = data[9:]
        self.lock.acquire()
        token = self.eventos['darToken'](data.decode('utf-8'), self.dictTokens)
        # obtener mac de ip
        ip = data.decode('utf-8')
        mac = getMacIp(ip)
        self.dictTokens[mac] = token
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
                try:
                    self.lanzar(data)
                except AlumnoInexistente:
                    self.conn.send(b'No encontrado')
                except:
                    self.conn.send(b'Error')
            if data.startswith(b'darToken:'):
                self.darToken(data)
        except:
            pass
        finally:
            self.conn.close()

if __name__ == '__main__':
    pathMacs = sys.argv[1]
    pathDirs = sys.argv[2]
    dem = Monitor(pathMacs, pathDirs)
    dem.run()
