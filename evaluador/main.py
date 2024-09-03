import socket
import os
import buffer
import multiprocessing
import stat
import shutil
from evaluar import evaluar

SERVER_HOST = 'server'
SERVER_PORT = 1234

directory = 'uploads'

try:
    os.mkdir(directory)
except FileExistsError:
    pass


os.chmod(directory, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)

class Monitor:
    def __init__(self, port=SERVER_PORT, host = SERVER_HOST):
        self.port = port
        self.host = host

    def run(self):
        mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        mySocket.bind((self.host, self.port))
        print('Recibiendo peticiones en puerto:', self.port)
        mySocket.listen(5)
        while True:
            conn, addr = mySocket.accept()
            attendThread = WorkThread(conn, addr)
            attendThread.start()

class WorkThread(multiprocessing.Process):
    def __init__(self, conn, addr):
        super().__init__()
        self.conn = conn
        self.addr = addr
        multiprocessing.Process.__init__(self)

    def run(self):
        connbuf = buffer.Buffer(self.conn)

        files_processed = 0

        programa_name = ""
        casos_name = ""

        while True and files_processed < 2:
            hash_type = connbuf.get_utf8()
            file_name = connbuf.get_utf8()

            if files_processed == 0:
                programa_name = file_name
            elif files_processed == 1:
                casos_name = file_name

            if not file_name:
                break  # Salir si no hay nombre de archivo
            
            file_name = os.path.join('uploads', file_name)
            file_size = int(connbuf.get_utf8())

            with open(file_name, 'wb') as f:
                remaining = file_size
                while remaining:
                    chunk_size = 4096 if remaining >= 4096 else remaining
                    chunk = connbuf.get_bytes(chunk_size)
                    if not chunk:
                        break
                    f.write(chunk)
                    remaining -= len(chunk)
                files_processed += 1

        print("Enviando respuesta")
        res = evaluar(f'uploads/{programa_name}', f'uploads/{casos_name}')
        [shutil.rmtree(os.path.join('uploads', f)) if os.path.isdir(os.path.join('uploads', f)) else os.remove(os.path.join('uploads', f)) for f in os.listdir('uploads')]
        self.conn.sendall(res.encode() + b'\x00') 
        self.conn.close()
        print(f'{res.encode()}')

if __name__ == '__main__':
    dem = Monitor()
    dem.run()
