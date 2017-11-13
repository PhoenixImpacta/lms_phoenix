from lms.forms import *
from lms.models import *
from django.shortcuts import render_to_response


def login(request):
        logado = False

        if request.method == 'POST':
                uform = UserForm(request.POST)
                if UserForm.objects.filter(UserForm=[request.POST]):

                        logado = True
        else:
                uform = UserForm()
        usuario = request.POST
        return render_to_response('rango/login.html', {'uform': uform, 'logado': logado, 'usuario': usuario })


def register(request):
        registered = False
        if request.method == 'POST':
                uform = UserForm(request.POST)
                if uform.is_valid():
                        usuario = uform.save()
                        usuario.save()
                        registered = True
                else:
                        print(uform.errors)
        else:
                uform = UserForm()

        return render_to_response('rango/register.html', {'uform': uform, 'registered': registered })



