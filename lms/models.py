from django.db import models
from django.contrib.auth.models import User



class UserProfile(models.Model):
        user = models.OneToOneField(User)


        def __unicode__(self):
                return self.user.username


class Perfil(models.Model):
        perfil = models.CharField(max_length=20)

        def __unicode__(self):
                return self.perfil






