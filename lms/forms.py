from django.forms import ModelForm
from lms.models import Usuario



class UserForm(ModelForm):
    class Meta:
        model = Usuario
        fields = ["USR_IdRA", "USR_IdPerfil", "USR_DssSenha"]

