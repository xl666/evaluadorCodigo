from django.test import TestCase

from evaluador_codigo.routines import *


class EvaluadorRoutinesTest(TestCase):
    fixtures = ["initial_data.json"]

    def test_abrir_archivo_casos_prueba(self):
        ejercicio = Ejercicio.objects.get(nombre="Palabras al revés")
        entradas, salidas = abrir_casos_prueba(ejercicio.casos_prueba.path)
        self.assertEqual(entradas, ['hola mundo cruel\n', 'ella\n', 'ih\n'])
        self.assertEqual(salidas, ['leurc odnum aloh\n', 'alle\n', 'hi\n'])

    def test_obtener_respuesta_anterior_practica(self):
        ejercicio = Ejercicio.objects.get(nombre="Antepasado prolog")
        practica = Practica.objects.get(id=5)
        user = User.objects.get(username="susana14")
        alumno = Alumno.objects.get(user=user)
        ejercicio_practica = EjerciciosPracticas.objects.get(ejercicio=ejercicio, practica=practica)
        res = obtener_respuesta_anterior_practica(ejercicio_practica, alumno)
        self.assertTrue(isinstance(res, RespuestasPracticas))

    def test_obtener_respuesta_anterior_practica_sin_respuesta(self):
        ejercicio = Ejercicio.objects.get(nombre="Antepasado prolog")
        practica = Practica.objects.get(id=5)
        user = User.objects.get(username="carlos")
        alumno = Alumno.objects.get(user=user)
        ejercicio_practica = EjerciciosPracticas.objects.get(ejercicio=ejercicio, practica=practica)
        res = obtener_respuesta_anterior_practica(ejercicio_practica, alumno)
        self.assertEqual(res, False)

    def test_realizar_evaluacion_cpp(self):
        user = User.objects.get(username="susana14")
        alumno = Alumno.objects.get(user=user)
        practica = Practica.objects.get(id=5)
        ejercicio = Ejercicio.objects.get(nombre="Garfield")
        ejercicio_practica = EjerciciosPracticas.objects.get(practica=practica, ejercicio=ejercicio)
        respuesta = RespuestasPracticas.objects.get(ejercicio=ejercicio_practica, alumno=alumno)
        resultado_evaluacion = realizar_evaluacion(respuesta)
        resultado_esperado = [True, True, True, True, True, True]
        self.assertEqual(resultado_evaluacion, resultado_esperado)

    def test_realizar_evaluacion_prolog(self):
        user = User.objects.get(username="susana14")
        alumno = Alumno.objects.get(user=user)
        practica = Practica.objects.get(id=5)
        ejercicio = Ejercicio.objects.get(nombre="Antepasado prolog")
        ejercicio_practica = EjerciciosPracticas.objects.get(practica=practica, ejercicio=ejercicio)
        respuesta = RespuestasPracticas.objects.get(ejercicio=ejercicio_practica, alumno=alumno)
        resultado_evaluacion = realizar_evaluacion(respuesta)
        resultado_esperado = [True, True, True]
        self.assertEqual(resultado_evaluacion, resultado_esperado)

    def test_realizar_evaluacion_java(self):
        user = User.objects.get(username="susana14")
        alumno = Alumno.objects.get(user=user)
        practica = Practica.objects.get(id=5)
        ejercicio = Ejercicio.objects.get(nombre="Palabras al revés")
        ejercicio_practica = EjerciciosPracticas.objects.get(practica=practica, ejercicio=ejercicio)
        respuesta = RespuestasPracticas.objects.get(ejercicio=ejercicio_practica, alumno=alumno)
        resultado_evaluacion = realizar_evaluacion(respuesta)
        resultado_esperado = [True, True, True]
        self.assertEqual(resultado_evaluacion, resultado_esperado)

    def test_realizar_evaluacion_lisp(self):
        user = User.objects.get(username="susana14")
        alumno = Alumno.objects.get(user=user)
        practica = Practica.objects.get(id=5)
        ejercicio = Ejercicio.objects.get(nombre="Longitud lista")
        ejercicio_practica = EjerciciosPracticas.objects.get(practica=practica, ejercicio=ejercicio)
        respuesta = RespuestasPracticas.objects.get(ejercicio=ejercicio_practica, alumno=alumno)
        resultado_evaluacion = realizar_evaluacion(respuesta)
        resultado_esperado = [True, True, True]
        self.assertEqual(resultado_evaluacion, resultado_esperado)

    def test_realizar_evaluacion_python(self):
        user = User.objects.get(username="susana14")
        alumno = Alumno.objects.get(user=user)
        practica = Practica.objects.get(id=5)
        ejercicio = Ejercicio.objects.get(nombre="Bolita")
        ejercicio_practica = EjerciciosPracticas.objects.get(practica=practica, ejercicio=ejercicio)
        respuesta = RespuestasPracticas.objects.get(ejercicio=ejercicio_practica, alumno=alumno)
        resultado_evaluacion = realizar_evaluacion(respuesta)
        resultado_esperado = [True, True]
        self.assertEqual(resultado_evaluacion, resultado_esperado)

    def test_realizar_evaluacion_runtime_error_cpp(self):
        user = User.objects.get(username="carlos")
        alumno = Alumno.objects.get(user=user)
        practica = Practica.objects.get(id=5)
        ejercicio = Ejercicio.objects.get(nombre="Garfield")
        ejercicio_practica = EjerciciosPracticas.objects.get(practica=practica, ejercicio=ejercicio)
        respuesta = RespuestasPracticas.objects.get(ejercicio=ejercicio_practica, alumno=alumno)
        resultado_evaluacion = realizar_evaluacion(respuesta)
        respuesta_esperada = ['Runtime error', 'Runtime error', 'Runtime error', 'Runtime error', 'Runtime error',
                              'Runtime error']
        self.assertEqual(resultado_evaluacion, respuesta_esperada)

    def test_realizar_evaluacion_runtime_error_java(self):
        user = User.objects.get(username="carlos")
        alumno = Alumno.objects.get(user=user)
        practica = Practica.objects.get(id=5)
        ejercicio = Ejercicio.objects.get(nombre="Palabras al revés")
        ejercicio_practica = EjerciciosPracticas.objects.get(practica=practica, ejercicio=ejercicio)
        respuesta = RespuestasPracticas.objects.get(ejercicio=ejercicio_practica, alumno=alumno)
        resultado_evaluacion = realizar_evaluacion(respuesta)
        respuesta_esperada = ['Runtime error', 'Runtime error', 'Runtime error']
        self.assertEqual(resultado_evaluacion, respuesta_esperada)

    def test_realizar_evaluacion_runtime_error_lisp(self):
        user = User.objects.get(username="carlos")
        alumno = Alumno.objects.get(user=user)
        practica = Practica.objects.get(id=5)
        ejercicio = Ejercicio.objects.get(nombre="Longitud lista")
        ejercicio_practica = EjerciciosPracticas.objects.get(practica=practica, ejercicio=ejercicio)
        respuesta = RespuestasPracticas.objects.get(ejercicio=ejercicio_practica, alumno=alumno)
        resultado_evaluacion = realizar_evaluacion(respuesta)
        respuesta_esperada = ['Runtime error', True, 'Runtime error']
        self.assertEqual(resultado_evaluacion, respuesta_esperada)

    def test_realizar_evaluacion_runtime_error_python(self):
        user = User.objects.get(username="carlos")
        alumno = Alumno.objects.get(user=user)
        practica = Practica.objects.get(id=5)
        ejercicio = Ejercicio.objects.get(nombre="Bolita")
        ejercicio_practica = EjerciciosPracticas.objects.get(practica=practica, ejercicio=ejercicio)
        respuesta = RespuestasPracticas.objects.get(ejercicio=ejercicio_practica, alumno=alumno)
        resultado_evaluacion = realizar_evaluacion(respuesta)
        respuesta_esperada = ['Runtime error', 'Runtime error']
        self.assertEqual(resultado_evaluacion, respuesta_esperada)

    def test_realizar_evaluacion_time_exceeded(self):
        user = User.objects.get(username="alan")
        alumno = Alumno.objects.get(user=user)
        practica = Practica.objects.get(id=5)
        ejercicio = Ejercicio.objects.get(nombre="Garfield")
        ejercicio_practica = EjerciciosPracticas.objects.get(practica=practica, ejercicio=ejercicio)
        respuesta = RespuestasPracticas.objects.get(ejercicio=ejercicio_practica, alumno=alumno)
        res = realizar_evaluacion(respuesta)
        respuesta_esperada = ['Time exceeded', 'Time exceeded', 'Time exceeded', 'Time exceeded', 'Time exceeded',
                              'Time exceeded']
        self.assertEqual(res, respuesta_esperada)

    def test_realizar_evaluacion_error_compilacion_cpp(self):
        user = User.objects.get(username="omar")
        alumno = Alumno.objects.get(user=user)
        practica = Practica.objects.get(id=5)
        ejercicio = Ejercicio.objects.get(nombre="Garfield")
        ejercicio_practica = EjerciciosPracticas.objects.get(practica=practica, ejercicio=ejercicio)
        respuesta = RespuestasPracticas.objects.get(ejercicio=ejercicio_practica, alumno=alumno)
        resultado_evaluacion = realizar_evaluacion(respuesta)
        self.assertFalse(resultado_evaluacion)

    def test_realizar_evaluacion_error_compilacion_java(self):
        user = User.objects.get(username="omar")
        alumno = Alumno.objects.get(user=user)
        practica = Practica.objects.get(id=5)
        ejercicio = Ejercicio.objects.get(nombre="Palabras al revés")
        ejercicio_practica = EjerciciosPracticas.objects.get(practica=practica, ejercicio=ejercicio)
        respuesta = RespuestasPracticas.objects.get(ejercicio=ejercicio_practica, alumno=alumno)
        resultado_evaluacion = realizar_evaluacion(respuesta)
        self.assertFalse(resultado_evaluacion)

    def test_realizar_evaluacion_error_compilacion_cpp(self):
        user = User.objects.get(username="omar")
        alumno = Alumno.objects.get(user=user)
        practica = Practica.objects.get(id=5)
        ejercicio = Ejercicio.objects.get(nombre="Longitud lista")
        ejercicio_practica = EjerciciosPracticas.objects.get(practica=practica, ejercicio=ejercicio)
        respuesta = RespuestasPracticas.objects.get(ejercicio=ejercicio_practica, alumno=alumno)
        resultado_evaluacion = realizar_evaluacion(respuesta)
        self.assertFalse(resultado_evaluacion)

    def test_calcular_puntaje_respuesta_correcta(self):
        user = User.objects.get(username="susana14")
        alumno = Alumno.objects.get(user=user)
        practica = Practica.objects.get(id=5)
        ejercicio = Ejercicio.objects.get(nombre="Garfield")
        ejercicio_practica = EjerciciosPracticas.objects.get(practica=practica, ejercicio=ejercicio)
        respuesta = RespuestasPracticas.objects.get(ejercicio=ejercicio_practica, alumno=alumno)
        resultado_evaluacion = realizar_evaluacion(respuesta)
        puntaje_esperado = 10
        resultado, puntaje_obtenido = calcular_puntaje_obtenido_respuesta(resultado_evaluacion, puntaje_esperado)
        self.assertTrue(resultado)
        self.assertEqual(puntaje_obtenido, puntaje_esperado)

    def test_calcular_puntaje_respuesta_runtime_error(self):
        user = User.objects.get(username="carlos")
        alumno = Alumno.objects.get(user=user)
        practica = Practica.objects.get(id=5)
        ejercicio = Ejercicio.objects.get(nombre="Garfield")
        ejercicio_practica = EjerciciosPracticas.objects.get(practica=practica, ejercicio=ejercicio)
        respuesta = RespuestasPracticas.objects.get(ejercicio=ejercicio_practica, alumno=alumno)
        resultado_evaluacion = realizar_evaluacion(respuesta)
        puntaje_esperado = 'Runtime error'
        resultado, puntaje_obtenido = calcular_puntaje_obtenido_respuesta(resultado_evaluacion, puntaje_esperado)
        self.assertFalse(resultado)
        self.assertEqual(puntaje_obtenido, puntaje_esperado)

    def test_calcular_puntaje_respuesta_time_exceeded(self):
        user = User.objects.get(username="alan")
        alumno = Alumno.objects.get(user=user)
        practica = Practica.objects.get(id=5)
        ejercicio = Ejercicio.objects.get(nombre="Garfield")
        ejercicio_practica = EjerciciosPracticas.objects.get(practica=practica, ejercicio=ejercicio)
        respuesta = RespuestasPracticas.objects.get(ejercicio=ejercicio_practica, alumno=alumno)
        resultado_evaluacion = realizar_evaluacion(respuesta)
        puntaje_esperado = 'Time exceeded'
        resultado, puntaje_obtenido = calcular_puntaje_obtenido_respuesta(resultado_evaluacion, puntaje_esperado)
        self.assertTrue(resultado)
        self.assertEqual(puntaje_obtenido, puntaje_esperado)
