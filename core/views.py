from django.shortcuts import render, redirect
from core.util.connection_db_mysql import abrirConexao, fecharConexao


# Create your views here.
def index(request):
    cnx = abrirConexao()
    cursor = None

    if cnx:
        cursor = cnx.cursor(buffered=True, dictionary=True)

        # perfis = {}
        # for (PRF_IdPerfil, PRF_DssPerfil) in cursor:

    try:
        cursor.execute("SELECT * FROM Perfis")

        context = {'perfis': cursor.fetchall()}

        # context = {'usuarios': Usuarios.objects.all(), 'cursos': Cursos.objects.all(), 'perfis': cursor, 'disciplinas_ementas': DisciplinasEmentas.objects.all(), 'planos_ensinos': PlanosEnsinos.objects.all(), 'disciplinas_planos_ensinos': DisciplinasPlanosEnsinos.objects.all(), 'cursos_disciplinas': CursosDisciplinas.objects.all()}


        return render(request, 'index.html', context)

    finally:
        fecharConexao(cursor, cnx)


def cadastro_usuario(request):
    cnx = abrirConexao()
    cursor = None

    if cnx:
        cursor = cnx.cursor(dictionary=True)

    try:
        erros = []
        cursor.execute("SELECT * FROM Perfis")
        context = {'perfis': cursor.fetchall()}

        if request.POST:
            ra = request.POST.get('ra')
            nome = request.POST.get('nome')
            senha = request.POST.get('senha')
            perfil = request.POST.get('perfil')

            if ra.strip() == '':
                erros.append("Ra inválido")
            if nome.strip() == '':
                erros.append("Nome inválido")
            if senha.strip() == '':
                erros.append("Senha inválida")

            if not(erros):
                query = (
                    "INSERT INTO Usuarios(USR_IdRA, USR_DssNome, USR_DssSenha, USR_IdPerfil)VALUES({}, '{}', '{}', {})".format(
                        ra, nome, senha, perfil
                    ))

                cursor.execute(query)

                cnx.commit()
            else:
                context["erros"] = erros
                print("***************** ", context)
                print("***************** ", erros)
    finally:
        fecharConexao(cursor, cnx)

    print("============ ", context)
    return render(request, 'cadastro_usuarios.html', context)


def cadastro_curso(request):
    if request.POST:
        cnx = abrirConexao()
        cursor = None

        if cnx:
            cursor = cnx.cursor()

        try:
            query = ("INSERT INTO Cursos(CUR_DssCurso)VALUES('{}');".format(request.POST.get('curso')))

            cursor.execute(query)

            cnx.commit()
        finally:
            fecharConexao(cursor, cnx)

    return render(request, 'cadastro_cursos.html')


def cadastro_perfis(request):
    if request.POST:
        cnx = abrirConexao()
        cursor = None

        if cnx:
            cursor = cnx.cursor()

        try:
            query = ("INSERT INTO Perfis(PRF_DSSPerfil)VALUES('{}')".format(request.POST.get('perfil')))

            cursor.execute(query)

            cnx.commit()
        finally:
            fecharConexao(cursor, cnx)

    return render(request, 'cadastro_perfis.html')


def cadastro_disciplinas_ementas(request):
    if request.POST:
        cnx = abrirConexao()
        cursor = None

        if cnx:
            cursor = cnx.cursor()

        try:
            query = ("INSERT INTO DisciplinasEmentas(DIS_DssDisciplina, DIS_DssEmenta)VALUES('{}', '{}');".format(
                request.POST.get('disciplina'), request.POST.get('ementa')))

            cursor.execute(query)

            cnx.commit()
        finally:
            fecharConexao(cursor, cnx)

    return render(request, 'cadastro_disciplinas_ementas.html')


def cadastro_planos_ensinos(request):
    if request.POST:
        cnx = abrirConexao()
        cursor = None

        if cnx:
            cursor = cnx.cursor()

        try:
            query = (
                "INSERT INTO PlanosEnsinos(PLE_DssPlanoEnsino)VALUES('{}');".format(request.POST.get('planoEnsino')))

            cursor.execute(query)

            cnx.commit()
        finally:
            fecharConexao(cursor, cnx)

    return render(request, 'cadastro_planos_ensinos.html')


def cadastro_disciplinas_planos_ensinos(request):
    cnx = abrirConexao()
    cursor = None

    if cnx:
        cursor = cnx.cursor(dictionary=True)

    try:
        cursor.execute("SELECT * FROM DisciplinasEmentas")
        context = {'disciplinas': cursor.fetchall()}
        cursor.execute("SELECT * FROM PlanosEnsinos")
        context['planosEnsinos'] = cursor.fetchall()

        if request.POST:
            cursor.execute(
                "INSERT INTO DisciplinasPlanosEnsinos(DPL_IdDisciplina, DPL_IdPlanoEnsino)VALUES({}, {});".format(
                    request.POST.get('disciplina'), request.POST.get('planoEnsino')))
            cnx.commit()
    finally:
        fecharConexao(cursor, cnx)

    return render(request, 'cadastro_disciplinas_planos_ensinos.html', context)


def cadastro_cursos_disciplinas(request):
    cnx = abrirConexao()
    cursor = None

    if cnx:
        cursor = cnx.cursor(dictionary=True)

    try:
        cursor.execute("SELECT * FROM Cursos")
        context = {'cursos': cursor.fetchall()}
        cursor.execute("SELECT * FROM DisciplinasEmentas")
        context['disciplinas'] = cursor.fetchall()

        if request.POST:
            cursor.execute(
                "INSERT INTO CursosDisciplinas(CDS_IdCurso, CDS_IdDisciplina)VALUES({}, {});".format(
                    request.POST.get('curso'), request.POST.get('disciplina')))
            cnx.commit()
    finally:
        fecharConexao(cursor, cnx)

    return render(request, 'cadastro_cursos_disciplinas.html', context)


# Funcionalidades Professor
def opcao_testes_online(request):
    return render(request, "professor/opcao_testes_online.html")


def teste_aberto(request):
    context = {}
    if request.POST:
        cnx = abrirConexao()
        cursor = None

        if cnx:
            cursor = cnx.cursor()

        try:
            erros = []
            resp_questao_1 = request.POST.get('resp1')
            resp_questao_2 = request.POST.get('resp2')
            resp_questao_3 = request.POST.get('resp3')
            resp_questao_4 = request.POST.get('resp4')
            resp_questao_5 = request.POST.get('resp5')
            resp_questao_6 = request.POST.get('resp6')
            resp_questao_7 = request.POST.get('resp7')
            resp_questao_8 = request.POST.get('resp8')
            resp_questao_9 = request.POST.get('resp9')
            resp_questao_10 = request.POST.get('resp10')

            if resp_questao_1.strip() == '' or resp_questao_2.strip() == '' or resp_questao_3.strip() == '' or resp_questao_4.strip() == '' or resp_questao_5.strip() == '' or resp_questao_6.strip() == '' or resp_questao_7.strip() == '' or resp_questao_8.strip() == '' or resp_questao_9.strip() == '' or resp_questao_10.strip() == '':
                erros.append("Respostas Inválidas!")

            if not (erros):
                # enviar email para o professr analizar as respostas !
                pass
            else:
                context['erros'] = erros
        finally:
            fecharConexao(cursor, cnx)

    return render(request, 'professor/teste_aberto.html', context)


def teste_escolha(request):
    return render(request, 'professor/teste_escolha.html')


def teste_v_f(request):
    return render(request, 'professor/teste_v_f.html')
