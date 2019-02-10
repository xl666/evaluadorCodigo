
import socket
import sys

HOST = 'localhost' #mientras no se hace migración a microservicios

def inyect(programa, entrada, maxTime=2, port=9030):
        message = '%s&&%s&&%s' % (programa, entrada, maxTime)
        retorno = inyectarAServicio(message, port)
        return eval(retorno)

def inyectarAServicio(message, port=9030):
        mySocket = socket.socket()
        mySocket.connect((HOST,port))
        mySocket.sendall(message.encode())
        mySocket.sendall('$$$'.encode())
        data = ''
        while not data.endswith('$$$'): # read message
            chunck = mySocket.recv(1024).decode()
            data += chunck
            if not chunck: #finisheds
                break
        if not data:
                raise RuntimeError("No se recibió respuesta")
        mySocket.close()
        return data[:-3] # quitar $$$

if __name__ == '__main__':
    print(inyect(sys.argv[1], sys.argv[2]))
