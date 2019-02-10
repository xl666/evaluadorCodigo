# -*- coding: utf-8 -*-
import json
import time

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import redirect, render

from evaluador_codigo.decorators import login_teacher_required
from evaluador_codigo.routines import *


@login_required(login_url="/login")
@login_teacher_required
def agregar_tema(request):
    if request.is_ajax():
        tema_post = request.POST.get('tema')
        tema = Tema.objects.create(tema=tema_post)
        return HttpResponse(
            json.dumps({"result": "El tema fue almacenado correctamente", "tema_id": tema.id, "tema": tema.tema}),
            content_type="application/json")
    else:
        return HttpResponse(json.dumps({"result": "Ocurrió un error al almacenar el tema"}),
                            content_type="application/json")


@login_required(login_url="/login")
@login_teacher_required
def agregar_curso(request):
    academico = get_object_or_404(Academico, user=request.user)
    context = obtener_informacion_academico(academico)
    form = CursoForm(academico)
    context["form"] = form
    template = "academico/cursos/agregar.html"
    if request.method == 'GET':
        return render(request, template, context)
    elif request.method == 'POST':
        form = CursoForm(academico, request.POST)
        print(request.POST.get("licenciatura"))
        print(request.POST.get("periodo"))
        if form.is_valid():
            curso = form.save()
            if curso:
                curso.academico = academico
                curso.save()
                return redirect(curso.get_absolute_url())
            else:
                context["error"] = "Error al almacenar el curso, verifique la información"
        context["form"] = form
        return render(request, template, context)


@login_required(login_url="/login")
@login_teacher_required
def agregar_ejercicio(request):
    academico = get_object_or_404(Academico, user=request.user)
    context = obtener_informacion_academico(academico)
    form = EjercicioForm()
    context["form"] = form
    template = "academico/ejercicios/agregar.html"
    if request.method == 'GET':
        return render(request, template, context)
    if request.method == 'POST':
        form = EjercicioForm(request.POST or None, request.FILES or None)
        entradas = request.POST.getlist("entradas[]")
        salidas = request.POST.getlist("salidas[]")
        temas = request.POST.get("temas")
        print(temas)
        print(request.POST.get("experiencias_educativas"))
        if form.is_valid():
            if not entradas or not salidas:
                context["error"] = "Debe agregar al menos un caso de prueba con sus entradas y salidas esperadas."
            else:
                ejercicio = form.save()
                ejercicio.academico = academico
                ejercicio.save()
                file = open('casosprueba.txt', 'w+', encoding='utf-8', errors='replace')
                ejercicio.casos_prueba.save('new', crear_casos_prueba(f=file, entradas=entradas, salidas=salidas))
                file.close()
                return redirect(ejercicio.get_absolute_url())
        else:
            context["form"] = form
        return render(request, template, context)


@login_required(login_url="/login")
@login_teacher_required
def agregar_examen(request, pk_curso):
    form = ExamenForm()
    academico = get_object_or_404(Academico, user=request.user)
    context = obtener_informacion_academico(academico)
    curso = get_object_or_404(Curso, pk=pk_curso, academico=academico)
    context["form"] = form
    context["curso_activo"] = curso
    context["ejercicios"] = Ejercicio.objects.filter(Q(academico=academico) | Q(publico=True))
    template = "academico/examenes/agregar.html"
    if request.method == 'GET':
        return render(request, template, context)
    if request.method == 'POST':
        form = ExamenForm(request.POST)
        ejercicios = request.POST.getlist("ejercicios[]")
        puntajes = request.POST.getlist("puntajes[]")
        if form.is_valid():
            if ejercicios and puntajes:
                examen = form.save(commit=False)
                if examen:
                    examen.curso = curso
                    examen.save()
                    for id_ejercicio, puntaje in zip(ejercicios, puntajes):
                        ejercicio = get_object_or_404(Ejercicio, id=id_ejercicio)
                        examen_ejercicio = EjerciciosExamenes.objects.create(examen=examen, ejercicio=ejercicio,
                                                                             puntaje=int(puntaje))
                    return redirect(context["curso_activo"].get_listado_examenes_url())
                else:
                    context["error"] = "Error al almacenar el examen, verifique la información"
            else:
                context["error"] = "Es necesario agregar al menos un ejercicio al examen"
        else:
            context["form"] = form
        return render(request, template, context)


