# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from evaluador_codigo.decorators import login_student_required
from evaluador_codigo.routines import *


@login_required(login_url="/login")
@login_student_required
def inscribir_curso(request):
    alumno = get_object_or_404(Alumno, user=request.user)
    context = obtener_informacion_alumno(alumno)
    context["cursos_todos"] = Curso.objects.filter(licenciatura=alumno.licenciatura).exclude(id__in=context["cursos"])
    template = "alumno/cursos/inscribir.html"
    if request.method == 'GET':
        return render(request, template, context)
    elif request.method == 'POST':
        codigo_inscripcion = request.POST.get('codigo', None)
        id_curso = request.POST.get('curso', None)
        curso = get_object_or_404(Curso, id=id_curso)
        if codigo_inscripcion == curso.codigo_inscripcion:
            try:
                alumno.cursos.add(curso)
                alumno.save()
                return redirect(curso.get_absolute_url())
            except:
                context["error"] = "Error al registrar inscripción, verifique los campos"
        else:
            context["error"] = "El código de inscripción ingresado es incorrecto"
        return render(request, template, context)


@login_required(login_url="/login")
@login_student_required
def ver_detalle_practica(request, pk_curso, pk_practica):
    alumno = get_object_or_404(Alumno, user=request.user)
    context = obtener_informacion_alumno(alumno)
    curso = obtener_curso_como_estudiante(pk_curso, alumno)
    practica = get_object_or_404(Practica, pk=pk_practica, curso=curso)
    context["curso_activo"] = curso
    context["practica"] = practica
    context["ejercicios_practica"] = obtener_ejercicios_practica(practica, alumno)
    template = "alumno/practicas/detalle.html"
    return render(request, template, context)


@login_required(login_url="/login")
@login_student_required
def ver_detalle_examen(request, pk_curso, pk_examen):
    alumno = get_object_or_404(Alumno, user=request.user)
    context = obtener_informacion_alumno(alumno)
    curso = obtener_curso_como_estudiante(pk_curso, alumno)
    examen = get_object_or_404(Examen, pk=pk_examen, curso=curso)
    if examen.estado != "activo":
        return redirect('inicio')
    context["curso_activo"] = curso
    context["examen"] = examen
    context["ejercicios_examen"] = obtener_ejercicios_examen(examen, alumno)
    template = "alumno/examenes/detalle.html"
    return render(request, template, context)


@login_required(login_url="/login")
@login_student_required
def resolver_ejercicio_practica(request, pk_curso, pk_practica, pk_ejercicio):
    alumno = get_object_or_404(Alumno, user=request.user)
    context = obtener_informacion_alumno(alumno)
    curso = obtener_curso_como_estudiante(pk_curso, alumno)
    practica = get_object_or_404(Practica, pk=pk_practica, curso=curso)
    ejercicio = get_object_or_404(Ejercicio, pk=pk_ejercicio)
    ejercicio_practica = get_object_or_404(EjerciciosPracticas, practica=practica, ejercicio=ejercicio)
    respuesta_anterior = obtener_respuesta_anterior_practica(ejercicio_practica, alumno)
    form = RespuestasPracticasForm()
    context["ejercicio"] = ejercicio_practica
    context["curso_activo"] = curso
    if respuesta_anterior:
        context["respuesta_anterior"] = respuesta_anterior
        context["respuesta_nombre"] = str(ejercicio.id) + str(alumno.id)
    context["form"] = form
    template = "alumno/practicas/responder_ejercicio.html"
    if request.method == 'GET':
        return render(request, template, context)
    if request.method == 'POST':
        if not validar_estado_practica(practica):  # verifica que el examen esté activo
            context[
                "error"] = "La práctica ha concluido"  # si el examen no está activo, no se guarda la respuesta del
            # estudiante
        else:
            form = obtener_form_respuesta_practica(request, ejercicio_practica, alumno)
            bandera, puntaje = subir_respuesta_ejercicio(form, respuesta_anterior, ejercicio_practica, context)
            if bandera:
                #return redirect(practica.get_absolute_url())
                context['ultimo_puntaje'] = puntaje
                context['redirigir'] = practica.get_absolute_url()
        return render(request, template, context)


@login_required(login_url="/login")
@login_student_required
def resolver_ejercicio_examen(request, pk_curso, pk_examen, pk_ejercicio):
    alumno = get_object_or_404(Alumno, user=request.user)
    context = obtener_informacion_alumno(alumno)
    curso = obtener_curso_como_estudiante(pk_curso, alumno)
    examen = get_object_or_404(Examen, pk=pk_examen, curso=curso)
    if examen.estado != "activo":
        return redirect('inicio')
    ejercicio = get_object_or_404(Ejercicio, pk=pk_ejercicio)
    ejercicio_examen = get_object_or_404(EjerciciosExamenes, examen=examen, ejercicio=ejercicio)
    respuesta_anterior = obtener_respuesta_anterior_examen(ejercicio_examen, alumno)
    form = RespuestasExamenesForm()
    context["ejercicio"] = ejercicio_examen
    context["curso_activo"] = curso
    if respuesta_anterior:
        context["respuesta_anterior"] = respuesta_anterior
        context["respuesta_nombre"] = str(ejercicio.id) + str(alumno.id)
    context["form"] = form
    template = "alumno/examenes/responder_ejercicio.html"
    if request.method == 'GET':
        return render(request, template, context)
    if request.method == 'POST':
        if not validar_estado_examen(examen):  # verifica que el examen esté activo
            context[
                "error"] = "El examen ha concluido"  # si el examen no está activo, no se guarda la respuesta del
            # estudiante
        else:
            form = obtener_form_respuesta_examen(request, ejercicio_examen, alumno)
            bandera, puntaje = subir_respuesta_ejercicio(form, respuesta_anterior, ejercicio_examen, context)
            if bandera:
                #return redirect(examen.get_absolute_url())
                context['ultimo_puntaje'] = puntaje
                context['redirigir'] = examen.get_absolute_url()
        return render(request, template, context)


@login_required(login_url="/login")
@login_student_required
def editar_perfil(request):
    alumno = get_object_or_404(Alumno, user=request.user)
    context = obtener_informacion_alumno(alumno)
    form_user = UserForm(instance=request.user)
    form_alumno = AlumnoForm(instance=alumno)
    template = "alumno/editar_perfil.html"
    context["form_user"] = form_user
    if request.method == 'GET':
        return render(request, template, context)
    if request.method == 'POST':
        form_user = UserForm(request.POST or None, request.FILES or None, instance=request.user)
        password_actual = request.POST.get("password_actual")
        password_nueva = request.POST.get("password_nueva")
        password_conf = request.POST.get("password_conf")
        if form_user.is_valid():
            user = form_user.save()
            if user.check_password(password_actual) and password_nueva and password_conf:
                if password_nueva == password_conf:
                    user.set_password(password_nueva)
                    user.save()
            return redirect('inicio')
        else:
            context["form_user"] = form_user
        return render(request, template, context)
