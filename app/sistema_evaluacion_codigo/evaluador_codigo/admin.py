from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext as _

from .models import *


class LicenciaturaAdmin(admin.ModelAdmin):
    list_display = ("licenciatura",)


class PeriodoAdmin(admin.ModelAdmin):
    list_display = ("periodo",)
    paginate_by = 15


class ExperienciaEducativaAdmin(admin.ModelAdmin):
    list_display = ("exp_educativa",)
    ordering = ("exp_educativa",)
    paginate_by = 15


class AcademicoAdmin(admin.ModelAdmin):
    list_display = ("user",)
    search_fields = ("user",)
    paginate_by = 15
    filter_horizontal = ('licenciaturas',)


class AlumnoAdmin(admin.ModelAdmin):
    list_display = ("user",)
    paginate_by = 15


class CursoAdmin(admin.ModelAdmin):
    list_display = ("nrc", "exp_educativa", "periodo", "bloque", "seccion")
    list_filter = ("exp_educativa",)
    paginate_by = 15


class EjercicioAdmin(admin.ModelAdmin):
    list_display = ("nombre", "descripcion",)
    list_filter = ("experiencias_educativas", "temas",)
    search_fields = ("nombre",)
    paginate_by = 15


class PracticaAdmin(admin.ModelAdmin):
    list_display = ("nombre", "descripcion",)
    list_filter = ("nombre",)
    search_fields = ("nombre",)
    paginate_by = 15


class UserAdmin(BaseUserAdmin):
    list_display = ("username",)
    paginate_by = 15
    list_filter = ("is_active", 'is_student', 'is_teacher',)
    search_fields = ('first_name', 'last_name', 'email', "is_active", 'is_student', 'is_teacher',)
    # add_form = UserCreationForm
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'is_student', 'is_teacher',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
        )
    add_fieldsets = (
        (None, {'fields': ('username', 'password1', 'password2')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'is_student', 'is_teacher',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
        )


class TemaAdmin(admin.ModelAdmin):
    list_display = ("tema",)
    paginate_by = 15


class RespuestasPracticasAdmin(admin.ModelAdmin):
    list_display = ("alumno", "ejercicio", "fecha_enviado")
    list_filter = ("ejercicio",)
    search_fields = ("practica", "alumno", "ejercicio")
    paginate_by = 15


class ExamenAdmin(admin.ModelAdmin):
    list_display = ("nombre", "descripcion", "estado")


admin.site.register(Licenciatura, LicenciaturaAdmin)
admin.site.register(Periodo, PeriodoAdmin)
admin.site.register(ExperienciaEducativa, ExperienciaEducativaAdmin)
admin.site.register(Academico, AcademicoAdmin)
admin.site.register(Alumno, AlumnoAdmin)
admin.site.register(Curso, CursoAdmin)
admin.site.register(Ejercicio, EjercicioAdmin)
# admin.site.register(RespuestasPracticas, RespuestasPracticasAdmin)
admin.site.register(Practica, PracticaAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Tema, TemaAdmin)
admin.site.register(Examen, ExamenAdmin)
