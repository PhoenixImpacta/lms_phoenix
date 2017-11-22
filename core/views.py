from django.shortcuts import render, redirect, render_to_response
from core.util.connection_db_mysql import abrirConexao, fecharConexao
from core.util.EnviarEmail import enviarEmail
from core.util.UploadFoto import save as salvar_foto
import datetime, ast


# Create your views here.
def index(request):
    cursor = None
    cnx = abrirConexao()
    usuario_logado = ast.literal_eval(request.COOKIES['usuario_logado'])
    context = {'usuario_logado': usuario_logado}
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
            if ra.strip() == '':
                erros.append("Ra inválido")

            if not (erros):
                usuario = None
                if tipo == 'a':
                    cursor.execute("select * from Aluno where ra={}".format(ra))
                    usuario = cursor.fetchall()
                elif tipo == 'p':
                    cursor.execute("select * from Professor where ra={}".format(ra))
                    usuario = cursor.fetchall()

                if not (usuario):
                    erros.append("Usuário não existe")
                    context["erros"] = erros
                else:
                    usuario_logado = dict(usuario[0])
                    resposta = render_to_response("index.html", context)
                    max_age = 365 * 24 * 60 * 60  # one year
                    expires = datetime.datetime.strftime(
                        datetime.datetime.utcnow() + datetime.timedelta(seconds=max_age), "%a, %d-%b-%Y %H:%M:%S GMT")
                    resposta.set_cookie("usuario_logado", usuario_logado, max_age=max_age, expires=expires, domain=None,
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

    usuario_logado = ast.literal_eval(request.COOKIES['usuario_logado'])

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
                    cursor.execute("select ra from Aluno;")
                    ids = cursor.fetchall()

                    for x in range(0, len(ids)):
                        # Inserir histórico
                        if ids[x][0] != usuario_logado['ra']:
                            cursor.execute(
                                "insert into HistoricoAvisos(aviso, data_envio, ra_usuario, ra_remetente) values ('{}', '{}', {}, {} );".format(
                                    aviso, datetime.date.today(), usuario_logado['ra'], ids[x][0]))

                elif para == 'professores':
                    cursor.execute("select email from Professor;")
                    email = cursor.fetchall()
                    enviarEmail(email, aviso)
                    cursor.execute("select ra from Professor;")
                    ids = cursor.fetchall()

                    for x in range(0, len(ids)):
                        # Inserir histórico
                        if ids[x][0] != usuario_logado['ra']:
                            cursor.execute(
                                "insert into HistoricoAvisos(aviso, data_envio, ra_usuario, ra_remetente) values ('{}', '{}', {}, {} );".format(
                                    aviso, datetime.date.today(), usuario_logado['ra'], ids[x][0]))
            else:
                context['erros'] = erros
    finally:
        fecharConexao(cursor, cnx)

    return render(request, 'avisos.html', context)


def enviar_aviso_nova_atividade(request):
    cnx = abrirConexao()
    cursor = None

    try:
        if cnx:
            cursor = cnx.cursor()

        usuario_logado = request.COOKIES['usuario_logado']
        context = {'usuario_logado': usuario_logado}

        if request.POST:
            erros = []
            nome = request.POST.get('nome')
            sumario = request.POST.get('sumario')
            instrucoes = request.POST.get('instrucoes')
            data = request.POST.get('data')

            if nome.strip() == '':
                erros.append('Nome inválido!')
            if sumario.strip() == '':
                erros.append('Sumário inválido!')
            if instrucoes.strip() == '':
                erros.append('Instruções inválidas!')
            if data.strip() == '':
                erros.append('Data inválida!')

            if not (erros):
                cursor.execute('select email from Aluno;')
                alunos = cursor.fetchall()

                cursor.execute(
                    "insert into HistoricoAtividade (sumario, nome, ra_professor, instrucoes, data_entrega) values('{}', '{}', {} , '{}', '{}');".format(
                        sumario, nome, 2000, instrucoes, datetime.datetime.strptime(data, '%d/%m/%Y').date()))
                enviarEmail(alunos, 'ola aluno tem nova atividade')
            else:
                context['erros'] = erros

    finally:
        fecharConexao(cursor, cnx)

    return render(request, 'professor/aviso_nova_atividade.html', context)


def enviar_aviso_para_aluno(request):
    cnx = abrirConexao()
    cursor = None
    usuario_logado = ast.literal_eval(request.COOKIES['usuario_logado'])
    context = {}

    if usuario_logado:
        context['usuario_logado'] = usuario_logado

    try:
        if cnx:
            cursor = cnx.cursor(dictionary=True)

        cursor.execute(
            "select ra, nome from Aluno as a inner join Matricula as m on a.ra = m.ra_aluno inner join Turma as t where m.id_turma = t.id_turma and t.ra_professor = {} group by a.nome;".format(
                usuario_logado['ra']))
        context['alunos'] = cursor.fetchall()

    finally:
        fecharConexao(cursor, cnx)

    return render(request, "professor/aviso_aluno.html", context)


def aviso_aluno(request, ra_aluno):
    cnx = abrirConexao()
    cursor = None
    usuario_logado = ast.literal_eval(request.COOKIES['usuario_logado'])
    context = {}

    if usuario_logado:
        context['usuario_logado'] = usuario_logado

    try:
        if cnx:
            cursor = cnx.cursor()

        if request.POST:
            erros = []
            aviso = request.POST.get('aviso')

            if aviso.strip() == '':
                erros.append("Aviso inválido")

            if not (erros):
                cursor.execute("SELECT email FROM Aluno where ra = {};".format(ra_aluno))
                email = cursor.fetchall()
                enviarEmail(email, aviso)

                cursor.execute(
                    "insert into HistoricoAvisos(aviso, data_envio, ra_usuario, ra_remetente) values ('{}', '{}', {}, {} );".format(
                        aviso, datetime.date.today(), usuario_logado['ra'], ra_aluno))
            else:
                context['erros'] = erros

    finally:
        fecharConexao(cursor, cnx)

    return render(request, "professor/aviso_area_aluno.html", context)

def visualizar_avisos_professor(request):
    cnx = abrirConexao()
    cursor = None
    usuario_logado = ast.literal_eval(request.COOKIES['usuario_logado'])
    context = {}

    if usuario_logado:
        context['usuario_logado'] = usuario_logado

    try:
        if cnx:
            cursor = cnx.cursor(dictionary=True)

        cursor.execute("select aviso, data_envio from HistoricoAvisos where ra_remetente = {};".format(usuario_logado['ra']))
        avisos = cursor.fetchall()
        context['avisos'] = avisos

    finally:
        fecharConexao(cursor, cnx)

    return render(request, 'professor/visualizar_avisos_professor.html', context)

def cadastrar_questoes(request):
    cnx = abrirConexao()
    cursor = None

    try:
        if cnx:
            cursor = cnx.cursor(dictionary=True)

        usuario_logado = ast.literal_eval(request.COOKIES['usuario_logado'])
        context = {'usuario_logado': usuario_logado}
        cursor.execute('select nome_disciplina from Turma where ra_professor = {};'.format(usuario_logado['ra']))
        disciplinas = cursor.fetchall()
        context['disciplinas'] = disciplinas

        if request.POST:
            disciplina = request.POST.get('disciplina')
            num_questao = request.POST.get('num_questao')
            data_entrega = request.POST.get('data_entrega')
            descricao = request.POST.get('descricao')

            cursor.execute("select * from DisciplinaOfertada where nome_disciplina = '{}';".format(disciplina))
            disciplina_ofertada = cursor.fetchall()

            cursor.execute("select id_turma from Turma where nome_disciplina = '{}';".format(disciplina))
            id_turma = cursor.fetchall()

            cursor.execute("insert into Questao values('{}', {}, '{}', {}, {}, '{}', '{}', '{}')".format(
                disciplina_ofertada[0]['nome_disciplina'], disciplina_ofertada[0]['ano'],
                disciplina_ofertada[0]['semestre'], id_turma[0]['id_turma'], num_questao,
                datetime.datetime.strptime(data_entrega, '%d/%m/%Y').date(), descricao, datetime.date.today()))

            enviarEmail('michael.jordan.java@gmail.com', 'ola aluno temos novas atividades')

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


def teste_v_f(request):
    return render(request, 'professor/teste_v_f.html')



# ALUNO
def visualizar_avisos(request):
    cnx = abrirConexao()
    cursor = None
    usuario_logado = ast.literal_eval(request.COOKIES['usuario_logado'])
    context = {}

    if usuario_logado:
        context['usuario_logado'] = usuario_logado

    try:
        if cnx:
            cursor = cnx.cursor(dictionary=True)

        cursor.execute("select aviso, data_envio from HistoricoAvisos where ra_remetente = {};".format(usuario_logado['ra']))
        avisos = cursor.fetchall()
        context['avisos'] = avisos

    finally:
        fecharConexao(cursor, cnx)

    return render(request, 'aluno/visualizar_avisos_aluno.html', context)

def aviso_professor(request, ra_professor):
    cnx = abrirConexao()
    cursor = None
    usuario_logado = ast.literal_eval(request.COOKIES['usuario_logado'])
    context = {}

    if usuario_logado:
        context['usuario_logado'] = usuario_logado

    try:
        if cnx:
            cursor = cnx.cursor()

        if request.POST:
            erros = []
            aviso = request.POST.get('aviso')

            if aviso.strip() == '':
                erros.append("Aviso inválido")

            if not (erros):
                cursor.execute("SELECT email FROM Professor where ra = {};".format(ra_professor))
                email = cursor.fetchall()
                enviarEmail(email, aviso)

                cursor.execute(
                    "insert into HistoricoAvisos(aviso, data_envio, ra_usuario, ra_remetente) values ('{}', '{}', {}, {} );".format(
                        aviso, datetime.date.today(), usuario_logado['ra'], ra_professor))
            else:
                context['erros'] = erros

    finally:
        fecharConexao(cursor, cnx)

    return render(request, "aluno/aviso_area_professor.html", context)

def enviar_aviso_para_professor(request):
    cnx = abrirConexao()
    cursor = None
    usuario_logado = ast.literal_eval(request.COOKIES['usuario_logado'])
    context = {}

    if usuario_logado:
        context['usuario_logado'] = usuario_logado

    try:
        if cnx:
            cursor = cnx.cursor(dictionary=True)

        cursor.execute(
            "select ra, nome from Professor as p inner join Matricula as m on m.ra_aluno = {}  inner join Turma as t on t.id_turma = m.id_turma  where t.ra_professor = p.ra group by p.nome order by p.ra;".format(
                usuario_logado['ra']))
        context['professores'] = cursor.fetchall()

    finally:
        fecharConexao(cursor, cnx)

    return render(request, "aluno/aviso_professor.html", context)

def upload_foto(request):
    cnx = abrirConexao()
    cursor = None
    usuario_logado = ast.literal_eval(request.COOKIES['usuario_logado'])
    context = {}

    if usuario_logado:
        context['usuario_logado'] = usuario_logado

    try:
        if cnx:
            cursor = cnx.cursor()

        if request.POST and request.FILES['file']:
            erros = []
            ra = request.POST.get('ra')


            if int(ra) < 1000:
                erros.append("RA Inválido!")

            if not(erros):
                file = request.FILES['file']
                caminho = salvar_foto(file)
                caminho = caminho.replace('core/static/', '').replace('%20', ' ')
                cursor.execute("insert into AlunoFoto(ra_aluno, caminho_foto) values ({}, '{}');".format(int(ra), caminho))

            else:
                context['erros'] = erros
    finally:
        fecharConexao(cursor, cnx)

    return render(request, 'aluno/upload_foto.html', context)

    # 7486354


def perfil_aluno(request):
    cnx = abrirConexao()
    cursor = None
    usuario_logado = ast.literal_eval(request.COOKIES['usuario_logado'])
    context = {}

    if usuario_logado:
        context['usuario_logado'] = usuario_logado

    try:
        if cnx:
            cursor = cnx.cursor(dictionary=True)

        cursor.execute("select * from AlunoFoto where ra_aluno = {};".format(usuario_logado['ra']))

        foto_aluno = cursor.fetchall()[0]
        context['foto_aluno'] = foto_aluno

    finally:
        fecharConexao(cursor, cnx)

    return render(request, 'aluno/perfil.html', context)


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