@login_required(login_url="/login")
@login_teacher_required
def agregar_practica(request, pk_curso):
    form = PracticaForm()
    academico = get_object_or_404(Academico, user=request.user)
    context = obtener_informacion_academico(academico)
    curso = get_object_or_404(Curso, pk=pk_curso, academico=academico)
    context["form"] = form
    context["curso_activo"] = curso
    context["ejercicios"] = Ejercicio.objects.filter(Q(academico=academico) | Q(publico=True))
    template = "academico/practicas/agregar.html"
    if request.method == 'GET':
        return render(request, template, context)
    if request.method == 'POST':
        form = PracticaForm(request.POST)
        ejercicios = request.POST.getlist("ejercicios[]")
        puntajes = request.POST.getlist("puntajes[]")
        if form.is_valid():
            if ejercicios and puntajes:
                practica = form.save(commit=False)
                if practica:
                    practica.curso = curso
                    practica.save()
                    for id_ejercicio, puntaje in zip(ejercicios, puntajes):
                        ejercicio = get_object_or_404(Ejercicio, id=id_ejercicio)
                        practica_ejercicio = EjerciciosPracticas.objects.create(practica=practica, ejercicio=ejercicio,
                                                                                puntaje=int(puntaje))
                    return redirect(context["curso_activo"].get_listado_practicas_url())
                else:
                    context["error"] = "Error al almacenar la práctica, verifique la información"
            else:
                context["error"] = "Es necesario agregar al menos un ejercicio a la práctica"
        else:
            context["form"] = form
        return render(request, template, context)


@login_required(login_url="/login")
@login_teacher_required
def editar_curso(request, pk_curso):
    academico = get_object_or_404(Academico, user=request.user)
    context = obtener_informacion_academico(academico)
    curso = get_object_or_404(Curso, pk=pk_curso, academico=academico)
    form = CursoForm(academico, instance=curso)
    context["form"] = form
    template = "academico/cursos/editar.html"
    if request.method == 'GET':
        return render(request, template, context)
    elif request.method == 'POST':
        form = CursoForm(academico, request.POST, instance=curso)
        if form.is_valid():
            curso = form.save()
            if curso:
                curso.academico = academico
                curso.save()
                return redirect('listado_cursos')
            else:
                context["error"] = "Error al almacenar el curso, verifique la información"
        return render(request, template, context)


@login_required(login_url="/login")
@login_teacher_required
def ver_detalle_ejercicio(request, id_ejercicio):
    academico = get_object_or_404(Academico, user=request.user)
    context = obtener_informacion_academico(academico)
    ejercicio = get_object_or_404(Ejercicio, id=id_ejercicio)
    context["ejercicio"] = ejercicio
    template = "academico/ejercicios/detalle.html"
    return render(request, template, context)


@login_required(login_url="/login")
@login_teacher_required
def editar_ejercicio(request, id_ejercicio):
    academico = get_object_or_404(Academico, user=request.user)
    context = obtener_informacion_academico(academico)
    ejercicio = get_object_or_404(Ejercicio, id=id_ejercicio, academico=academico)
    form = EjercicioForm(instance=ejercicio)
    entradas, salidas = abrir_casos_prueba(ejercicio.casos_prueba.path)
    context["ejercicio"] = ejercicio
    context["form"] = form
    context["casos_prueba"] = zip(entradas, salidas)
    template = "academico/ejercicios/editar.html"
    if request.method == 'GET':
        return render(request, template, context)
    if request.method == 'POST':
        form = EjercicioForm(request.POST, request.FILES, instance=ejercicio)
        entradas = request.POST.getlist("entradas[]")
        salidas = request.POST.getlist("salidas[]")
        if form.is_valid():
            if not entradas or not salidas:
                context["error"] = "Debe agregar al menos un caso de prueba con sus entradas y salidas esperadas."
            else:
                ejercicio_actualizado = form.save()
                file = open('casosprueba.txt', 'w+', encoding='utf-8', errors='replace')
                ejercicio_actualizado.casos_prueba.save('new',
                                                        crear_casos_prueba(f=file, entradas=entradas, salidas=salidas))
                file.close()
                return redirect(ejercicio_actualizado.get_absolute_url())
        else:
            context["form"] = form
        return render(request, template, context)


