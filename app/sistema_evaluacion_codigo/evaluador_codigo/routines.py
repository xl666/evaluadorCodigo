# -*- coding: utf-8 -*-
from django.core.files import File
from django.shortcuts import get_object_or_404

from api.compilador import compile
from api.evaluador import evaluar
from api.unirFuentes import generarFuenteJava
from .forms import *
from .models import *


# Crea el archivo de casos de prueba para ligarlo a un ejercicio
def crear_casos_prueba(f, entradas, salidas):
    for entrada, salida in zip(entradas, salidas):
        f.write(str(entrada) + '\n')
        f.write(INPUT_BREAK + '\n')
        f.write(str(salida) + '\n')
        f.write(CASE_BREAK + '\n')
    djangofile = File(f)
    return djangofile


# Abre el archivo de casos de prueba para poder editar un ejercicio
def abrir_casos_prueba(casos_prueba):
    entradas = []
    salidas = []
    entrada = ''
    salida = ''
    ban = False
    for line in open(casos_prueba, encoding='utf-8'):
        messyLine = line
        line = line.strip()
        if (line == ''):
            continue
        if line == INPUT_BREAK:
            entradas.append(entrada)
            entrada = ''  # restart input
            ban = True
        elif line == CASE_BREAK:
            salidas.append(salida)
            salida = ''  # restart output
            ban = False
        elif ban:
            salida += messyLine
        else:  # input reconstruction
            for elem in line.split(','):
                entrada += elem + '\n'
    return entradas, salidas


def realizar_union_fuentes(respuesta):
    if (respuesta.archivo_respuesta_temporal.name.endswith('zip')):
        if generarFuenteJava(respuesta.archivo_respuesta_temporal.path, respuesta.get_path_archivo("Main.java")):
            with open(respuesta.get_path_archivo("Main.java"), 'r') as resultado:
                djangofile = File(resultado)
                respuesta.archivo_respuesta_temporal.save("Main.java", resultado)
                respuesta.save()
            return True
        else:
            return False


def realizar_evaluacion(respuesta):
    resultado_evaluacion = False
    if (respuesta.archivo_respuesta_temporal.name.endswith('py') or respuesta.archivo_respuesta_temporal.name.endswith(
        'prolog')):
        resultado_evaluacion = evaluar(respuesta.archivo_respuesta_temporal.path,
                                       respuesta.ejercicio.ejercicio.casos_prueba.path)
    else:
        resultado_compilacion, archivo_compilado = compile(respuesta.archivo_respuesta_temporal.path,
                                                           respuesta.get_path())
        if resultado_compilacion:
            resultado_evaluacion = evaluar(respuesta.get_path_archivo(archivo_compilado),
                                           respuesta.ejercicio.ejercicio.casos_prueba.path)
    return resultado_evaluacion


# Obtiene el puntaje obtenido por el alumno en su respuesta
def calcular_puntaje_obtenido_respuesta(resultado_evaluacion, puntaje_ejercicio):
    num_casos = len(resultado_evaluacion)
    casos_aprobados = 0
    for resultado in resultado_evaluacion:
        if resultado == True:
            casos_aprobados = casos_aprobados + 1
        elif resultado == 'Runtime error' or resultado == 'Time exceeded':
            return False, resultado
    return True, int(puntaje_ejercicio / num_casos * casos_aprobados)


# valida que una práctica esté activa
def validar_estado_practica(practica):
    estado = False
    if practica.get_estado() == "activa":
        estado = True
    return estado


# valida que un examen esté activo
def validar_estado_examen(examen):
    estado = False
    if examen.estado == "activo":
        estado = True
    return estado


def validar_respuesta_anterior(respuesta, respuesta_anterior, puntaje_obtenido, error=""):
    if respuesta_anterior:  # verifica si hay una respuesta anterior enviada por el alumno para el mismo ejercicio
        if respuesta_anterior.puntaje_obtenido < puntaje_obtenido:  # si el alumno mejora el puntaje obtenido,
            # se deshecha la respuesta anterior y se guarda la enviada
            respuesta.puntaje_obtenido = puntaje_obtenido
            respuesta.archivo_respuesta.save('new', respuesta.archivo_respuesta_temporal)
            respuesta.error = error
            respuesta.save()
    else:  # si no hay una respuesta anterior se guarda la respuesta enviada
        respuesta.archivo_respuesta.save('new', respuesta.archivo_respuesta_temporal)
        respuesta.puntaje_obtenido = puntaje_obtenido
        respuesta.error = error
        respuesta.save()


