# -*- coding: utf-8 -*-
import uuid  # Requerida para las instancias de ejercicios únicos
from datetime import datetime

import pytz
import tzlocal
from django.conf import settings
from django.contrib.auth.models import AbstractUser, UserManager
from django.core.files.storage import FileSystemStorage
from django.core.validators import FileExtensionValidator
from django.db import models
from django.shortcuts import reverse
from django.utils import timezone

from sistema_evaluacion_codigo.base import *

timezone.activate('America/Mexico_City')


class OverwriteStorage(FileSystemStorage):
    '''
        Cambia el comportamiento predeterminado de Django y lo hace sobrescribir archivos de
        el mismo nombre que fueron cargados por el usuario
    '''

    def get_available_name(self, name, max_length=None):
        self.delete(name)
        return name


def get_upload_img_profile(instance, filename):
    file_extension = os.path.splitext(filename)[1]
    file_path = os.path.join("imagenes", "perfiles", str(instance.id), str(instance.id) + str(file_extension))
    return file_path


class User(AbstractUser):
    is_student = models.BooleanField('Estudiante', default=False)
    is_teacher = models.BooleanField('Académico', default=False)
    img_profile = models.ImageField("Imagen de perfil", upload_to=get_upload_img_profile, null=True, blank=True,
                                    storage=OverwriteStorage(), max_length=200)
    objects = UserManager()

    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"

    def __str__(self):
        return self.first_name + ' ' + self.last_name

    def __unicode__(self):
        if __name__ == '__main__':
            return self.first_name + ' ' + self.last_name

    def get_img_url(self):
        if self.img_profile:
            file_url = self.img_profile.url
        else:
            file_url = os.path.join(settings.MEDIA_URL, "imagenes", "perfiles", "user-default.png")
        return file_url


class Licenciatura(models.Model):
    licenciatura = models.CharField("Licenciatura", null=False, blank=False, max_length=50, unique=True)

    class Meta:
        verbose_name = "Licenciatura"
        verbose_name_plural = "Licenciaturas"
        ordering = ['licenciatura', ]

    def __str__(self):
        return self.licenciatura

    def __unicode__(self):
        return self.licenciatura


class Periodo(models.Model):
    periodo = models.CharField("Periodo", null=False, blank=False, max_length=50, unique=True)

    class Meta:
        verbose_name = "Periodo"
        verbose_name_plural = "Periodos"
        ordering = ['periodo', ]

    def __str__(self):
        return self.periodo

    def __unicode__(self):
        return self.periodo


class Academico(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=False, blank=False)
    licenciaturas = models.ManyToManyField(Licenciatura)

    class Meta:
        verbose_name = "Académico"
        verbose_name_plural = "Academicos"

    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name

    def __unicode__(self):
        return self.user.first_name + ' ' + self.user.last_name


class ExperienciaEducativa(models.Model):
    exp_educativa = models.CharField("Experiencia educativa", null=False, blank=False, max_length=50, unique=True)

    class Meta:
        verbose_name = "Experiencia educativa"
        verbose_name_plural = "Experiencias educativas"
        ordering = ['exp_educativa', ]

    def __str__(self):
        return self.exp_educativa

    def __unicode__(self):
        return self.exp_educativa


class Tema(models.Model):
    tema = models.CharField("Tema", null=False, blank=False, max_length=250, unique=True)

    class Meta:
        verbose_name = "Tema"
        verbose_name_plural = "Temas"

    def __str__(self):
        return self.tema

    def __unicode__(self):
        return self.tema