@login_required(login_url="/login")
@login_teacher_required
def editar_practica(request, pk_curso, pk_practica):
    academico = get_object_or_404(Academico, user=request.user)
    context = obtener_informacion_academico(academico)
    curso = get_object_or_404(Curso, pk=pk_curso, academico=academico)
    practica = get_object_or_404(Practica, pk=pk_practica, curso=curso)
    form = PracticaForm(initial={'nombre':      practica.nombre,
                                 'inicio':      practica.inicio.strftime("%Y-%m-%d %H:%M:%S"),
                                 'termino':     practica.termino.strftime("%Y-%m-%d %H:%M:%S"),
                                 'descripcion': practica.descripcion})
    context["form"] = form
    context["curso_activo"] = curso
    context["practica"] = practica
    context["ejercicios_practica"] = EjerciciosPracticas.objects.filter(practica=practica)
    context["ejercicios"] = Ejercicio.objects.filter(Q(academico=academico) | Q(publico=True))
    template = "academico/practicas/editar.html"
    if request.method == 'GET':
        return render(request, template, context)
    if request.method == 'POST':
        form = PracticaForm(request.POST, instance=practica)
        ejercicios = request.POST.getlist("ejercicios[]")
        puntajes = request.POST.getlist("puntajes[]")
        ejercicios_enviados = []
        if form.is_valid():
            if ejercicios and puntajes:
                practica_actualizada = form.save()
                for id_ejercicio, puntaje in zip(ejercicios, puntajes):
                    ejercicio = Ejercicio.objects.get(id=id_ejercicio)
                    ejercicios_enviados.append(ejercicio)
                    if ejercicio not in practica.ejercicios.all():
                        practica_ejercicio = EjerciciosPracticas.objects.create(practica=practica_actualizada,
                                                                                ejercicio=ejercicio,
                                                                                puntaje=int(puntaje))
                for ejercicio in practica_actualizada.ejercicios.all():
                    if ejercicio not in ejercicios_enviados:
                        ejercicio_practica = EjerciciosPracticas.objects.get(ejercicio=ejercicio,
                                                                             practica=practica_actualizada)
                        ejercicio_practica.delete()
                return redirect(context["curso_activo"].get_listado_practicas_url())
            else:
                context["error"] = "Es necesario agregar al menos un ejercicio a la práctica"
        else:
            context["form"] = form
        return render(request, template, context)


@login_required(login_url="/login")
@login_teacher_required
def editar_examen(request, pk_curso, pk_examen):
    academico = get_object_or_404(Academico, user=request.user)
    context = obtener_informacion_academico(academico)
    curso = get_object_or_404(Curso, pk=pk_curso, academico=academico)
    examen = Examen.objects.get(pk=pk_examen, curso=curso)
    form = ExamenForm(instance=examen)
    context["form"] = form
    context["curso_activo"] = curso
    context["ejercicios_examen"] = EjerciciosExamenes.objects.filter(examen=examen)
    context["ejercicios"] = Ejercicio.objects.filter(Q(academico=academico) | Q(publico=True))
    template = "academico/examenes/editar.html"
    if request.method == 'GET':
        return render(request, template, context)
    if request.method == 'POST':
        form = ExamenForm(request.POST, instance=examen)
        id_ejercicios = request.POST.getlist("ejercicios[]")
        puntajes = request.POST.getlist("puntajes[]")
        ejercicios_enviados = []
        if form.is_valid():
            if id_ejercicios and puntajes:
                examen = form.save()
                for id_ejercicio, puntaje in zip(id_ejercicios, puntajes):
                    ejercicio = Ejercicio.objects.get(id=id_ejercicio)
                    ejercicios_enviados.append(ejercicio)
                    if ejercicio not in examen.ejercicios.all():
                        examen_ejercicio = EjerciciosExamenes.objects.create(examen=examen, ejercicio=ejercicio,
                                                                             puntaje=int(puntaje))
                for ejercicio in examen.ejercicios.all():
                    if ejercicio not in ejercicios_enviados:
                        ejercicio_examen = EjerciciosExamenes.objects.get(ejercicio=ejercicio, examen=examen)
                        ejercicio_examen.delete()
                return redirect(context["curso_activo"].get_listado_examenes_url())

            else:
                context["error"] = "Es necesario agregar al menos un ejercicio al examen"
        else:
            context["form"] = form
        return render(request, template, context)


