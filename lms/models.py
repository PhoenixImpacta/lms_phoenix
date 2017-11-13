from django.db import models
from django.contrib.auth.models import User




class Perfis(models.Model):
        PRF_IdPerfil = models.IntegerField(primary_key=True)
        PRF_DSSPerfil = models.CharField(max_length=15, null=False)

        def __unicode__(self):
                return self.PRF_IdPerfil

class Usuario(models.Model):
        USR_IdRA = models.IntegerField(primary_key=True)
        USR_DssNome = models.CharField(max_length=70, null=False)
        USR_DssSenha = models.CharField(max_length=12, null=False)
        USR_IdPerfil = models.ForeignKey(Perfis)

        def __unicode__(self):
                return self.USR_IdPerfil, self.USR_DssSenha, self.USR_IdRA




class UserProfile(models.Model):
        user = models.OneToOneField(User)


        def __unicode__(self):
                return self.user.username