class Curso(models.Model):
    exp_educativa = models.ForeignKey(ExperienciaEducativa, related_name='cursos', on_delete=models.CASCADE, null=False,
                                      blank=False)
    nrc = models.CharField("NRC", null=False, blank=False, max_length=5)
    periodo = models.ForeignKey(Periodo, on_delete=models.CASCADE)
    activo = models.BooleanField("Activo", default=True)
    bloque = models.CharField("Bloque", null=False, blank=False, max_length=2)
    seccion = models.CharField("Sección", null=False, blank=False, max_length=2)
    academico = models.ForeignKey(Academico, on_delete=models.CASCADE, null=True, blank=False)
    codigo_inscripcion = models.CharField("Código de inscripción", null=False, blank=False, max_length=10)
    licenciatura = models.ForeignKey(Licenciatura, related_name='cursos', on_delete=models.CASCADE, null=False,
                                     blank=False)

    class Meta:
        verbose_name = "Curso"
        verbose_name_plural = "Cursos"
        unique_together = (('nrc', 'periodo'),)
        ordering = ['exp_educativa', ]

    def __str__(self):
        return self.nrc + ' ' + self.exp_educativa.exp_educativa

    def __unicode__(self):
        return self.nrc + ' ' + self.exp_educativa.exp_educativa

    def get_absolute_url(self):
        return reverse("curso_detalle", args=[str(self.pk)])

    def get_edit_url(self):
        return reverse("curso_editar", args=[str(self.pk)])

    def get_add_practica_url(self):
        return reverse("agregar_practica", args=[str(self.pk)])

    def get_add_examen_url(self):
        return reverse("agregar_examen", args=[str(self.pk)])

    def get_listado_practicas_url(self):
        return reverse("listado_practicas", args=[str(self.pk)])

    def get_listado_examenes_url(self):
        return reverse("listado_examenes", args=[str(self.pk)])

    def get_listado_integrantes_url(self):
        return reverse("listado_integrantes_curso", args=[str(self.pk)])

    def get_listado_puntajes_url(self):
        return reverse("ver_puntajes_generales", args=[str(self.pk)])

    def get_num_practicas_activas(self):
        practicas_activas = 0
        for practica in self.practicas.all():
            if practica.get_estado() == "activa":
                practicas_activas = practicas_activas + 1
        return practicas_activas

    def get_num_examenes_activos(self):
        return len(self.examenes.filter(estado="activo"))

    def get_num_integrantes(self):
        return len(self.alumnos.all()) + 1


def get_upload_casos_prueba(instance, filename):
    file_path = os.path.join("ejercicios", "casos_de_prueba", str(instance.id) + ".txt")
    return file_path


def get_upload_archivo_apoyo(instance, filename):
    file_extension = os.path.splitext(filename)[1]
    file_path = os.path.join("ejercicios", "archivos_apoyo", str(instance.id) + file_extension)
    return file_path


class Ejercicio(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    nombre = models.CharField("Nombre", null=False, blank=False, max_length=100, unique=True)
    experiencias_educativas = models.ManyToManyField(ExperienciaEducativa)
    temas = models.ManyToManyField(Tema)
    publico = models.BooleanField("Público", default=False)
    academico = models.ForeignKey(Academico, on_delete=models.CASCADE, null=True, blank=True)
    descripcion = models.TextField("Descripción", null=False, blank=False)
    entrada = models.TextField("Entrada", null=True, blank=True)
    salida = models.TextField("Salida", null=True, blank=True)
    ejemplo_entrada = models.TextField("Ejemplo entrada", null=False, blank=False)
    ejemplo_salida = models.TextField("Ejemplo salida", null=False, blank=False)
    casos_prueba = models.FileField("Casos de prueba", upload_to=get_upload_casos_prueba, storage=OverwriteStorage(),
                                    max_length=500)
    archivo_apoyo = models.FileField("Archivo de apoyo", upload_to=get_upload_archivo_apoyo, null=True, blank=True,
                                     storage=OverwriteStorage(), max_length=500)

    class Meta:
        verbose_name = "Ejercicio"
        verbose_name_plural = "Ejercicios"
        ordering = ['nombre', ]

    def __str__(self):
        return self.nombre

    def __unicode__(self):
        return self.nombre

    def get_absolute_url(self):
        return reverse("ejercicio_detalle", args=[str(self.id)])

    def get_edit_url(self):
        return reverse("ejercicio_editar", args=[str(self.id)])


class Practica(models.Model):
    nombre = models.CharField("Nombre", null=False, blank=False, max_length=100)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name="practicas")
    inicio = models.DateTimeField("Fecha inicio", null=False, blank=False)
    termino = models.DateTimeField("Fecha término", null=False, blank=False)
    descripcion = models.TextField("Descripción", null=True, blank=True)
    ejercicios = models.ManyToManyField(Ejercicio, through='EjerciciosPracticas')

    class Meta:
        verbose_name = "Práctica"
        verbose_name_plural = "Prácticas"

    def __str__(self):
        return self.nombre

    def __unicode__(self):
        return self.nombre

    def get_absolute_url(self):
        return reverse("practica_detalle", args=[str(self.curso.pk), str(self.pk)])

    def get_edit_url(self):
        return reverse("editar_practica", args=[str(self.curso.pk), str(self.pk)])

    def get_delete_url(self):
        return reverse("eliminar_practica", args=[str(self.curso.pk), str(self.pk)])

    def get_puntajes_url(self):
        return reverse("ver_puntajes_practica", args=[str(self.curso.pk), str(self.pk)])

    def get_estado(self):
        local_timezone = tzlocal.get_localzone()  # get pytz tzinfo
        inicio = self.inicio.strftime("%Y-%m-%d %H:%M:%S")
        termino = self.termino.strftime("%Y-%m-%d %H:%M:%S")
        utc_time = datetime.strptime(inicio, "%Y-%m-%d %H:%M:%S")
        local_time_inicio = utc_time.replace(tzinfo=pytz.utc).astimezone(local_timezone)
        utc_time = datetime.strptime(termino, "%Y-%m-%d %H:%M:%S")
        local_time_termino = utc_time.replace(tzinfo=pytz.utc).astimezone(local_timezone)
        if local_time_inicio <= timezone.now():
            if local_time_termino > timezone.now():
                estado = "activa"
            else:
                estado = "cerrada"
        else:
            estado = "por iniciar"
        return estado

    def get_puntaje(self):
        puntaje = 0
        ejercicios = EjerciciosPracticas.objects.filter(practica=self)
        for ejercicio in ejercicios:
            puntaje = puntaje + ejercicio.puntaje
        return puntaje

    def get_puntaje_obtenido(self, alumno):
        puntaje_obtenido = 0
        ejercicios = EjerciciosPracticas.objects.filter(practica=self)
        for ejercicio in ejercicios:
            respuesta = RespuestasPracticas.objects.get(ejercicio=ejercicio, alumno=alumno)
            puntaje_obtenido = puntaje_obtenido + respuesta.puntaje_obtenido
        return puntaje_obtenido


