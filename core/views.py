from django.shortcuts import render, redirect, render_to_response
from core.util.connection_db_mysql import abrirConexao, fecharConexao
from core.util.EnviarEmail import enviarEmail
import datetime


# Create your views here.
def index(request):
    cursor = None
    cnx = abrirConexao()
    usuario_logado = request.COOKIES['usuario_logado']
    print("==========", usuario_logado)
    context = {'usuario_logado': request.COOKIES['usuario_logado']}
    if cnx:
        cursor = cnx.cursor(buffered=True, dictionary=True)

    try:

        return render(request, 'index.html', context)

    finally:
        fecharConexao(cursor, cnx)


def login(request):
    cnx = abrirConexao()
    cursor = None
    context = {}





    if cnx:
        cursor = cnx.cursor(dictionary=True)

    try:
        erros = []

        if request.POST:

            ra = request.POST.get('ra')
            tipo = request.POST.get('tipo')
            print("--------", tipo)
            if ra.strip() == '':
                erros.append("Ra inválido")

            if not (erros):

                usuario = None
                if tipo == 'a':
                    cursor.execute("select * from Aluno where ra={}".format(ra))
                    usuario = cursor.fetchall()


                elif tipo == 'c':
                    cursor.execute("select * from Coordenador where ra={}".format(ra))
                    usuario = cursor.fetchall()



                elif tipo == 'p':
                    cursor.execute("select * from Professor where ra={}".format(ra))
                    usuario = cursor.fetchall()





                if not (usuario):
                    erros.append("Usuário não existe")
                    context["erros"] = erros
                else:
                    resposta = render_to_response("index.html", context)
                    max_age = 365 * 24 * 60 * 60  # one year
                    expires = datetime.datetime.strftime(
                        datetime.datetime.utcnow() + datetime.timedelta(seconds=max_age), "%a, %d-%b-%Y %H:%M:%S GMT")
                    resposta.set_cookie("usuario_logado", usuario, max_age=max_age, expires=expires, domain=None,
                                        secure=False)
                    return resposta

            else:
                context["erros"] = erros
    finally:
        fecharConexao(cursor, cnx)

    return render(request, 'login.html', context)


def enviar_avisos(request):
    cnx = abrirConexao()
    cursor = None
    context = {}

    usuario_logado = request.COOKIES['usuario_logado']

    if usuario_logado:
        context = {'usuario_logado': usuario_logado}

    if cnx:
        cursor = cnx.cursor()
    try:

        if request.POST:
            erros = []
            aviso = request.POST.get('aviso')
            para = request.POST.get('para')

            if aviso.strip() == '':
                erros.append("Aviso inválido")

            if not (erros):
                if para == 'alunos':
                    cursor.execute("SELECT email FROM Aluno;")
                    email = cursor.fetchall()
                    enviarEmail(email, aviso)
                elif para == 'professores':
                    cursor.execute("select email from Professor;")
                    email = cursor.fetchall()
                    enviarEmail(email, aviso)

                    # Inserir histórico
                    # cursor.execute("insert into HistoricoAvisos values({}, {}, {});".format(aviso, datetime.date, usuario_logado['ra']))
    finally:
        fecharConexao(cursor, cnx)

    return render(request, 'avisos.html', context)


def enviar_aviso_nova_atividade(request):
    cnx = abrirConexao()
    cursor = None

    try:
        if cnx:
            cursor = cnx.cursor(dictionary=True)

        usuario_logado = request.COOKIES['usuario_logado']
        context = {'usuario_logado': usuario_logado}
        cursor.execute('select nome_disciplina from Turma where ra_professor = 2000;')
        disciplinas = cursor.fetchall()
        context['disciplinas'] = disciplinas

    finally:
        fecharConexao(cursor, cnx)



    return render(request, 'professor/cadastro_questoes.html', context)

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

'''
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

            query = (
                "INSERT INTO Questoes VALUES('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}');".format(resp1, resp2,
                                                                                                         resp3, resp4,
                                                                                                         resp5, resp6,
                                                                                                         resp7, resp8,
                                                                                                         resp9, resp10))
            cursor.execute(query)
            cnx.commit()

        finally:
            fecharConexao(cursor, cnx)

    return render(request, 'professor/teste_escolha.html')

'''
def teste_v_f(request):
    return render(request, 'professor/teste_v_f.html')


