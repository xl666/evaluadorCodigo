from django.urls import path, re_path, include

from .views import academico
from .views import alumno
from .views import anonimo
from .views import general

urlpatterns = [
    # urls usuario anonimo
    path('login/', anonimo.iniciar_sesion, name="login"),
    path('academicos/registro', anonimo.registrar_academico, name="registrar_academico"),
    path('alumnos/registro', anonimo.registrar_alumno, name="registrar_alumno"),

    # urls compartidas
    path('', general.inicio, name="inicio"),
    path('logout/', general.cerrar_sesion, name="logout"),
    path('ayuda/', general.ver_ayuda, name="ayuda"),
    path('cursos-<int:pk_curso>/', general.ver_curso, name="curso_detalle"),
    path('cursos-<int:pk_curso>/practicas/', general.ver_listado_practicas, name="listado_practicas"),
    path('cursos-<int:pk_curso>/examenes/', general.ver_listado_examenes, name="listado_examenes"),
    path('cursos-<int:pk_curso>/integrantes/', general.ver_listado_integrantes_curso,
         name="listado_integrantes_curso"),

    # urls usuario académico
    path('perfil-academico/editar', academico.editar_perfil, name="editar_perfil_academico"),
    path('temas/registro', academico.agregar_tema, name="agregar_tema"),
    path('ejercicios/listado', academico.ver_listado_ejercicios, name="listado_ejercicios"),
    path('ejercicios/registro', academico.agregar_ejercicio, name="agregar_ejercicio"),
    re_path(r'^ejercicios/(?P<id_ejercicio>[0-9A-Fa-f-]+)/editar$', academico.editar_ejercicio, name="ejercicio_editar"),
    re_path(r'^ejercicios/(?P<id_ejercicio>[0-9A-Fa-f-]+)/detalle$', academico.ver_detalle_ejercicio,
            name="ejercicio_detalle"),
    path('cursos/registro', academico.agregar_curso, name="agregar_curso"),
    path('cursos/listado', academico.ver_listado_cursos, name="listado_cursos"),
    re_path(r'^cursos-(?P<pk_curso>\d+)/editar$', academico.editar_curso, name="curso_editar"),
    path('cursos-<int:pk_curso>/practicas/registro', academico.agregar_practica, name="agregar_practica"),
    re_path(r'^cursos-(?P<pk_curso>\d+)/practicas-(?P<pk_practica>\d+)/editar$', academico.editar_practica,
            name="editar_practica"),
    re_path(r'^cursos-(?P<pk_curso>\d+)/practicas-(?P<pk_practica>\d+)/eliminar$', academico.eliminar_practica,
            name="eliminar_practica"),
    re_path(r'^cursos-(?P<pk_curso>\d+)/practicas-(?P<pk_practica>\d+)/puntajes$', academico.ver_puntajes_practica,
            name="ver_puntajes_practica"),
    re_path(r'^cursos-(?P<pk_curso>\d+)/practicas-(?P<pk_practica>\d+)/puntajes/respuestas-(?P<pk_respuesta>\d+)$',
            academico.ver_respuesta_ejercicio_practica, name="detalle_respuesta_practica"),
    re_path(r'^cursos-(?P<pk_curso>\d+)/examenes/registro$', academico.agregar_examen, name="agregar_examen"),
    re_path(r'^cursos-(?P<pk_curso>\d+)/examenes-(?P<pk_examen>\d+)/editar$', academico.editar_examen,
            name="editar_examen"),
    re_path(r'^cursos-(?P<pk_curso>\d+)/examenes-(?P<pk_examen>\d+)/eliminar$', academico.eliminar_examen,
            name="eliminar_examen"),
    re_path(r'^cursos-(?P<pk_curso>\d+)/examenes-(?P<pk_examen>\d+)/puntajes$', academico.ver_puntajes_examen,
            name="ver_puntajes_examen"),
    re_path(r'^cursos-(?P<pk_curso>\d+)/examenes-(?P<pk_examen>\d+)/activar$', academico.activar_examen,
            name="activar_examen"),
    re_path(r'^cursos-(?P<pk_curso>\d+)/examenes-(?P<pk_examen>\d+)/administrar$', academico.administrar_examen,
            name="administrar_examen"),
    re_path(r'^cursos-(?P<pk_curso>\d+)/examenes-(?P<pk_examen>\d+)/concluir$', academico.concluir_examen,
            name="concluir_examen"),
    re_path(r'^cursos-(?P<pk_curso>\d+)/examenes-(?P<pk_examen>\d+)/puntajes/respuestas-(?P<pk_respuesta>\d+)$',
            academico.ver_respuesta_ejercicio_examen,
            name="detalle_respuesta_examen"),
    re_path(r'^cursos/(?P<pk_curso>\d+)/puntajes-generales$', academico.ver_puntajes_generales,
            name="ver_puntajes_generales"),

    # urls usuario alumno
    path('perfil-alumno/editar', alumno.editar_perfil, name="editar_perfil_alumno"),
    path('cursos/inscripcion', alumno.inscribir_curso, name="inscribir_curso"),
    re_path(r'^cursos-(?P<pk_curso>\d+)/practicas-(?P<pk_practica>\d+)$', alumno.ver_detalle_practica,
            name="practica_detalle"),
    re_path(r'^cursos-(?P<pk_curso>\d+)/practicas-(?P<pk_practica>\d+)/ejercicios-(?P<pk_ejercicio>[0-9A-Fa-f-]+)$',
            alumno.resolver_ejercicio_practica, name="resolver_ejercicio_practica"),
    re_path(r'^cursos-(?P<pk_curso>\d+)/examenes-(?P<pk_examen>\d+)$', alumno.ver_detalle_examen,
            name="examen_detalle"),
    re_path(r'^cursos-(?P<pk_curso>\d+)/examenes-(?P<pk_examen>\d+)/ejercicios-(?P<pk_ejercicio>[0-9A-Fa-f-]+)$',
            alumno.resolver_ejercicio_examen, name="resolver_ejercicio_examen"),
]