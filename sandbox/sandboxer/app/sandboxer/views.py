from django.shortcuts import render_to_response
from sandboxer import settings
import os
import threading
import socket


DELIMITADOR = b'$$$'

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def index(request):
    ip = get_client_ip(request)
    cliente = socket.socket()
    try:
        cliente.connect(('localhost', int(settings.PUERTO_MONITOR)))
        cliente.send(b'lanzar:%s%s' % (ip.encode('utf-8'), DELIMITADOR))
        puerto = int(cliente.recv(1024))
        print(puerto)
        return render_to_response('index.html', {'urlEvaluador': settings.EVALUADOR_URL, 'puerto': puerto})
    except Exception as err:
        print('CAEEEEEEEEEEEEEEEEEEEEEe')
        print(err)
    finally:
        cliente.close()
    
    
