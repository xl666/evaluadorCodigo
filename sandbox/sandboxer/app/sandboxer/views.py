from django.shortcuts import render_to_response
from sandboxer import settings

def index(request):
    return render_to_response('index.html', {'urlEvaluador': settings.EVALUADOR_URL})
