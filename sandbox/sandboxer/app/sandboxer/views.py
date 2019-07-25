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

def recuperarToken(request, ip):
    token = request.session.get('token', None)
    if not token:
        try:
            cliente = socket.socket()
            cliente.connect(('localhost', int(settings.PUERTO_MONITOR)))
            cliente.send(b'darToken:%s%s' % (ip.encode('utf-8'), DELIMITADOR))
            token = cliente.recv(1024)
            token = token.decode('utf-8')
            request.session['token'] = token
            cliente.close()
        except:
            raise
        finally:
            cliente.close()
    return token

def lanzarContenedor(request, token, ip):
    puerto = request.session.get('puerto', None)
    if not puerto:
        try:
            cliente = socket.socket()
            cliente.connect(('localhost', int(settings.PUERTO_MONITOR)))
            cliente.send(b'lanzar:%s%s' % (ip.encode('utf-8'), DELIMITADOR))
            puerto = int(cliente.recv(1024))
        except:
            raise
        finally:
            cliente.close()
    return puerto

def index(request):
    ip = get_client_ip(request)
    try:
        token = recuperarToken(request, ip)
        print(token)
        puerto = lanzarContenedor(request, token, ip)
        request.session['token'] = token
        request.session['puerto'] = puerto        
        
        return render_to_response('index.html', {'urlEvaluador': settings.EVALUADOR_URL, 'puerto': puerto})
    except Exception as err:
        print(err)
    
    
