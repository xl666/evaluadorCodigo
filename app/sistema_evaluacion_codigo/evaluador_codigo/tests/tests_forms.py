from django.test import TestCase, RequestFactory
from django.test import Client
from evaluador_codigo.forms import *
from evaluador_codigo.models import User, ExperienciaEducativa, Periodo,Tema,Licenciatura
from django.core.files import File
import mock

class EvaluadorFormsTest(TestCase):
    fixtures = ["initial_data.json"]

    def setUp(self):
        # Every test needs a client.

        self.client = Client()

    def test_user_form(self):
        form_data = {"username":"roy", "first_name":"Rodrigo", "last_name":"Ruíz Salmorán",
                     "email":"roy@hotmail.com"}
        form = UserForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_user_form_invalido(self):
        form_data = {"username": "revo", "first_name": "", "last_name": "Pérez Arriaga",
                     "email": "elrevo@hotmail.com"}
        form = UserForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_academico_form(self):
        form_data = {"licenciaturas":[1,2]}
        form = AcademicoForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_academico_form_invalido(self):
        form_data = {"licenciaturas" :""}
        form = AcademicoForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_alumno_form(self):
        form_data = {"licenciatura": 1,"matricula":"s14011656"}
        form = AlumnoForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_alumno_form_invalido(self):
        form_data = {"licenciatura": 1,"matricula":""}
        form = AlumnoForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_curso_form(self):
        academico = Academico.objects.get(id=3)
        form_data = {"licenciatura": 1, "exp_educativa": 1,
                     "periodo": 1, "nrc": "29832", "bloque": "1", "seccion": "2",
                     "codigo_inscripcion": "12345", "activo": True}
        form = CursoForm(academico,data=form_data)
        self.assertTrue(form.is_valid())

    def test_curso_form_invalido(self):
        academico = Academico.objects.get(id=3)
        form_data = {"licenciatura": 1, "exp_educativa": "",
                     "periodo": 1, "nrc": "29832", "bloque": "1", "seccion": "2",
                     "codigo_inscripcion": "12345", "activo": True}
        form = CursoForm(academico,data=form_data)
        self.assertFalse(form.is_valid())

    def test_ejercicio_form(self):
        form_data = {"nombre":"Ejercicio 1", "experiencias_educativas":[1], "temas":[1],
                    "descripcion":"realizar una suma", "entrada":"dos números enteros", "salida":"número entero",
                     "ejemplo_entrada":"1 2", "ejemplo_salida":"3",
                  "archivo_apoyo":"", "publico":True}
        form = EjercicioForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_ejercicio_form_invalido(self):
        form_data = {"nombre":"Ejercicio 1", "experiencias_educativas":[1], "temas":[1],
                    "descripcion":"", "entrada":"dos números enteros", "salida":"número entero",
                     "ejemplo_entrada":"1 2", "ejemplo_salida":"3",
                  "archivo_apoyo":"", "publico":True}
        form = EjercicioForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_practica_form(self):
        form_data = {"nombre": "Práctica 1", "inicio": "2018-09-12 00:13:22", "termino": "2018-10-12 00:13:22",
                     "descripcion": ""}
        form = PracticaForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_practica_form_invalido(self):
        form_data = {"nombre": "", "inicio": "2018-09-12 00:13:22", "termino": "2018-10-12 00:13:22",
                     "descripcion": ""}
        form = PracticaForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_examen_form(self):
        form_data = {"nombre": "Primer parcial", "descripcion": ""}
        form = ExamenForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_examen_form_invalido(self):
        form_data = {"nombre": "", "descripcion": ""}
        form = ExamenForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_respuesta_practica_form(self):
        file = mock.MagicMock(spec=File, name='FileMock')
        file.name = 'test1.py'
        form_data = {}
        file_data = {"archivo_respuesta_temporal": file}
        form =  RespuestasPracticasForm(data=form_data, files=file_data)
        self.assertTrue(form.is_valid())

    def test_respuesta_practica_form_invalido(self):
        file = mock.MagicMock(spec=File, name='FileMock')
        file.name = 'test1.png'
        form_data = {}
        file_data = {"archivo_respuesta_temporal": file}
        form = RespuestasPracticasForm(data=form_data, files=file_data)
        self.assertFalse(form.is_valid())

    def test_respuesta_examen_form(self):
        file = mock.MagicMock(spec=File, name='FileMock')
        file.name = 'test1.cpp'
        form_data = {}
        file_data = {"archivo_respuesta_temporal": file}
        form =  RespuestasExamenesForm(data=form_data, files=file_data)
        self.assertTrue(form.is_valid())

    def test_respuesta_examen_form_invalido(self):
        file = mock.MagicMock(spec=File, name='FileMock')
        file.name = 'test1.txt'
        form_data = {}
        file_data = {"archivo_respuesta_temporal": file}
        form = RespuestasExamenesForm(data=form_data, files=file_data)
        self.assertFalse(form.is_valid())