class EjerciciosPracticas(models.Model):
    practica = models.ForeignKey(Practica, on_delete=models.CASCADE, null=False, blank=False)
    ejercicio = models.ForeignKey(Ejercicio, on_delete=models.CASCADE, null=False, blank=False)
    puntaje = models.IntegerField("Puntaje", null=False, blank=False)

    class Meta:
        verbose_name = "Ejercicios de práctica"
        verbose_name_plural = "Ejercicios de prácticas"

    def __str__(self):
        return self.ejercicio.nombre

    def __unicode__(self):
        return self.ejercicio.nombre

    def get_ejercicio_url(self):
        return reverse("resolver_ejercicio_practica",
                       args=[str(self.practica.curso.pk), str(self.practica.pk), str(self.ejercicio.pk)])


class Examen(models.Model):
    nombre = models.CharField("Examen", null=False, blank=False, max_length=100)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name="examenes")
    estado = models.CharField("Estado", max_length=11, default="por iniciar")
    fecha_inicio = models.DateTimeField("Fecha inicio", null=True, blank=True)
    fecha_termino = models.DateTimeField("Fecha término", null=True, blank=True)
    descripcion = models.TextField("Descripción", null=True, blank=True)
    ejercicios = models.ManyToManyField(Ejercicio, through='EjerciciosExamenes')

    class Meta:
        verbose_name = "Examen"
        verbose_name_plural = "Exámenes"

    def __str__(self):
        return self.nombre

    def __unicode__(self):
        return self.nombre

    def get_absolute_url(self):
        return reverse("examen_detalle", args=[str(self.curso.pk), str(self.pk)])

    def get_edit_url(self):
        return reverse("editar_examen", args=[str(self.curso.pk), str(self.pk)])

    def get_delete_url(self):
        return reverse("eliminar_examen", args=[str(self.curso.pk), str(self.pk)])

    def get_activar_url(self):
        return reverse("activar_examen", args=[str(self.curso.pk), str(self.pk)])

    def get_administrar_url(self):
        return reverse("administrar_examen", args=[str(self.curso.pk), str(self.pk)])

    def get_concluir_url(self):
        return reverse("concluir_examen", args=[str(self.curso.pk), str(self.pk)])

    def get_puntajes_url(self):
        return reverse("ver_puntajes_examen", args=[str(self.curso.pk), str(self.pk)])

    def get_puntaje(self):
        puntaje = 0
        ejercicios = EjerciciosExamenes.objects.filter(examen=self)
        for ejercicio in ejercicios:
            puntaje = puntaje + ejercicio.puntaje
        return puntaje

    def get_puntaje_obtenido(self, alumno):
        puntaje_obtenido = 0
        ejercicios = EjerciciosExamenes.objects.filter(examen=self)
        for ejercicio in ejercicios:
            respuesta = RespuestasExamenes.objects.get(ejercicio=ejercicio, alumno=alumno)
            puntaje_obtenido = puntaje_obtenido + respuesta.puntaje_obtenido
        return puntaje_obtenido


