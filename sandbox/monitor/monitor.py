
"""
"""

import socket
import multiprocessing
import subprocess
import datetime

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
        print('listenning on port: %s' % self.port)
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
        while not data.endswith('$$$'): # read message
            chunck = self.conn.recv(1024).decode()
            data += chunck
            if not chunck: #finished
                break
        if not data:
            raise RuntimeError("No se transmitieron datos")
        data = data[:-3] # quitar $$$
        mensaje = '%s: %s' % (datetime.datetime.now(), data)
        subprocess.call(['kdialog', '--msgbox', mensaje])
        print(mensaje)

if __name__ == '__main__':
    dem = Monitor()
    dem.run()

