from datetime import datetime, timedelta

from django.test import Client
from django.test import TestCase

from evaluador_codigo.models import *


class EvaluadorModelsTest(TestCase):
    def setUp(self):
        # Every test needs a client.
        self.client = Client()
        self.fecha_actual = datetime.now()

    def crear_usuario(self, username="angelsg", first_name="Ángel Juan", last_name="Sánchez García",
                      email="angel@gmail.com", password="camilo123", is_teacher=True, is_student=False):
        return User.objects.create_user(username=username, first_name=first_name, last_name=last_name, email=email,
                                        password=password, is_teacher=is_teacher, is_student=is_student)

    def crear_licenciaturas(self):
        lic1 = Licenciatura.objects.create(licenciatura="Ingeniería de software")
        lic2 = Licenciatura.objects.create(licenciatura="Tecnologías computacionales")
        return lic1, lic2

    def crear_exp_educativa(self):
        return ExperienciaEducativa.objects.create(exp_educativa="Introducción a la programación")

    def crear_tema(self):
        return Tema.objects.create(tema="Búsquedas")

    def crear_periodo(self):
        return Periodo.objects.create(periodo="agosto 2018 - enero 2019")

    def crear_academico(self, user):
        return Academico.objects.create(user=user)

    def crear_alumno(self, user):
        lic1, lic2 = self.crear_licenciaturas()
        return Alumno.objects.create(user=user, matricula="s14011632", licenciatura=lic1)

    def crear_curso(self):
        lic1, lic2 = self.crear_licenciaturas()
        exp1 = self.crear_exp_educativa()
        periodo1 = self.crear_periodo()
        return Curso.objects.create(licenciatura=lic1, exp_educativa=exp1, periodo=periodo1, nrc="29832", bloque="1",
                                    seccion="2", codigo_inscripcion="12345",
                                    academico=self.crear_academico(self.crear_usuario()))

    def crear_ejercicio(self):
        academico = self.crear_academico(
            self.crear_usuario(username="xavier", first_name="Héctor Xavier", last_name="Limón Riaño",
                               email="xavier@gmail.com", password="camilo123", is_student=False, is_teacher=True))
        ejercicio = Ejercicio.objects.create(nombre="Ejercicio 1", descripcion="realizar una suma",
                                             entrada="dos números enteros", salida="número entero",
                                             ejemplo_entrada="1 2", ejemplo_salida="3", publico=True,
                                             academico=academico)
        return ejercicio

    def crear_practica(self, inicio, termino):
        practica = Practica.objects.create(nombre="Práctica 1", inicio=inicio, termino=termino, descripcion="",
                                           curso=self.crear_curso())
        ejercicio_practica = EjerciciosPracticas(practica=practica, ejercicio=self.crear_ejercicio(), puntaje=10)
        return practica, ejercicio_practica

    def crear_examen(self):
        examen = Examen.objects.create(nombre="Primer parcial", descripcion="", curso=self.crear_curso())
        ejercicio_examen = EjerciciosExamenes(examen=examen, ejercicio=self.crear_ejercicio(), puntaje=10)
        return examen, ejercicio_examen

    def test_crear_usuario(self):
        user = self.crear_usuario(is_teacher=True, is_student=False)
        self.assertTrue(isinstance(user, User))

    def test_crear_academico(self):
        academico = self.crear_academico(self.crear_usuario())
        self.assertTrue(isinstance(academico, Academico))

    def test_crear_alumno(self):
        alumno = self.crear_alumno(
            self.crear_usuario(username="susana14", first_name="Susana", last_name="González Portilla",
                               email="susana@gmail.com", password="camilo123", is_student=True, is_teacher=False))
        self.assertTrue(isinstance(alumno, Alumno))

    def test_crear_periodo(self):
        periodo = self.crear_periodo()
        self.assertTrue(isinstance(periodo, Periodo))

    def test_crear_tema(self):
        tema = self.crear_tema()
        self.assertTrue(isinstance(tema, Tema))

    def test_crear_curso(self):
        curso = self.crear_curso()
        self.assertTrue(isinstance(curso, Curso))
        self.assertEqual(curso.activo, True)
        self.assertEqual(curso.get_num_integrantes(), 1)
        self.assertEqual(curso.get_num_practicas_activas(), 0)
        self.assertEqual(curso.get_num_examenes_activos(), 0)

    def test_crear_ejercicio(self):
        ejercicio = self.crear_ejercicio()
        self.assertTrue(isinstance(ejercicio, Ejercicio))

    def test_crear_practica_activa(self):
        inicio = self.fecha_actual
        termino = self.fecha_actual + timedelta(days=1)
        inicio.strftime("%Y-%m-%d %H:%M:%S")
        termino.strftime("%Y-%m-%d %H:%M:%S")
        practica, ejercicio_practica = self.crear_practica(inicio, termino)
        self.assertTrue(isinstance(practica, Practica))
        self.assertTrue(isinstance(ejercicio_practica, EjerciciosPracticas))
        self.assertEqual(practica.get_estado(), "activa")

    def test_crear_practica_por_iniciar(self):
        inicio = self.fecha_actual + timedelta(days=1)
        termino = self.fecha_actual + timedelta(days=2)
        inicio.strftime("%Y-%m-%d %H:%M:%S")
        termino.strftime("%Y-%m-%d %H:%M:%S")
        practica, ejercicio_practica = self.crear_practica(inicio, termino)
        self.assertTrue(isinstance(practica, Practica))
        self.assertTrue(isinstance(ejercicio_practica, EjerciciosPracticas))
        self.assertEqual(practica.get_estado(), "por iniciar")

    def test_crear_examen(self):
        examen, ejercicio_examen = self.crear_examen()
        self.assertTrue(isinstance(examen, Examen))
        self.assertTrue(isinstance(ejercicio_examen, EjerciciosExamenes))
        self.assertEqual(examen.estado, "por iniciar")
