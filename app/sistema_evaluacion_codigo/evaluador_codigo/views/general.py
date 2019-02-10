# -*- coding: utf-8 -*-
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from evaluador_codigo.decorators import redirect_admin
from evaluador_codigo.routines import *


@login_required(login_url="/login")
@redirect_admin
def inicio(request):
    if request.user.is_teacher:
        academico = get_object_or_404(Academico, user=request.user)
        print(academico.user.get_img_url())
        context = obtener_informacion_academico(academico)
        if context["cursos_activos"]:
            curso = context["cursos_activos"].first()
            print(curso.get_num_integrantes())
            return redirect(curso.get_absolute_url())
        return redirect('/cursos/registro')
    elif request.user.is_student:
        alumno = get_object_or_404(Alumno, user=request.user)
        context = obtener_informacion_alumno(alumno)
        if context["cursos_activos"]:
            curso = context["cursos_activos"].first()
            return redirect(curso.get_absolute_url())
        return redirect('/cursos/inscripcion')


@login_required(login_url="/login")
@redirect_admin
def ver_curso(request, pk_curso):
    context = {}
    if request.user.is_teacher:
        academico = get_object_or_404(Academico, user=request.user)
        context = obtener_informacion_academico(academico)
        curso = get_object_or_404(Curso, pk=pk_curso, academico=academico)
        template = "academico/cursos/curso_principal.html"
    elif request.user.is_student:
        alumno = get_object_or_404(Alumno, user=request.user)
        context = obtener_informacion_alumno(alumno)
        curso = obtener_curso_como_estudiante(pk_curso, alumno)
        template = "alumno/cursos/curso_principal.html"
    context["curso_activo"] = curso
    return render(request, template, context)


@login_required(login_url="/login")
@redirect_admin
def ver_listado_practicas(request, pk_curso):
    if request.user.is_teacher:
        academico = get_object_or_404(Academico, user=request.user)
        context = obtener_informacion_academico(academico)
        curso = get_object_or_404(Curso, pk=pk_curso, academico=academico)
        template = "academico/practicas/listado.html"
    elif request.user.is_student:
        alumno = get_object_or_404(Alumno, user=request.user)
        context = obtener_informacion_alumno(alumno)
        curso = obtener_curso_como_estudiante(pk_curso, alumno)
        template = "alumno/practicas/listado.html"
    context["curso_activo"] = curso
    context["practicas"] = obtener_practicas(curso)
    return render(request, template, context)


@login_required(login_url="/login")
@redirect_admin
def ver_listado_examenes(request, pk_curso):
    if request.user.is_teacher:
        academico = get_object_or_404(Academico, user=request.user)
        context = obtener_informacion_academico(academico)
        curso = get_object_or_404(Curso, pk=pk_curso, academico=academico)
        try:
            examen_activo = Examen.objects.get(estado="activo", curso=curso)
            if examen_activo:
                return redirect(examen_activo.get_administrar_url())
        except:
            context["examenes"] = obtener_examenes_como_academico(curso)
            template = "academico/examenes/listado.html"
    elif request.user.is_student:
        alumno = get_object_or_404(Alumno, user=request.user)
        context = obtener_informacion_alumno(alumno)
        curso = obtener_curso_como_estudiante(pk_curso, alumno)
        context["examenes"] = obtener_examenes_como_alumno(curso)
        template = "alumno/examenes/listado.html"
    context["curso_activo"] = curso
    return render(request, template, context)


@login_required(login_url="/login")
@redirect_admin
def ver_listado_integrantes_curso(request, pk_curso):
    if request.user.is_teacher:
        academico = get_object_or_404(Academico, user=request.user)
        context = obtener_informacion_academico(academico)
        curso = get_object_or_404(Curso, pk=pk_curso, academico=academico)
        template = "academico/cursos/listado_integrantes.html"
    elif request.user.is_student:
        alumno = get_object_or_404(Alumno, user=request.user)
        context = obtener_informacion_alumno(alumno)
        curso = obtener_curso_como_estudiante(pk_curso, alumno)
        template = "alumno/cursos/listado_integrantes.html"
    context["curso_activo"] = curso
    return render(request, template, context)


@login_required(login_url="/login")
@redirect_admin
def ver_ayuda(request):
    if request.user.is_teacher:
        academico = get_object_or_404(Academico, user=request.user)
        context = obtener_informacion_academico(academico)
        template = "academico/ayuda.html"
        return render(request, template, context)
    elif request.user.is_student:
        alumno = get_object_or_404(Alumno, user=request.user)
        context = obtener_informacion_alumno(alumno)
        template = "alumno/ayuda.html"
        return render(request, template, context)


@login_required(login_url="/login")
def cerrar_sesion(request):
    logout(request)
    return redirect('inicio')
