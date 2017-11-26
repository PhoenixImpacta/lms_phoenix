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
from core.views import *

urlpatterns = [
    #url(r'^admin/', admin.site.urls),
    url(r'^index/$', index, name='index'),
    url(r'^$', login, name='login'),
    #url(r'^cadastro_usuario/$', cadastro_usuario, name='cadastro_usuario'),
    url(r'^cadastro_curso/$', cadastro_curso, name='cadastro_curso'),
    #url(r'^cadastro_disciplinas_ementas/$', cadastro_disciplinas_ementas, name='cadastro_disciplinas_ementas'),
    #url(r'^cadastro_planos_ensinos/$', cadastro_planos_ensinos, name='cadastro_planos_ensinos'),
    #url(r'^cadastro_disciplinas_planos_ensinos/$', cadastro_disciplinas_planos_ensinos, name='cadastro_disciplinas_planos_ensinos'),
    #url(r'^cadastro_cursos_disciplinas/$', cadastro_cursos_disciplinas, name='cadastro_cursos_disciplinas'),
    url(r'^opcao_testes_online/$', opcao_testes_online, name='opcao_testes_online'),
    url(r'^opcao_testes_online/teste_aberto/$', teste_aberto, name='teste_aberto'),
    url(r'^opcao_testes_online/teste_v_f/$', teste_v_f, name='teste_v_f'),
    url(r'^avisos/$', enviar_avisos, name='avisos'),
    url(r'^novas_atividades/$', enviar_aviso_nova_atividade, name='novas_atividades'),
    url(r'^admin/$', cadastro_perfis, name='cadastro_perfis'),
    url(r'^disciplina/$', cadastro_curso_turma, name='cadastro_curso_turma'),
    url(r'^cadastro_curso/$', cadastro_curso, name='cadastro_curso'),
]