def obtener_practicas(curso):
    estado_practicas = []
    color_practicas = []
    practicas = Practica.objects.filter(curso=curso)
    for practica in practicas:
        estado = practica.get_estado()
        estado_practicas.append(estado)
        if estado == "por iniciar":
            color_practicas.append("label-warning")
        elif estado == "activa":
            color_practicas.append("label-success")
        elif estado == "cerrada":
            color_practicas.append("label-default")
    return zip(practicas, estado_practicas, color_practicas)


def obtener_examenes_como_academico(curso):
    estado_examenes = []
    color_examenes = []
    examenes = Examen.objects.filter(curso=curso)
    for examen in examenes:
        estado_examenes.append(examen.estado)
        if examen.estado == "por iniciar":
            color_examenes.append("label-warning")
        elif examen.estado == "activo":
            color_examenes.append("label-success")
        elif examen.estado == "concluido":
            color_examenes.append("label-default")
    return zip(examenes, estado_examenes, color_examenes)


def obtener_ejercicios_practica(practica, alumno):
    puntajes = []
    ejercicios_practica = EjerciciosPracticas.objects.filter(practica=practica)
    for ejercicio in ejercicios_practica:
        try:
            respuesta = RespuestasPracticas.objects.get(ejercicio=ejercicio, alumno=alumno)
            puntajes.append(respuesta.puntaje_obtenido)
        except:
            puntajes.append(0)
    return zip(ejercicios_practica, puntajes)


def obtener_ejercicios_examen(examen, alumno):
    puntajes = []
    ejercicios_examen = EjerciciosExamenes.objects.filter(examen=examen)
    for ejercicio in ejercicios_examen:
        try:
            respuesta = RespuestasExamenes.objects.get(ejercicio=ejercicio, alumno=alumno)
            puntajes.append(respuesta.puntaje_obtenido)
        except:
            puntajes.append(0)
    return zip(ejercicios_examen, puntajes)


def obtener_examenes_como_alumno(curso):
    estado_examenes = []
    color_examenes = []
    examenes = Examen.objects.filter(curso=curso).exclude(estado="por iniciar").exclude(estado="concluido")
    for examen in examenes:
        estado_examenes.append(examen.estado)
        if examen.estado == "activo":
            color_examenes.append("label-success")
    return zip(examenes, estado_examenes, color_examenes)


# obtiene los puntajes de todos los alumnos, en todas las prácticas de un curso determinado
def obtener_puntajes_practicas(alumnos, practicas):
    puntajes_practicas = []
    puntajes_alumno = []
    for alumno in alumnos:
        for practica in practicas:
            puntaje = get_puntaje_obtenido_practica(practica, alumno)
            puntajes_alumno.append(puntaje)
        puntajes_practicas.append(puntajes_alumno)
        puntajes_alumno = []
    return puntajes_practicas


# obtiene los puntajes de todos los alumnos, en todos los exámenes de un curso determinado
def obtener_puntajes_examenes(alumnos, examenes):
    puntajes_examenes = []
    puntajes_alumno = []
    for alumno in alumnos:
        for examen in examenes:
            puntaje = get_puntaje_obtenido_examen(examen, alumno)
            puntajes_alumno.append(puntaje)
        puntajes_examenes.append(puntajes_alumno)
        puntajes_alumno = []
    return puntajes_examenes


# obtiene los puntajes obtenidos por todos los alumnos, en cada ejercicio de una práctica determinada
def obtener_puntajes_practica(alumnos, ejercicios):
    respuestas_alumno = []
    respuestas_todas = []
    for alumno in alumnos:
        for ejercicio in ejercicios:
            try:
                respuesta = RespuestasPracticas.objects.get(ejercicio=ejercicio, alumno=alumno)
            except:
                respuesta = "Sin entrega del estudiante"
            respuestas_alumno.append(respuesta)
        respuestas_todas.append(respuestas_alumno)
        respuestas_alumno = []
    return respuestas_todas


# obtiene los puntajes obtenidos por todos los alumnos, en cada ejercicio de un examen determinado
def obtener_puntajes_examen(alumnos, ejercicios):
    respuestas_alumno = []
    respuestas_todas = []
    for alumno in alumnos:
        for ejercicio in ejercicios:
            try:
                respuesta = RespuestasExamenes.objects.get(ejercicio=ejercicio, alumno=alumno)
            except:
                respuesta = "Sin entrega del estudiante"
            respuestas_alumno.append(respuesta)
        respuestas_todas.append(respuestas_alumno)
        respuestas_alumno = []
    return respuestas_todas


