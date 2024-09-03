import time
import socket
from api.buffer import Buffer
import os

SERVER_HOST = 'server'
SERVER_PORT = 1234

def evaluar_service(path_programa, path_casos):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((SERVER_HOST, SERVER_PORT))

    try:
        sbuf = Buffer(s)

        hash_type = "abc"
        files = f'{path_programa} {path_casos}'
        files_to_send = files.split()

        for file_name in files_to_send:
            sbuf.put_utf8(hash_type)
            sbuf.put_utf8(file_name.split("/")[-1])

            file_size = os.path.getsize(file_name)
            sbuf.put_utf8(str(file_size))

            with open(file_name, 'rb') as f:
                sbuf.put_bytes(f.read())
        
        response_message = b""
        while b'\x00' not in response_message:
            chunk = s.recv(1024)
            if not chunk:
                break
            response_message += chunk

        return response_message.decode('utf-8').strip('\x00')
    finally:
        s.close()
