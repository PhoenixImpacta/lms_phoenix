from django.contrib.auth.models import User
from lms.models import UserProfile
from lms.forms import UserForm, PerfilForm
from django.http import HttpResponse
from django.shortcuts import render_to_response, RequestContext


def register(request):
        context = RequestContext(request)
        registered = False
        if request.method == 'POST':
                uform = UserForm(data = request.POST)
                pform = PerfilForm(data = request.POST)
                if uform.is_valid() and pform.is_valid():
                        user = uform.save()
                        # form brings back a plain text string, not an encrypted password
                        pw = user.password
                        # thus we need to use set password to encrypt the password string
                        user.set_password(pw)
                        user.save()
                        profile = pform.save(commit = False)
                        profile.user = user
                        profile.save()
                        registered = True
                else:
                        print (uform.errors, pform.errors)
        else:
                uform = UserForm()
                pform = PerfilForm()

        return render_to_response('rango/register.html', {'uform': uform, 'pform': pform, 'registered': registered }, context)