class EjerciciosExamenes(models.Model):
    examen = models.ForeignKey(Examen, on_delete=models.CASCADE, null=False, blank=False)
    ejercicio = models.ForeignKey(Ejercicio, on_delete=models.CASCADE, null=False, blank=False)
    puntaje = models.IntegerField("Puntaje", null=False, blank=False)

    class Meta:
        verbose_name = "Ejercicios de práctica"
        verbose_name_plural = "Ejercicios de prácticas"

    def __str__(self):
        return str(self.puntaje)

    def __unicode__(self):
        return str(self.puntaje)

    def get_ejercicio_url(self):
        return reverse("resolver_ejercicio_examen",
                       args=[str(self.examen.curso.pk), str(self.examen.pk), str(self.ejercicio.pk)])


class Alumno(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=False)
    matricula = models.CharField("Matrícula", null=False, blank=False, max_length=9, unique=True)
    licenciatura = models.ForeignKey(Licenciatura, on_delete=models.CASCADE, null=False, blank=False)
    cursos = models.ManyToManyField(Curso, related_name="alumnos")
    respuestas_examenes = models.ManyToManyField(EjerciciosExamenes, through='RespuestasExamenes')
    respuestas_practicas = models.ManyToManyField(EjerciciosPracticas, through='RespuestasPracticas')

    class Meta:
        verbose_name = "Alumno"
        verbose_name_plural = "Alumnos"

    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name

    def __unicode__(self):
        return self.user.first_name + ' ' + self.user.last_name

    def get_puntajes_practicas(self):
        pass


def get_upload_respuesta_practica(instance, filename):
    file_extension = os.path.splitext(filename)[1]
    file_path = os.path.join("practicas", "practica" + str(instance.ejercicio.practica.id),
                             str(instance.alumno.matricula), str(instance.ejercicio.ejercicio.id),
                             str(instance.ejercicio.ejercicio.id) + file_extension)
    return file_path


def get_upload_respuesta_temporal_practica(instance, filename):
    file_extension = os.path.splitext(filename)[1]
    file_path = os.path.join("practicas", "practica" + str(instance.ejercicio.practica.id),
                             str(instance.alumno.matricula), str(instance.ejercicio.ejercicio.id), filename)
    return file_path


