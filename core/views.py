from django.shortcuts import render, redirect
from core.util.connection_db_mysql import abrirConexao, fecharConexao


# Create your views here.
def index(request):
    cursor = None
    cnx = abrirConexao()

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


def login(request):
    cnx = abrirConexao()
    cursor = None

    if cnx:
        cursor = cnx.cursor(dictionary=True)

    try:
        erros = []
        cursor.execute("SELECT * FROM Usuarios")
        context = {'usuarios': cursor.fetchall()}

        if request.POST:
            ra = request.POST.get('ra')
            senha = request.POST.get('senha')

            if ra.strip() == '':
                erros.append("Ra inválido")
            if senha.strip() == '':
                erros.append("Senha inválida")

            if not(erros):
                cursor.execute("select * from Usuarios where USR_IdRa={} and USR_DssSenha ={}".format(ra, senha))
                usuario = cursor.fetchall()

                if not(usuario):
                    erros.append("Usuário não existe")
                    context["erros"] = erros
                else:
                    print("==============================================Entrei")
                    # Salvar Sessão

            else:
                context["erros"] = erros
                print("***************** ", context)
                print("***************** ", erros)
    finally:
        fecharConexao(cursor, cnx)

    print("============ ", context)
    return render(request, 'login.html', context)


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

            if not (erros):
                query = (
                    "INSERT INTO Usuarios(USR_IdRA, USR_DssNome, USR_DssSenha, USR_IdPerfil)VALUES({}, '{}', '{}', {})".format(
                        ra, nome, senha, perfil
                    ))

                cursor.execute(query)

                cnx.commit()
            else:
                context["erros"] = erros
    finally:
        fecharConexao(cursor, cnx)

    return render(request, 'cadastro_usuarios.html', context)


def cadastro_curso(request):
    context = {}
    if request.POST:
        cnx = abrirConexao()
        cursor = None

        if cnx:
            cursor = cnx.cursor()

        try:
            erros = []
            curso = request.POST.get("curso")

            if curso.strip() == '':
                erros.append("Curso inválido!")

            if not (erros):
                query = ("INSERT INTO Cursos(CUR_DssCurso)VALUES('{}');".format(curso))

                cursor.execute(query)

                cnx.commit()
            else:
                context["erros"] = erros
        finally:
            fecharConexao(cursor, cnx)

    return render(request, 'cadastro_cursos.html', context)


def cadastro_disciplinas_ementas(request):
    context = {}
    if request.POST:
        cnx = abrirConexao()
        cursor = None

        if cnx:
            cursor = cnx.cursor()

        try:
            erros = []

            disciplina = request.POST.get('disciplina')
            ementa = request.POST.get('ementa')

            if disciplina.strip() == '':
                erros.append("Disciplina inválida!")

            if ementa.strip() == '':
                erros.append("Ementa inválida!")

            if not (erros):
                query = ("INSERT INTO DisciplinasEmentas(DIS_DssDisciplina, DIS_DssEmenta)VALUES('{}', '{}');".format(
                    disciplina, ementa))

                cursor.execute(query)

                cnx.commit()
            else:
                context["erros"] = erros
        finally:
            fecharConexao(cursor, cnx)

    return render(request, 'cadastro_disciplinas_ementas.html')


def cadastro_planos_ensinos(request):
    context = {}
    if request.POST:
        cnx = abrirConexao()
        cursor = None

        if cnx:
            cursor = cnx.cursor()

        try:
            erros = []
            planoEnsino = request.POST.get('planoEnsino')

            if planoEnsino.strip() == '':
                erros.append("Plano Ensino inválido!")

            if not (erros):

                query = (
                    "INSERT INTO PlanosEnsinos(PLE_DssPlanoEnsino)VALUES('{}');".format(planoEnsino))

                cursor.execute(query)

                cnx.commit()
            else:
                context["erros"] = erros
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
    cnx = abrirConexao()
    cursor = None
    context = {}

    if cnx:
        cursor = cnx.cursor()

    if request.POST:
        try:
            resp1: request.POST.get("resp1")
            resp2: request.POST.get("resp2")
            resp3: request.POST.get("resp3")
            resp4: request.POST.get("resp4")
            resp5: request.POST.get("resp5")
            resp6: request.POST.get("resp6")
            resp7: request.POST.get("resp7")
            resp8: request.POST.get("resp8")
            resp9: request.POST.get("resp9")
            resp10: request.POST.get("resp10")

            query = ("INSERT INTO Questoes VALUES('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}');")

        finally:
            fecharConexao(cursor, cnx)




    return render(request, 'professor/teste_escolha.html')


def teste_v_f(request):
    return render(request, 'professor/teste_v_f.html')
