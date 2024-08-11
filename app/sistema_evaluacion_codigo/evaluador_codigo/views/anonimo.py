import re
from enum import Enum
from django import forms
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render
from captcha.fields import CaptchaField
from datetime import datetime, timezone

from evaluador_codigo.decorators import logout_required
from evaluador_codigo.models import Academico, Alumno, Licenciatura, User, Intentos
from evaluador_codigo.forms import RegisterForm

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def recuperar_info_ip(ip:str) -> Intentos:
    try:
        register = Intentos.objects.get(ip=ip)
        return register
    except:
        return None

def fecha_en_intervalo(fecha_ultimo_intento:datetime, ahora:datetime, tiempo_limite:int) -> bool:
    diferencia_segundos = (ahora - fecha_ultimo_intento).seconds
    if diferencia_segundos < tiempo_limite:
        return True
    return False

def puede_intentar_loguearse(request, tiempo_limite=300, intentos_maximos=3) -> bool:
    ip = get_client_ip(request)
    ahora = datetime.now(timezone.utc)
    registro = recuperar_info_ip(ip)
    if not registro:
        nuevo_registro = Intentos()
        nuevo_registro.ip = ip
        modificar_registro(nuevo_registro, ahora)
        return True
    else:
        intentos = registro.intentos
        fecha_ultimo_intento = registro.fecha_ultimo_intento
        if not fecha_en_intervalo(fecha_ultimo_intento, ahora, tiempo_limite):
            modificar_registro(registro, ahora)
         
            return True
        else:
            if intentos < intentos_maximos:
                modificar_registro(registro, ahora, intentos+1)
                return True
            else:
                modificar_registro(registro, ahora, intentos_maximos)
                return False
        
def modificar_registro(registro:Intentos, ahora: datetime, intentos=1) -> None:
    registro.intentos = intentos
    registro.fecha_ultimo_intento = ahora
    registro.save()

@logout_required
def iniciar_sesion(request):
    context = {}
    template = "anonimo/login.html"
    if request.method == 'GET':
        return render(request, template, context)
    elif request.method == 'POST':
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        if not puede_intentar_loguearse(request):
            context["error"] = 'Ha excedido el límite de intentos, intente más tarde'
            return render(request, template, context)
        aut = authenticate(username=username, password=password)
        if aut is not None:
            usuario = User.objects.get(username=username)
            if not usuario.is_active:
                context["error"] = 'Su cuenta no está activa, porfavor contacte al administrador'
            else:
                login(request, aut)
                return redirect('inicio')
        else:
            context["error"] = 'Verifique usuario y contraseña'
        return render(request, template, context)


@logout_required
def registrar_alumno(request):
    template = "anonimo/registro_alumno.html"
    context = {"licenciaturas": Licenciatura.objects.all()}
    
    if request.method == 'GET':
        form = RegisterForm()
        context['form'] = form
        return render(request, template, context)
    
    elif request.method == 'POST':
        form = RegisterForm(request.POST) 
        context['form'] = form
        
        if form.is_valid():
            username = form.cleaned_data['username']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            matricula = form.cleaned_data['matricula']
            licenciatura = form.cleaned_data['licenciatura']

            user_exist = user_exist_database(username, email, matricula, True)

            if(user_exist == User_exist_response.NOT_EXIST):
                try:
                    user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                                    password=password, email=email, is_student=True, is_active=True)

                    Alumno.objects.create(user=user, matricula=matricula, licenciatura=licenciatura)
                    return redirect('inicio')
                except:
                    context["error"] = F"El usuario ya existe en el sistema"
            elif user_exist == User_exist_response.USERNAME_EXIST:
                context["error"] = F"El username ya se encuentra registrado"
            elif user_exist == User_exist_response.EMAIL_EXIST:
                context["error"] = F"El email ya se encuentra registrado"
            elif user_exist == User_exist_response.MATRICULA_EXIST:
                context["error"] = F"La matricula ya se encuentra registrado"
        return render(request, template, context)

class User_exist_response(Enum):
    NOT_EXIST = 0
    USERNAME_EXIST = 1
    EMAIL_EXIST = 2
    MATRICULA_EXIST = 3

def user_exist_database(username: str, email: str, matricula, is_student):

    if User.objects.filter(username=username).exists():
        return User_exist_response.USERNAME_EXIST

    if User.objects.filter(email=email).exists():
        return User_exist_response.EMAIL_EXIST

    if is_student and matricula:
        if Alumno.objects.filter(matricula=matricula).exists():
            return User_exist_response.MATRICULA_EXIST

    return User_exist_response.NOT_EXIST

def agregar_texto(texto):
    try:
        with open('logs.txt', 'a') as archivo:
            archivo.write('\n' + texto)
    except FileNotFoundError:
        with open('logs.txt', 'w') as archivo:
            archivo.write(texto)

@logout_required
def registrar_academico(request):
    template = "anonimo/registro_academico.html"
    context = {"licenciaturas": Licenciatura.objects.all()}
    if request.method == 'GET':
        return render(request, template, context)
    elif request.method == 'POST':
        username = request.POST.get('username', None)
        email = request.POST.get('email', None)
        first_name = request.POST.get('name', None)
        last_name = request.POST.get('last_name', None)
        id_licenciaturas = request.POST.getlist("licenciaturas")
        password = request.POST.get('password', None)
        conf_password = request.POST.get('conf_password', None)
        if not username.strip(' ') or not first_name.strip(' ') or not last_name.strip(' ') or not id_licenciaturas \
            or not email.strip(' ') or not password.strip(' ') or not conf_password.strip(' '):
            context["error"] = "Falta uno o más campos"
        elif password != conf_password:
            context["error"] = "La contraseña no coincide con su confirmación"
        else:
            try:
                user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                                password=password, email=email, is_teacher=True, is_active=False)
                academico = Academico(user=user)
                academico.save()
                for id_licenciatura in id_licenciaturas:
                    lic = Licenciatura.objects.get(id=id_licenciatura)
                    academico.licenciaturas.add(lic)
                academico.save()
                context["exito"] = "Solicitud enviada exitosamente, el administrador le notificará cuando sea aceptada"
                return render(request, template, context)
            except:
                context["error"] = "El usuario ya existe en el sistema"
        return render(request, template, context)
