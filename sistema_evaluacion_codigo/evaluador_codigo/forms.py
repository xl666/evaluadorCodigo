from bootstrap_datepicker_plus.widgets import DateTimePickerInput
from django import forms
from django.core.validators import FileExtensionValidator
from django.forms import ModelForm

from .models import Academico, Alumno, Curso, Ejercicio, Examen, Licenciatura, Practica, RespuestasExamenes, \
    RespuestasPracticas, User


class UserForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['email'].required = True
        self.fields['username'].label = "Nombre de usuario"
        self.fields['first_name'].label = "Nombre"
        self.fields['last_name'].label = "Apellidos"
        self.fields['email'].label = "Correo electrónico"
        self.fields['img_profile'].label = "Imagen de perfil"
        self.fields[
            'username'].help_text = "Requerido. 150 carácteres como máximo. Únicamente letras, dígitos y @/./+/-/_"

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "img_profile", ]
        widgets = {'first_name': forms.TextInput(attrs={'required': True}),
                   'last_name':  forms.TextInput(attrs={'required': True}),
                   'email':      forms.TextInput(attrs={'required': True}), }


class AcademicoForm(ModelForm):
    class Meta:
        model = Academico
        fields = ["licenciaturas", ]


class AlumnoForm(ModelForm):
    class Meta:
        model = Alumno
        fields = ["matricula", "licenciatura", ]


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['email'].required = True
        self.fields['username'].label = "Nombre de usuario"
        self.fields['first_name'].label = "Nombre"
        self.fields['last_name'].label = "Apellidos"
        self.fields['email'].label = "Correo electrónico"
        self.fields[
            'username'].help_text = "Requerido. 150 carácteres como máximo. Únicamente letras, dígitos y @/./+/-/_"

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "password"]

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        user.is_active = False
        if commit:
            user.save()
        return user


class CursoForm(ModelForm):
    def __init__(self, academico, *args, **kwargs):
        super(CursoForm, self).__init__(*args, **kwargs)
        self.fields['licenciatura'].queryset = academico.licenciaturas.all()
        self.fields[
            'codigo_inscripcion'].help_text = "Código para que los alumnos puedan inscribirse al curso."

    class Meta:
        model = Curso
        fields = ["licenciatura", "exp_educativa", "periodo", "nrc", "bloque", "seccion", "codigo_inscripcion",
                  "activo"]


class LicenciaturaForm(ModelForm):
    class Meta:
        model = Licenciatura
        fields = ["licenciatura", ]


class EjercicioForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(EjercicioForm, self).__init__(*args, **kwargs)
        self.fields['entrada'].required = False
        self.fields['salida'].required = False
        self.fields['archivo_apoyo'].required = False
        self.fields['temas'].required = True
        self.fields['experiencias_educativas'].required = True
        self.fields[
            'temas'].help_text = "Presione ctrl para seleccionar más de un tema. Si el tema no está registrado, " \
                                 "puede agregarlo."
        self.fields[
            'experiencias_educativas'].help_text = "Presione ctrl para seleccionar más de una experiencia educativa."
        self.fields['entrada'].label = "Descripción de la entrada"
        self.fields['salida'].label = "Descripción de la salida"
        self.fields['experiencias_educativas'].label = "Experiencias educativas relacionadas"
        self.fields['temas'].label = "Temas relacionados"
        # self.fields['archivo_apoyo'].help_text ="Únicamente se permiten: 'py, java, prolog, cpp, lisp, zip'."

    class Meta:
        model = Ejercicio
        fields = ["nombre", "experiencias_educativas", "temas", "descripcion", "entrada", "salida", "ejemplo_entrada",
                  "ejemplo_salida", "archivo_apoyo", "publico"]


class PracticaForm(ModelForm):
    class Meta:
        model = Practica
        fields = ["nombre", "inicio", "termino", "descripcion"]
        widgets = {  # Use localization and bootstrap 3
            'inicio':  DateTimePickerInput(format='YYYY-MM-DD HH:mm:ss', attrs={'placeholder': 'YYYY-MM-DD hh:mm:ss'}),
            'termino': DateTimePickerInput(format='YYYY-MM-DD HH:mm:ss', attrs={'placeholder': 'YYYY-MM-DD hh:mm:ss'})

            }


class ExamenForm(ModelForm):
    class Meta:
        model = Examen
        fields = ["nombre", "descripcion"]


class RespuestasPracticasForm(ModelForm):
    message = ("La extensión de archivo '%(extension)s' no está permitida. "
               "Únicamente se permiten: '%(allowed_extensions)s'.")
    archivo_respuesta_temporal = forms.FileField(validators=[
        FileExtensionValidator(allowed_extensions=['py', 'java', 'prolog', 'cpp', 'c', 'lisp', 'zip'],
                               message=message)])

    def __init__(self, *args, **kwargs):
        super(RespuestasPracticasForm, self).__init__(*args, **kwargs)
        self.fields['archivo_respuesta_temporal'].label = "Respuesta del estudiante"
        self.fields['archivo_respuesta_temporal'].required = True

    class Meta:
        model = RespuestasPracticas
        fields = ["archivo_respuesta_temporal"]


class RespuestasExamenesForm(ModelForm):
    message = ("La extensión de archivo '%(extension)s' no está permitida. "
               "Únicamente se permiten: '%(allowed_extensions)s'.")
    archivo_respuesta_temporal = forms.FileField(validators=[
        FileExtensionValidator(allowed_extensions=['py', 'java', 'prolog', 'cpp', 'c', 'lisp', 'zip'],
                               message=message)])

    def __init__(self, *args, **kwargs):
        super(RespuestasExamenesForm, self).__init__(*args, **kwargs)
        self.fields['archivo_respuesta_temporal'].label = "Respuesta del estudiante"
        self.fields['archivo_respuesta_temporal'].required = True

    class Meta:
        model = RespuestasExamenes
        fields = ["archivo_respuesta_temporal"]
