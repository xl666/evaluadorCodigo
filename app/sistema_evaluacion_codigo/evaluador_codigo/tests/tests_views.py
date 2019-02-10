import mock
from django.core.files import File
from django.test import Client
from django.test import TransactionTestCase

from evaluador_codigo.forms import *
from evaluador_codigo.models import EjerciciosExamenes, EjerciciosPracticas, User


class EvaluadorViewsTest(TransactionTestCase):
    fixtures = ["initial_data.json"]  # carga datos iniciales a la bd

    def setUp(self):
        # Every test needs a client.
        self.client = Client()
        self.user_alumno = User.objects.get(username="susana14")
        self.user_academico = User.objects.get(username="xavier")
        """curso 1: paradigmas de programación
            alumno 1: Susana
             práctica 5: Práctica 1 del curso 1
             Examen 7: Segundo parcial del curso 1
             ejercicio e6e2e46b-28da-4648-9fef-ffc015b7db15 practica 5 ejercicio_practica 16
             
        """

    def login_academico(self):
        self.client.login(username='xavier', password='camilo123')

    def login_alumno(self):
        self.client.login(username='susana14', password='camilo123')

    def test_solicitar_registro_academico(self):
        response = self.client.post('/academicos/registro',
                                    {"username": "gerardo", "email": "gerardo@hotmail.com", "name": "Gerardo",
                                     "last_name": "Contreras vega", "licenciaturas": [2], "password": "camilo123",
                                     "conf_password": "camilo123"})
        self.assertEqual(response.status_code, 302)

    def test_solicitar_registro_academico_existente(self):
        response = self.client.post('/academicos/registro',
                                    {"username": "angelsg", "email": "angs@hotmail.com", "name": "Ángel Juan",
                                     "last_name": "Sánchez García", "licenciaturas": [1], "password": "camilo123",
                                     "conf_password": "camilo123"})
        self.assertEqual(response.context["error"], "El usuario ya existe en el sistema")

    def test_solicitar_registro_academico_campos_faltantes(self):
        response = self.client.post('/academicos/registro',
                                    {"username": "", "email": "gerardo@hotmail.com", "name": "Gerardo",
                                     "last_name": "Contreras vega", "licenciaturas": [2], "password": "camilo123",
                                     "conf_password": "camilo123"})

        self.assertEqual(response.context["error"], "Falta uno o más campos")

    def test_solicitar_registro_academico_error_confirmacion_password(self):
        response = self.client.post('/academicos/registro',
                                    {"username": "gerardo", "email": "gerardo@hotmail.com", "name": "Gerardo",
                                     "last_name": "Contreras vega", "licenciaturas": [2], "password": "camilo123",
                                     "conf_password": "camilo"})
        self.assertEqual(response.context["error"], "La contraseña no coincide con su confirmación")

    def test_registrar_alumno(self):
        response = self.client.post('/alumnos/registro',
                                    {"username": "mares", "matricula": "s14011613", "email": "mares@hotmail.com",
                                     "name": "Francisco Gerardo", "last_name": "Mares Solano", "licenciatura": 1,
                                     "password": "camilo123", "conf_password": "camilo123"})

        self.assertEqual(response.status_code, 302)

    def test_registrar_alumno_existente(self):
        response = self.client.post('/alumnos/registro',
                                    {"username": "carlos", "matricula": "s14011642", "email": "carlos@hotmail.com",
                                     "name": "Carlos Erasmo", "last_name": "Torres Sanromán", "licenciatura": 1,
                                     "password": "camilo123", "conf_password": "camilo123"})
        self.assertEqual(response.context["error"], "El usuario ya existe en el sistema")

    def test_registrar_alumno_campos_faltantes(self):
        response = self.client.post('/alumnos/registro',
                                    {"username": "roy", "matricula": "", "email": "roy@hotmail.com", "name": "Rodrigo",
                                     "last_name": "Ruíz Salmorán", "licenciatura": 1, "password": "camilo123",
                                     "conf_password": "camilo123"})
        self.assertEqual(response.context["error"], "Falta uno o más campos")

    def test_registrar_alumno_error_confirmacion_password(self):
        response = self.client.post('/alumnos/registro',
                                    {"username": "roy", "matricula": "s14011633", "email": "roy@hotmail.com",
                                     "name": "Rodrigo", "last_name": "Ruíz Salmorán", "licenciatura": 1,
                                     "password": "camilo", "conf_password": "camilo123"})
        self.assertEqual(response.context["error"], "La contraseña no coincide con su confirmación")

    def test_acceder_crear_curso_como_academico(self):
        self.login_academico()
        response = self.client.get('/cursos/registro')
        self.assertEqual(response.status_code, 200)

    def test_acceder_crear_curso_como_alumno(self):
        self.login_alumno()
        response = self.client.get('/cursos/registro')
        self.assertEqual(response.status_code, 302)

    def test_acceder_crear_curso_como_usuario_anonimo(self):
        response = self.client.get('/cursos/registro')
        self.assertEqual(response.status_code, 302)

    def test_agregar_curso(self):
        self.login_academico()
        response = self.client.post('/cursos/registro',
                                    {"licenciatura": 1, "exp_educativa": 1, "periodo": 1, "nrc": "56722", "bloque": "1",
                                     "seccion": "2", "codigo_inscripcion": "12345", "activo": True})
        self.assertEqual(response.status_code, 302)

    def test_agregar_curso_campos_faltantes(self):
        self.login_academico()
        response = self.client.post('/cursos/registro',
                                    {"licenciatura": "", "exp_educativa": "", "periodo": "", "nrc": "", "bloque": "",
                                     "seccion": "", "codigo_inscripcion": "", "activo": True})
        self.assertFormError(response, 'form', 'licenciatura', 'Este campo es obligatorio.')
        self.assertFormError(response, 'form', 'exp_educativa', 'Este campo es obligatorio.')
        self.assertFormError(response, 'form', 'periodo', 'Este campo es obligatorio.')
        self.assertFormError(response, 'form', 'nrc', 'Este campo es obligatorio.')
        self.assertFormError(response, 'form', 'bloque', 'Este campo es obligatorio.')
        self.assertFormError(response, 'form', 'seccion', 'Este campo es obligatorio.')
        self.assertFormError(response, 'form', 'codigo_inscripcion', 'Este campo es obligatorio.')

    def test_acceder_crear_ejercicio_como_academico(self):
        self.login_academico()
        response = self.client.get('/ejercicios/registro')
        self.assertEqual(response.status_code, 200)

    def test_acceder_crear_ejercicio_como_alumno(self):
        self.login_alumno()
        response = self.client.get('/ejercicios/registro')
        self.assertEqual(response.status_code, 302)

    def test_acceder_crear_ejercicio_como_usuario_anonimo(self):
        response = self.client.get('/ejercicios/registro')
        self.assertEqual(response.status_code, 302)

    def test_agregar_ejercicio(self):
        self.login_academico()
        response = self.client.post('/ejercicios/registro',
                                    {"nombre": "Ejercicio 1", "experiencias_educativas": [1], "temas": [1],
                                     "descripcion": "realizar una suma", "entrada": "dos números enteros",
                                     "salida": "número entero", "ejemplo_entrada": "1 2", "ejemplo_salida": "3",
                                     "publico": True, "entradas[]": ["1", "2", "3"], "salidas[]": ["1", "2", "3"],
                                     "archivo_apoyo": "", })
        self.assertEqual(response.status_code, 302)

    def test_agregar_ejercicio_campos_faltantes(self):
        self.login_academico()
        response = self.client.post('/ejercicios/registro',
                                    {"nombre": "", "experiencias_educativas": [], "temas": [], "descripcion": "",
                                     "entrada": "", "salida": "", "ejemplo_entrada": "", "ejemplo_salida": "",
                                     "publico": True, "entradas[]": ["1", "2", "3"], "salidas[]": ["1", "2", "3"],
                                     "archivo_apoyo": "", })
        self.assertFormError(response, 'form', 'nombre', 'Este campo es obligatorio.')
        self.assertFormError(response, 'form', 'experiencias_educativas', 'Este campo es obligatorio.')
        self.assertFormError(response, 'form', 'temas', 'Este campo es obligatorio.')
        self.assertFormError(response, 'form', 'descripcion', 'Este campo es obligatorio.')
        self.assertFormError(response, 'form', 'ejemplo_entrada', 'Este campo es obligatorio.')
        self.assertFormError(response, 'form', 'ejemplo_salida', 'Este campo es obligatorio.')

    def test_agregar_ejercicio_sin_casos_prueba(self):
        self.login_academico()
        response = self.client.post('/ejercicios/registro',
                                    {"nombre": "Ejercicio 1", "experiencias_educativas": [1], "temas": [1],
                                     "descripcion": "realizar una suma", "entrada": "dos números enteros",
                                     "salida": "número entero", "ejemplo_entrada": "1 2", "ejemplo_salida": "3",
                                     "publico": True, "entradas[]": [], "salidas[]": [], "archivo_apoyo": "", })
        self.assertEqual(response.context["error"],
                         "Debe agregar al menos un caso de prueba con sus entradas y salidas esperadas.")

    def test_acceder_crear_examen_como_academico(self):
        self.login_academico()
        curso = Curso.objects.get(id=1)
        response = self.client.get(curso.get_add_examen_url())
        self.assertEqual(response.status_code, 200)

    def test_acceder_crear_examen_como_alumno(self):
        self.login_alumno()
        curso = Curso.objects.get(id=1)
        response = self.client.get(curso.get_add_examen_url())
        self.assertEqual(response.status_code, 302)

    def test_acceder_crear_examen_como_usuario_anonimo(self):
        curso = Curso.objects.get(id=1)
        response = self.client.get(curso.get_add_examen_url())
        self.assertEqual(response.status_code, 302)

    def test_agregar_examen(self):
        self.login_academico()
        curso = Curso.objects.get(id=1)
        response = self.client.post(curso.get_add_examen_url(), {"nombre": "Segundo parcial", "descripcion": "",
                                                                 "ejercicios[]": [
                                                                     "602f92d0-6ee9-4631-9b1c-54c60a161692"],
                                                                 "puntajes[]": [1]})
        self.assertEqual(response.status_code, 302)

    def test_agregar_examen_campos_faltantes(self):
        self.login_academico()
        curso = Curso.objects.get(id=1)
        response = self.client.post(curso.get_add_examen_url(), {"nombre": "", "descripcion": "", "ejercicios[]": [
            "602f92d0-6ee9-4631-9b1c-54c60a161692"], "puntajes[]": [1]})
        self.assertFormError(response, 'form', 'nombre', 'Este campo es obligatorio.')

    def test_agregar_examen_sin_ejercicios(self):
        self.login_academico()
        curso = Curso.objects.get(id=1)
        response = self.client.post(curso.get_add_examen_url(),
                                    {"nombre": "primer parcial", "descripcion": "", "ejercicios[]": [],
                                     "puntajes[]": []})
        self.assertEqual(response.context["error"], "Es necesario agregar al menos un ejercicio al examen")

    def test_acceder_crear_practica_como_academico(self):
        self.login_academico()
        curso = Curso.objects.get(id=1)
        response = self.client.get(curso.get_add_practica_url())
        self.assertEqual(response.status_code, 200)

    def test_acceder_crear_practica_como_alumno(self):
        self.login_alumno()
        curso = Curso.objects.get(id=1)
        response = self.client.get(curso.get_add_practica_url())
        self.assertEqual(response.status_code, 302)

    def test_acceder_crear_examen_como_usuario_anonimo(self):
        curso = Curso.objects.get(id=1)
        response = self.client.get(curso.get_add_practica_url())
        self.assertEqual(response.status_code, 302)

    def test_agregar_practica(self):
        self.login_academico()
        curso = Curso.objects.get(id=1)
        response = self.client.post(curso.get_add_practica_url(),
                                    {"nombre": "Practica 1", "descripcion": "", "inicio": "2018-09-30 00:13:22",
                                     "termino": "2018-10-30 00:13:22",
                                     "ejercicios[]": ["5ab02d30-d42c-4dfd-b9f3-5bf7d64afe52"], "puntajes[]": [1]})
        self.assertEqual(response.status_code, 302)

    def test_agregar_practica_campos_faltantes(self):
        self.login_academico()
        curso = Curso.objects.get(id=1)
        response = self.client.post(curso.get_add_practica_url(),
                                    {"nombre": "", "descripcion": "", "inicio": "", "termino": "", "ejercicios[]": [],
                                     "puntajes[]": []})
        self.assertFormError(response, 'form', 'nombre', 'Este campo es obligatorio.')
        self.assertFormError(response, 'form', 'inicio', 'Este campo es obligatorio.')
        self.assertFormError(response, 'form', 'termino', 'Este campo es obligatorio.')

    def test_agregar_practica_sin_ejercicios(self):
        self.login_academico()
        curso = Curso.objects.get(id=1)
        response = self.client.post(curso.get_add_practica_url(),
                                    {"nombre": "Practica 1", "descripcion": "", "inicio": "2018-09-30 00:13:22",
                                     "termino": "2018-10-30 00:13:22", "ejercicios[]": [], "puntajes[]": []})
        self.assertEqual(response.context["error"], "Es necesario agregar al menos un ejercicio a la práctica")

    def test_editar_practica(self):
        self.login_academico()
        curso = Curso.objects.get(id=1)

        response = self.client.post(curso.get_add_practica_url(),
                                    {"nombre": "Practica 1", "descripcion": "", "inicio": "2018-09-30 00:13:22",
                                     "termino": "2018-10-30 00:13:22",
                                     "ejercicios[]": ["5ab02d30-d42c-4dfd-b9f3-5bf7d64afe52"], "puntajes[]": [1]})
        self.assertEqual(response.status_code, 302)

    def test_resolver_ejercicio_examen(self):
        self.login_alumno()
        file = mock.MagicMock(spec=File, name='FileMock')
        file.name = 'test1.cpp'
        file_data = {"archivo_respuesta_temporal": file}
        ejercicio = EjerciciosExamenes.objects.get(pk=9)
        response = self.client.post(ejercicio.get_ejercicio_url(), file_data)
        self.assertEqual(response.context["error"], "Error de compilación")

    def test_resolver_ejercicio_examen(self):
        self.login_alumno()
        file = mock.MagicMock(spec=File, name='FileMock')
        file.name = 'test1.cpp'
        file_data = {"archivo_respuesta_temporal": file}
        ejercicio = EjerciciosExamenes.objects.get(pk=3)
        response = self.client.post(ejercicio.get_ejercicio_url(), file_data)
        self.assertEqual(response.context["error"], "El examen ha concluido")

    def test_resolver_ejercicio_examen_archivo_invalido(self):
        self.login_alumno()
        file = mock.MagicMock(spec=File, name='FileMock')
        file.name = 'test1.txt'
        file_data = {"archivo_respuesta_temporal": file}
        ejercicio = EjerciciosExamenes.objects.get(id=9)
        response = self.client.post(ejercicio.get_ejercicio_url(), file_data)
        self.assertFormError(response, 'form', 'archivo_respuesta_temporal',
                             "La extensión de archivo 'txt' no está permitida. Únicamente se permiten: 'py, java, prolog, cpp, c, lisp, zip'.")

    def test_resolver_ejercicio_examen_sin_archivo(self):
        self.login_alumno()
        file_data = {"archivo_respuesta_temporal": ""}
        ejercicio = EjerciciosExamenes.objects.get(id=9)
        response = self.client.post(ejercicio.get_ejercicio_url(), file_data)
        self.assertFormError(response, 'form', 'archivo_respuesta_temporal', "Este campo es obligatorio.")

    def test_resolver_ejercicio_practica(self):
        self.login_alumno()
        file = mock.MagicMock(spec=File, name='FileMock')
        file.name = 'test1.cpp'
        file_data = {"archivo_respuesta_temporal": file}
        ejercicio = EjerciciosPracticas.objects.get(id=9)
        response = self.client.post(ejercicio.get_ejercicio_url(), file_data)
        self.assertEqual(response.context["error"], "Error de compilación")

    def test_resolver_ejercicio_practica_archivo_invalido(self):
        self.login_alumno()
        file = mock.MagicMock(spec=File, name='FileMock')
        file.name = 'test1.txt'
        file_data = {"archivo_respuesta_temporal": file}
        ejercicio = EjerciciosPracticas.objects.get(id=9)
        response = self.client.post(ejercicio.get_ejercicio_url(), file_data)
        self.assertFormError(response, 'form', 'archivo_respuesta_temporal',
                             "La extensión de archivo 'txt' no está permitida. Únicamente se permiten: 'py, java, prolog, cpp, c, lisp, zip'.")

    def test_resolver_ejercicio_practica_sin_archivo(self):
        self.login_alumno()
        file_data = {"archivo_respuesta_temporal": ""}
        ejercicio = EjerciciosPracticas.objects.get(id=9)
        response = self.client.post(ejercicio.get_ejercicio_url(), file_data)
        self.assertFormError(response, 'form', 'archivo_respuesta_temporal', "Este campo es obligatorio.")
