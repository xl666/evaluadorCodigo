from django.conf.urls import url

from .views import academico
from .views import alumno
from .views import anonimo
from .views import general

urlpatterns = [
    # urls usuario anonimo
    url(r'^login/', anonimo.iniciar_sesion, name="login"),
    url(r'^academicos/registro', anonimo.registrar_academico, name="registrar_academico"),
    url(r'^alumnos/registro', anonimo.registrar_alumno, name="registrar_alumno"),

    # urls compartidas
    url(r'^$', general.inicio, name="inicio"),
    url(r'^logout/', general.cerrar_sesion, name="logout"),
    url(r'^ayuda/$', general.ver_ayuda, name="ayuda"),
    url(r'^cursos-(?P<pk_curso>\d+)$', general.ver_curso, name="curso_detalle"),
    url(r'^cursos-(?P<pk_curso>\d+)/practicas$', general.ver_listado_practicas, name="listado_practicas"),
    url(r'^cursos-(?P<pk_curso>\d+)/examenes$', general.ver_listado_examenes, name="listado_examenes"),
    url(r'^cursos-(?P<pk_curso>\d+)/integrantes$', general.ver_listado_integrantes_curso,
        name="listado_integrantes_curso"),

    # urls usuario académico
    url(r'^perfil-academico/editar', academico.editar_perfil, name="editar_perfil_academico"),
    url(r'^temas/registro', academico.agregar_tema, name="agregar_tema"),
    url(r'^ejercicios/listado', academico.ver_listado_ejercicios, name="listado_ejercicios"),
    url(r'^ejercicios/registro', academico.agregar_ejercicio, name="agregar_ejercicio"),
    url(r'^ejercicios/(?P<id_ejercicio>[0-9A-Fa-f-]+)/editar$', academico.editar_ejercicio, name="ejercicio_editar"),
    url(r'^ejercicios/(?P<id_ejercicio>[0-9A-Fa-f-]+)/detalle$', academico.ver_detalle_ejercicio,
        name="ejercicio_detalle"),
    url(r'^cursos/registro', academico.agregar_curso, name="agregar_curso"),
    url(r'^cursos/listado', academico.ver_listado_cursos, name="listado_cursos"),
    url(r'^cursos-(?P<pk_curso>\d+)/editar$', academico.editar_curso, name="curso_editar"),
    url(r'^cursos-(?P<pk_curso>\d+)/practicas/registro$', academico.agregar_practica, name="agregar_practica"),
    url(r'^cursos-(?P<pk_curso>\d+)/practicas-(?P<pk_practica>\d+)/editar$', academico.editar_practica,
        name="editar_practica"),
    url(r'^cursos-(?P<pk_curso>\d+)/practicas-(?P<pk_practica>\d+)/eliminar$', academico.eliminar_practica,
        name="eliminar_practica"),
    url(r'^cursos-(?P<pk_curso>\d+)/practicas-(?P<pk_practica>\d+)/puntajes$', academico.ver_puntajes_practica,
        name="ver_puntajes_practica"),
    url(r'^cursos-(?P<pk_curso>\d+)/practicas-(?P<pk_practica>\d+)/puntajes/respuestas-(?P<pk_respuesta>\d+)$',
        academico.ver_respuesta_ejercicio_practica, name="detalle_respuesta_practica"),
    url(r'^cursos-(?P<pk_curso>\d+)/examenes/registro$', academico.agregar_examen, name="agregar_examen"),
    url(r'^cursos-(?P<pk_curso>\d+)/examenes-(?P<pk_examen>\d+)/editar$', academico.editar_examen,
        name="editar_examen"),
    url(r'^cursos-(?P<pk_curso>\d+)/examenes-(?P<pk_examen>\d+)/eliminar$', academico.eliminar_examen,
        name="eliminar_examen"),
    url(r'^cursos-(?P<pk_curso>\d+)/examenes-(?P<pk_examen>\d+)/puntajes$', academico.ver_puntajes_examen,
        name="ver_puntajes_examen"),
    url(r'^cursos-(?P<pk_curso>\d+)/examenes-(?P<pk_examen>\d+)/activar$', academico.activar_examen,
        name="activar_examen"),
    url(r'^cursos-(?P<pk_curso>\d+)/examenes-(?P<pk_examen>\d+)/administrar$', academico.administrar_examen,
        name="administrar_examen"),
    url(r'^cursos-(?P<pk_curso>\d+)/examenes-(?P<pk_examen>\d+)/concluir$', academico.concluir_examen,
        name="concluir_examen"),
    url(r'^cursos-(?P<pk_curso>\d+)/examenes-(?P<pk_examen>\d+)/puntajes/respuestas-(?P<pk_respuesta>\d+)$',
        academico.ver_respuesta_ejercicio_examen,
        name="detalle_respuesta_examen"),
    url(r'^cursos/(?P<pk_curso>\d+)/puntajes-generales$', academico.ver_puntajes_generales,
        name="ver_puntajes_generales"),

    # urls usuario alumno
    url(r'^perfil-alumno/editar', alumno.editar_perfil, name="editar_perfil_alumno"),
    url(r'^cursos/inscripcion', alumno.inscribir_curso, name="inscribir_curso"),
    url(r'^cursos-(?P<pk_curso>\d+)/practicas-(?P<pk_practica>\d+)$', alumno.ver_detalle_practica,
        name="practica_detalle"),
    url(r'^cursos-(?P<pk_curso>\d+)/practicas-(?P<pk_practica>\d+)/ejercicios-(?P<pk_ejercicio>[0-9A-Fa-f-]+)$',
        alumno.resolver_ejercicio_practica, name="resolver_ejercicio_practica"),
    url(r'^cursos-(?P<pk_curso>\d+)/examenes-(?P<pk_examen>\d+)$', alumno.ver_detalle_examen, name="examen_detalle"),
    url(r'^cursos-(?P<pk_curso>\d+)/examenes-(?P<pk_examen>\d+)/ejercicios-(?P<pk_ejercicio>[0-9A-Fa-f-]+)$',
        alumno.resolver_ejercicio_examen, name="resolver_ejercicio_examen"),

    ]