class RespuestasPracticas(models.Model):
    ejercicio = models.ForeignKey(EjerciciosPracticas, on_delete=models.CASCADE)
    alumno = models.ForeignKey(Alumno, related_name='respuesta_practica', on_delete=models.CASCADE, null=False,
                               blank=False)
    puntaje_obtenido = models.IntegerField("Puntaje", default=0)
    archivo_respuesta = models.FileField("Respuesta", upload_to=get_upload_respuesta_practica, null=False, blank=False,
                                         validators=[FileExtensionValidator(
                                             allowed_extensions=['py', 'java', 'prolog', 'cpp', 'c', 'lisp', 'zip'])],
                                         storage=OverwriteStorage(), max_length=500)
    archivo_respuesta_temporal = models.FileField("Respuesta temporal",
                                                  upload_to=get_upload_respuesta_temporal_practica, null=True,
                                                  blank=True, validators=[
            FileExtensionValidator(allowed_extensions=['py', 'java', 'prolog', 'cpp', 'c', 'lisp', 'zip'])],
                                                  storage=OverwriteStorage(), max_length=500)
    fecha_enviado = models.DateTimeField("Fecha enviado", auto_now=True)
    error = models.CharField("Error", null=True, max_length=100)

    class Meta:
        verbose_name = "Respuesta de ejercicio"
        verbose_name_plural = "Respuesta de ejercicio"
        unique_together = (('ejercicio', 'alumno'),)

    def __str__(self):
        return str(self.puntaje_obtenido)

    def __unicode__(self):
        return str(self.puntaje_obtenido)

    def delete(self, *args, **kwargs):
        if os.path.isfile(self.archivo_respuesta.path):
            os.remove(self.archivo_respuesta.path)
        super(RespuestasPracticas, self).delete(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("detalle_respuesta_practica",
                       args=[str(self.ejercicio.practica.curso.pk), str(self.ejercicio.practica.pk), str(self.pk)])

    # obtiene la ruta donde se guardarán todos los archivos(zip, compilados) de respuesta del estudiante
    def get_path(self):
        file_path = os.path.join(settings.BASE_DIR, "media", "practicas", "practica" + str(self.ejercicio.practica.id),
                                 str(self.alumno.matricula), str(self.ejercicio.ejercicio.id), )
        return file_path

    # obtiene la ruta de un archivo en específico, puede ser un compilado por ejemplo
    def get_path_archivo(self, filename):
        file_path = os.path.join(settings.BASE_DIR, "media", "practicas", "practica" + str(self.ejercicio.practica.id),
                                 str(self.alumno.matricula), str(self.ejercicio.ejercicio.id), filename)
        return file_path


def get_upload_respuesta_examen(instance, filename):
    file_extension = os.path.splitext(filename)[1]
    file_path = os.path.join("examenes", "examen" + str(instance.ejercicio.examen.id), str(instance.alumno.matricula),
                             str(instance.ejercicio.ejercicio.id),
                             str(instance.ejercicio.ejercicio.id) + file_extension)
    return file_path


def get_upload_respuesta_temporal_examen(instance, filename):
    file_extension = os.path.splitext(filename)[1]
    file_path = os.path.join("examenes", "examen" + str(instance.ejercicio.examen.id), str(instance.alumno.matricula),
                             str(instance.ejercicio.ejercicio.id), filename)
    return file_path


class RespuestasExamenes(models.Model):
    ejercicio = models.ForeignKey(EjerciciosExamenes, on_delete=models.CASCADE)
    alumno = models.ForeignKey(Alumno, related_name='respuesta_examen', on_delete=models.CASCADE, null=False,
                               blank=False)
    puntaje_obtenido = models.IntegerField("Puntaje", default=0)
    archivo_respuesta = models.FileField("Respuesta", upload_to=get_upload_respuesta_examen, null=False, blank=False,
                                         validators=[FileExtensionValidator(
                                             allowed_extensions=['py', 'java', 'prolog', 'cpp', 'c', 'lisp', 'zip'])],
                                         storage=OverwriteStorage(), max_length=500)
    archivo_respuesta_temporal = models.FileField("Respuesta temporal", upload_to=get_upload_respuesta_temporal_examen,
                                                  null=True, blank=True, validators=[
            FileExtensionValidator(allowed_extensions=['py', 'java', 'prolog', 'cpp', 'c', 'lisp', 'zip'])],
                                                  storage=OverwriteStorage(), max_length=500)
    fecha_enviado = models.DateTimeField("Fecha enviado", auto_now=True)
    error = models.CharField("Error", null=True, max_length=100)

    class Meta:
        verbose_name = "Respuesta de ejercicio"
        verbose_name_plural = "Respuesta de ejercicio"
        unique_together = (('ejercicio', 'alumno'),)

    def __str__(self):
        return str(self.puntaje_obtenido)

    def __unicode__(self):
        return str(self.puntaje_obtenido)

    def get_absolute_url(self):
        return reverse("detalle_respuesta_examen",
                       args=[str(self.ejercicio.examen.curso.pk), str(self.ejercicio.examen.pk), str(self.pk)])

    def get_path(self):
        file_path = os.path.join(settings.BASE_DIR, "media", "examenes", "examen" + str(self.ejercicio.examen.id),
                                 str(self.alumno.matricula), str(self.ejercicio.ejercicio.id), )
        return file_path

    def get_path_archivo(self, filename):
        file_path = os.path.join(settings.BASE_DIR, "media", "examenes", "examen" + str(self.ejercicio.examen.id),
                                 str(self.alumno.matricula), str(self.ejercicio.ejercicio.id), filename)
        return file_path