# obtiene el puntaje de un alumno, en una práctica determinada
def get_puntaje_obtenido_practica(practica, alumno):
    puntaje_obtenido = 0
    ejercicios = EjerciciosPracticas.objects.filter(practica=practica)
    for ejercicio in ejercicios:
        try:
            respuesta = RespuestasPracticas.objects.get(ejercicio=ejercicio, alumno=alumno)
            puntaje_obtenido = puntaje_obtenido + respuesta.puntaje_obtenido
        except:
            puntaje_obtenido = puntaje_obtenido + 0
    return puntaje_obtenido


# obtiene el puntaje de un alumno, en un examen determinado
def get_puntaje_obtenido_examen(examen, alumno):
    puntaje_obtenido = 0
    ejercicios = EjerciciosExamenes.objects.filter(examen=examen)
    for ejercicio in ejercicios:
        try:
            respuesta = RespuestasExamenes.objects.get(ejercicio=ejercicio, alumno=alumno)
            puntaje_obtenido = puntaje_obtenido + respuesta.puntaje_obtenido
        except:
            puntaje_obtenido = puntaje_obtenido + 0
    return puntaje_obtenido


def obtener_form_respuesta_examen(request, ejercicio, alumno):
    try:
        respuesta_anterior = RespuestasExamenes.objects.get(ejercicio=ejercicio, alumno=alumno)
        return RespuestasExamenesForm(request.POST or None, request.FILES or None, instance=respuesta_anterior)
    except:
        return RespuestasExamenesForm(request.POST or None, request.FILES or None)


def obtener_form_respuesta_practica(request, ejercicio, alumno):
    try:
        respuesta_anterior = RespuestasPracticas.objects.get(ejercicio=ejercicio, alumno=alumno)
        return RespuestasPracticasForm(request.POST or None, request.FILES or None, instance=respuesta_anterior)
    except:
        return RespuestasPracticasForm(request.POST or None, request.FILES or None)


def obtener_respuesta_anterior_examen(ejercicio, alumno):
    try:
        return RespuestasExamenes.objects.get(ejercicio=ejercicio, alumno=alumno)
    except:
        return False


def obtener_respuesta_anterior_practica(ejercicio, alumno):
    try:
        return RespuestasPracticas.objects.get(ejercicio=ejercicio, alumno=alumno)
    except:
        return False


def subir_respuesta_ejercicio(form, respuesta_anterior, ejercicio, context):
    if form.is_valid():
        respuesta = form.save(commit=False)
        if respuesta:
            respuesta.ejercicio = ejercicio
            respuesta.alumno = context["alumno"]
            respuesta.save()
            if (respuesta.archivo_respuesta_temporal.name.endswith('zip')):
                if not realizar_union_fuentes(respuesta):
                    context["error"] = "Error al unir fuentes"
                    return False, 0
            resultado_evaluacion = realizar_evaluacion(respuesta)
            if resultado_evaluacion:
                resultado, puntaje = calcular_puntaje_obtenido_respuesta(resultado_evaluacion, ejercicio.puntaje)
                if not resultado:
                    context["error"] = puntaje
                    validar_respuesta_anterior(respuesta, respuesta_anterior, 0, error=context["error"])
                    return False, 0
                validar_respuesta_anterior(respuesta, respuesta_anterior, puntaje)
                return True, puntaje
            else:
                context["error"] = "Error de compilación"
                validar_respuesta_anterior(respuesta, respuesta_anterior, 0, error=context["error"])
                return False, 0
    else:
        context["form"] = form
        return False, 0


def obtener_informacion_academico(academico):
    context = {}
    context["licenciaturas"] = academico.licenciaturas.all()
    context["cursos_activos"] = Curso.objects.filter(academico=academico).filter(activo=True)
    context["cursos_inactivos"] = Curso.objects.filter(academico=academico).filter(activo=False)
    context["cursos"] = Curso.objects.filter(academico=academico)
    context["academico"] = academico
    return context


def obtener_informacion_alumno(alumno):
    context = {}
    context["licenciaturas"] = alumno.licenciatura
    context["cursos_activos"] = alumno.cursos.filter(activo=True)
    context["cursos_inactivos"] = alumno.cursos.filter(activo=False)
    context["cursos"] = alumno.cursos.all()
    context["alumno"] = alumno
    return context


def obtener_curso_como_estudiante(pk_curso, alumno):
    curso = get_object_or_404(Curso, pk=pk_curso)  # obtiene el curso enviado en la url
    queryset = curso.alumnos.all()  # obtiene todos los alumnos que están inscritos a ese curso
    get_object_or_404(queryset, pk=alumno.pk)  # verifica que el alumno que hace la solicitud, esté inscrito en el curso
    return curso
