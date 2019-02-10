import os
from django.core.exceptions import ValidationError

def validar_extension_archivo_fuente(value):
    ext = os.path.splitext(value.name)[1]
    print(ext)
    valid_extensions = ['.py', '.java', '.prolog', '.cpp','.lisp','.zip']
    if not ext in valid_extensions:
        raise ValidationError(u'Porfavor sube un archivo con formato válido')