@login_required(login_url="/login")
@login_teacher_required
def activar_examen(request, pk_curso, pk_examen):
    academico = get_object_or_404(Academico, user=request.user)
    curso = get_object_or_404(Curso, pk=pk_curso, academico=academico)
    examen = get_object_or_404(Examen, pk=pk_examen, curso=curso)
    examen.estado = "activo"
    examen.fecha_inicio = time.strftime("%Y-%m-%d %H:%M:%S")
    examen.save()
    return redirect(examen.get_administrar_url())


@login_required(login_url="/login")
@login_teacher_required
def administrar_examen(request, pk_curso, pk_examen):
    academico = get_object_or_404(Academico, user=request.user)
    context = obtener_informacion_academico(academico)
    curso = get_object_or_404(Curso, pk=pk_curso, academico=academico)
    examen = get_object_or_404(Examen, pk=pk_examen, curso=curso)
    alumnos = curso.alumnos.all()
    ejercicios = EjerciciosExamenes.objects.filter(examen=examen)
    respuestas_todas = obtener_puntajes_examen(alumnos, ejercicios)
    context["curso_activo"] = curso
    context["alumnos"] = alumnos
    context["examen"] = examen
    context["ejercicios"] = ejercicios
    context["respuestas"] = zip(respuestas_todas, alumnos)
    template = "academico/examenes/administrar.html"
    return render(request, template, context)


@login_required(login_url="/login")
@login_teacher_required
def concluir_examen(request, pk_curso, pk_examen):
    academico = get_object_or_404(Academico, user=request.user)
    curso = get_object_or_404(Curso, pk=pk_curso, academico=academico)
    examen = get_object_or_404(Examen, pk=pk_examen, curso=curso)
    examen.estado = "concluido"
    examen.fecha_termino = time.strftime("%Y-%m-%d %H:%M:%S")
    examen.save()
    return redirect(curso.get_listado_examenes_url())


@login_required(login_url="/login")
@login_teacher_required
def ver_puntajes_generales(request, pk_curso):
    academico = get_object_or_404(Academico, user=request.user)
    context = obtener_informacion_academico(academico)
    curso = get_object_or_404(Curso, pk=pk_curso, academico=academico)
    practicas = Practica.objects.filter(curso=curso).order_by('inicio')
    examenes = Examen.objects.filter(curso=curso).order_by('fecha_inicio')
    alumnos = curso.alumnos.all()
    puntajes_practicas = obtener_puntajes_practicas(alumnos, practicas)
    puntajes_examenes = obtener_puntajes_examenes(alumnos, examenes)
    context["curso_activo"] = curso
    context["alumnos"] = alumnos
    context["examenes"] = examenes
    context["practicas"] = practicas
    context["puntajes"] = zip(puntajes_practicas, puntajes_examenes, alumnos)
    template = "academico/cursos/listado_puntajes_generales.html"
    return render(request, template, context)


@login_required(login_url="/login")
@login_teacher_required
def ver_puntajes_practica(request, pk_curso, pk_practica):
    academico = get_object_or_404(Academico, user=request.user)
    context = obtener_informacion_academico(academico)
    curso = get_object_or_404(Curso, pk=pk_curso, academico=academico)
    practica = get_object_or_404(Practica, pk=pk_practica)
    alumnos = curso.alumnos.all()
    ejercicios = EjerciciosPracticas.objects.filter(practica=practica)
    respuestas_todas = obtener_puntajes_practica(alumnos, ejercicios)
    context["curso_activo"] = curso
    context["alumnos"] = alumnos
    context["practica"] = practica
    context["ejercicios"] = ejercicios
    context["respuestas"] = zip(respuestas_todas, alumnos)
    template = "academico/practicas/listado_puntajes.html"
    return render(request, template, context)


@login_required(login_url="/login")
def ver_puntajes_examen(request, pk_curso, pk_examen):
    academico = get_object_or_404(Academico, user=request.user)
    context = obtener_informacion_academico(academico)
    curso = get_object_or_404(Curso, pk=pk_curso, academico=academico)
    examen = get_object_or_404(Examen, pk=pk_examen, curso=curso)
    alumnos = curso.alumnos.all()
    ejercicios = EjerciciosExamenes.objects.filter(examen=examen)
    respuestas_todas = obtener_puntajes_examen(alumnos, ejercicios)
    context["curso_activo"] = curso
    context["alumnos"] = alumnos
    context["examen"] = examen
    context["ejercicios"] = ejercicios
    context["respuestas"] = zip(respuestas_todas, alumnos)
    template = "academico/examenes/listado_puntajes.html"
    return render(request, template, context)


