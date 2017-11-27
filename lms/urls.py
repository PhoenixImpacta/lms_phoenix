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
from core.views import login, upload_foto, index, visualizar_avisos_professor, enviar_aviso_para_professor, \
    aviso_professor, \
    visualizar_avisos, perfil_aluno, opcao_testes_online, teste_aberto, teste_escolha, teste_v_f, \
    enviar_avisos, enviar_aviso_nova_atividade, cadastrar_questoes, enviar_aviso_para_aluno, aviso_aluno, \
    abrir_matricula, matricular, confirmar_matricula, logout, cadastro_perfis, cadastro_curso_turma, cadastro_curso, \
    cadastro_disciplina, editar_disciplina, deleta_disciplina, lista_disciplina, lista_curso, deleta_curso

urlpatterns = [
    url(r'^index/$', index, name='index'),
    url(r'^$', login, name='login'),
    url(r'^opcao_testes_online/$', opcao_testes_online, name='opcao_testes_online'),
    url(r'^opcao_testes_online/teste_aberto/$', teste_aberto, name='teste_aberto'),
    url(r'^opcao_testes_online/teste_escolha/$', teste_escolha, name='teste_escolha'),
    url(r'^opcao_testes_online/teste_v_f/$', teste_v_f, name='teste_v_f'),
    url(r'^avisos/$', enviar_avisos, name='avisos'),
    url(r'^nova_questao/$', cadastrar_questoes, name='nova_questao'),
    url(r'^novas_atividades/$', enviar_aviso_nova_atividade, name='novas_atividades'),
    url(r'^avisos_aluno/$', enviar_aviso_para_aluno, name='avisos_aluno'),
    url(r'^avisos_aluno/aluno/(?P<ra_aluno>\d+)$', aviso_aluno, name='aviso_aluno'),
    url(r'^visualizar_avisos$', visualizar_avisos, name='visualizar_avisos'),
    url(r'^visualizar_avisos/professor/$', visualizar_avisos_professor, name='visualizar_avisos_professor'),
    url(r'^avisos_professor/$', enviar_aviso_para_professor, name='avisos_professor'),
    url(r'^avisos_professor/professor/(?P<ra_professor>\d+)$', aviso_professor, name='aviso_professor'),
    url(r'^upload_foto/$', upload_foto, name='upload_foto'),
    url(r'^perfil_aluno/$', perfil_aluno, name='perfil_aluno'),
    url(r'^abrir_matricula/$', abrir_matricula, name='abrir_matricula'),
    url(r'^confirmar_matricula/$', confirmar_matricula, name='confirmar_matricula'),
    url(r'^matricular/$', matricular, name='matricular'),
    url(r'^logout/$', logout, name='logout'),
    url(r'^admin/$', cadastro_perfis, name='cadastro_perfis'),
    url(r'^curso/turma/$', cadastro_curso_turma, name='cadastro_curso_turma'),
    url(r'^cadastro/curso/$', cadastro_curso, name='cadastro_curso'),
    url(r'^cadastro/disciplina/$', cadastro_disciplina, name='cadastro_disciplina'),
    url(r'^editar/disciplina/$', editar_disciplina, name='editar_disciplina'),
    url(r'^deleta/disciplina/$', deleta_disciplina, name='deleta_disciplina'),
    url(r'^lista/disciplina/$', lista_disciplina, name='lista_disciplina'),
    url(r'^lista/curso/$', lista_curso, name='lista_curso'),
    url(r'^deleta/curso/$', deleta_curso, name='deleta_curso'),
]
