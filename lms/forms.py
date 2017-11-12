from django.forms import ModelForm
from lms.models import Perfil
from django.contrib.auth.models import User

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ["username", "email", "password"]


class PerfilForm(ModelForm):
    class Meta:
        model = Perfil
        fields = ['perfil']