from django.shortcuts import redirect

def logout_required(fun):
    def interna(request, *args, **kwarg):
        if request.user.is_authenticated:
            return redirect('inicio')
        return fun(request, *args, **kwarg)
    return interna

def login_teacher_required(fun):
    def interna(request, *args, **kwarg):
        if not request.user.is_teacher:
            return redirect('inicio')
        return fun(request, *args, **kwarg)
    return interna

def login_student_required(fun):
    def interna(request, *args, **kwarg):
        if not request.user.is_student:
            return redirect('inicio')
        return fun(request, *args, **kwarg)
    return interna

def redirect_admin(fun):
    def interna(request, *args, **kwarg):
        if request.user.is_superuser:
            return redirect('/admin')
        return fun(request, *args, **kwarg)
    return interna