# 7486354
'''
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

'''
# Funcionalidades Professor


def cadastro_perfis(request):
    context = {}
    if request.POST:
        cnx = abrirConexao()
        cursor = None

        if cnx:
            cursor = cnx.cursor()

        try:
            erros = []
            nome = request.POST.get("nome")
            ra = request.POST.get("ra")
            email = request.POST.get("email")

            if nome.strip() == '' or ra.strip() == '':
                erros.append("Perfil inválido!")

            if not (erros):
                query = ("INSERT INTO Coordenador(nome, ra, email)VALUES('{}','{}','{}');".format(nome, ra, email))

                cursor.execute(query)

                cnx.commit()
            else:
                context["erros"] = erros
        finally:
            fecharConexao(cursor, cnx)

    return render(request, 'admin/admin.html', context)

'''CADASTRO DE CURSOS E DISCIPLINAS POR TURMA'''

def cadastro_curso_turma(request):
    cnx = abrirConexao()
    cursor = None


    if cnx:
        cursor = cnx.cursor(dictionary=True)


    try:
        erros = []
        mensagem = []
        cursor.execute("select * from Curso")
        cursos = cursor.fetchall()

        cursor.execute("select * from CursoTurma")
        CT = cursor.fetchall()

        cursor.execute("select * from Turma")
        turma = cursor.fetchall()

        cursor.execute("select * from GradeCurricular")
        grade = cursor.fetchall()

        cursor.execute("select * from Disciplina")
        dis = cursor.fetchall()

        cursor.execute("select nome from Disciplina")
        nome_dis = cursor.fetchall()

        context={'cursos': cursos, 'CT': CT, 'turma': turma, 'grade': grade, 'dis': dis}


        if request.POST:
            disciplina = request.POST.get('disciplina')
            curso = request.POST.get('curso')
            id_turma = request.POST.get('idTurma')
            ano = request.POST.get("ano")
            semestre = request.POST.get("semestre")


            if not (erros):

                '''BUSCA A SIGLA DO CURSO SELECIONADO'''

                cursor.execute("select sigla from Curso where nome = '{}'".format(curso))
                sigla = cursor.fetchall()

                s = sigla[0]
                sig = s['sigla']
                lista = {'sigla_curso': sig, 'nome_disciplina': disciplina, 'ano_ofertado': ano, 'semestre_ofertado': semestre, 'id_turma': id_turma}

                print(lista, '======', CT[0])
                verifica = []
                for i in range(0, len(CT)):
                    CR = CT[i]
                    print(CR)
                    print(lista)
                    for n in range(0, len(lista)):
                        ver = (lista.get('sigla_curso') == CR.get('sigla_curso')and lista.get('nome_disciplina') == CR.get('nome_disciplina')and int(lista.get('id_turma')) == int(CR.get('id_turma')) and int(lista.get('ano_ofertado')) == int(CR.get('ano_ofertado'))and int(lista.get('semestre_ofertado')) == int(CR.get('semestre_ofertado')))
                        verifica.append(ver)
                        print(verifica)


                '''INSERE NA TABELA CURSOTURMA OS VALORES SELECIONADOS'''
                if True in verifica:
                    mensagem.append("Já cadastrado")
                    context['mensagem'] = mensagem

                else:
                    cursoTurma = cursor.execute("insert into CursoTurma(sigla_curso, nome_disciplina, id_turma, ano_ofertado, semestre_ofertado) values('{}', '{}', {}, {}, {})".format(sig, disciplina, id_turma, ano, semestre))
                    cursor.execute(cursoTurma)
                    cnx.commit()

                    mensagem.append("Cadastrado com sucesso")
                    context['mensagem'] = mensagem




            else:
                erros.append("Seleção invalida")
                context["erros"] = erros
    finally:
        fecharConexao(cursor, cnx)

    return render(request, 'admin/cad_curso_turma.html', context)




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
            sigla = request.POST.get("sigla")

            if curso.strip() == '':
                erros.append("Curso inválido!")

            if not (erros):
                query = ("INSERT INTO Curso(sigla, nome)VALUES('{}', '{}');".format(sigla, curso))
                cursor.execute(query)
                cnx.commit()
            else:
                context["erros"] = erros
        finally:
            fecharConexao(cursor, cnx)

    return render(request, 'admin/cadastro_cursos.html', context)