@login_required(login_url="/login")
@login_teacher_required
def ver_respuesta_ejercicio_practica(request, pk_curso, pk_practica, pk_respuesta):
    academico = get_object_or_404(Academico, user=request.user)
    context = obtener_informacion_academico(academico)
    curso = get_object_or_404(Curso, pk=pk_curso, academico=academico)
    practica = get_object_or_404(Practica, pk=pk_practica)
    respuesta = get_object_or_404(RespuestasPracticas, pk=pk_respuesta)
    context["curso_activo"] = curso
    context["practica"] = practica
    context["respuesta"] = respuesta
    archivo = open(respuesta.archivo_respuesta.path, "r", encoding='cp1252', errors='replace')
    context["codigo"] = archivo.read()
    archivo.close()
    template = "academico/detalle_respuesta_estudiante.html"
    return render(request, template, context)


@login_required(login_url="/login")
@login_teacher_required
def ver_respuesta_ejercicio_examen(request, pk_curso, pk_examen, pk_respuesta):
    academico = get_object_or_404(Academico, user=request.user)
    context = obtener_informacion_academico(academico)
    curso = get_object_or_404(Curso, pk=pk_curso, academico=academico)
    examen = get_object_or_404(Examen, pk=pk_examen)
    respuesta = get_object_or_404(RespuestasExamenes, pk=pk_respuesta)
    context["curso_activo"] = curso
    context["examen"] = examen
    context["respuesta"] = respuesta
    archivo = open(respuesta.archivo_respuesta.path, "r", encoding='cp1252', errors='replace')
    context["codigo"] = archivo.read()
    archivo.close()
    template = "academico/detalle_respuesta_estudiante.html"
    return render(request, template, context)


@login_required(login_url="/login")
@login_teacher_required
def editar_perfil(request):
    academico = get_object_or_404(Academico, user=request.user)
    context = obtener_informacion_academico(academico)
    form_user = UserForm(instance=request.user)
    form_academico = AcademicoForm(instance=academico)
    context["form_academico"] = form_academico
    context["form_user"] = form_user
    template = "academico/editar_perfil.html"
    if request.method == 'GET':
        return render(request, template, context)
    if request.method == 'POST':
        form_user = UserForm(request.POST or None, request.FILES or None, instance=request.user)
        form_academico = AcademicoForm(request.POST, instance=academico)
        password_actual = request.POST.get("password_actual")
        password_nueva = request.POST.get("password_nueva")
        password_conf = request.POST.get("password_conf")
        if form_user.is_valid() and form_academico.is_valid():
            user = form_user.save()
            academico = form_academico.save()
            if user.check_password(password_actual):
                if password_nueva and password_conf and password_nueva == password_conf:
                    user.set_password(password_nueva)
                    user.save()
            return redirect('inicio')
        else:
            context["form_academico"] = form_academico
            context["form_user"] = form_user
        return render(request, template, context)


@login_required(login_url="/login")
@login_teacher_required
def eliminar_practica(request, pk_curso, pk_practica):
    academico = get_object_or_404(Academico, user=request.user)
    curso = get_object_or_404(Curso, pk=pk_curso, academico=academico)
    practica = get_object_or_404(Practica, pk=pk_practica)
    practica.delete()
    return redirect(curso.get_listado_practicas_url())


@login_required(login_url="/login")
@login_teacher_required
def eliminar_examen(request, pk_curso, pk_examen):
    academico = get_object_or_404(Academico, user=request.user)
    curso = get_object_or_404(Curso, pk=pk_curso, academico=academico)
    examen = get_object_or_404(Examen, pk=pk_examen)
    examen.delete()
    return redirect(curso.get_listado_examenes_url())


@login_required(login_url="/login")
@login_teacher_required
def ver_listado_ejercicios(request):
    academico = get_object_or_404(Academico, user=request.user)
    context = obtener_informacion_academico(academico)
    context["ejercicios"] = Ejercicio.objects.filter(Q(academico=academico) | Q(publico=True))
    template = "academico/ejercicios/listado.html"
    return render(request, template, context)


@login_required(login_url="/login")
@login_teacher_required
def ver_listado_cursos(request):
    academico = get_object_or_404(Academico, user=request.user)
    context = obtener_informacion_academico(academico)
    template = "academico/cursos/listado.html"
    return render(request, template, context)
