"""lms URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from core.views import index, cadastro_usuario, cadastro_curso, cadastro_perfis, cadastro_disciplinas_ementas, cadastro_planos_ensinos, cadastro_disciplinas_planos_ensinos, cadastro_cursos_disciplinas

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', index, name='index'),
    url(r'^cadastro_usuario/$', cadastro_usuario, name='cadastro_usuario'),
    url(r'^cadastro_curso/$', cadastro_curso, name='cadastro_curso'),
    url(r'^cadastro_perfis/$', cadastro_perfis, name='cadastro_perfis'),
    url(r'^cadastro_disciplinas_ementas/$', cadastro_disciplinas_ementas, name='cadastro_disciplinas_ementas'),
    url(r'^cadastro_planos_ensinos/$', cadastro_planos_ensinos, name='cadastro_planos_ensinos'),
    url(r'^cadastro_disciplinas_planos_ensinos/$', cadastro_disciplinas_planos_ensinos, name='cadastro_disciplinas_planos_ensinos'),
    url(r'^cadastro_cursos_disciplinas/$', cadastro_cursos_disciplinas, name='cadastro_cursos_disciplinas'),
]
