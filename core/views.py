from django.shortcuts import render, redirect, render_to_response, HttpResponse
from core.util.connection_db_mysql import abrirConexao, fecharConexao
from core.util.EnviarEmail import enviarEmail, enviarLink
from core.util.UploadFoto import save as salvar_foto
from core.util.CodigoAcesso import gerar_codigo
import datetime, ast, random


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

        cursor.execute(
            "select aviso, data_envio from HistoricoAvisos where ra_remetente = {};".format(usuario_logado['ra']))
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

        cursor.execute(
            "select aviso, data_envio from HistoricoAvisos where ra_remetente = {};".format(usuario_logado['ra']))
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

            if not (erros):
                file = request.FILES['file']
                caminho = salvar_foto(file)
                caminho = caminho.replace('core/static/', '').replace('%20', ' ')
                cursor.execute(
                    "insert into AlunoFoto(ra_aluno, caminho_foto) values ({}, '{}');".format(int(ra), caminho))

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


def abrir_matricula(request):
    cnx = abrirConexao()
    cursor = None
    usuario_logado = ast.literal_eval(request.COOKIES['usuario_logado'])
    context = {}

    if usuario_logado:
        context['usuario_logado'] = usuario_logado

    try:
        if cnx:
            cursor = cnx.cursor(dictionary=True)

        cursor.execute("select * from DisciplinaOfertada;")
        disciplinas = cursor.fetchall()
        context['disciplinas'] = disciplinas

        codigo = gerar_codigo()
        context['codigo'] = codigo

        if request.POST:
            '''1- Link da disciplina
               2- Codigo de acesso: 30 seg duração
               3- Os alunos acessam o link com o codigo de acesso
               4- Enviam os dados ao professor (email) e não no banco'''
            # salvar na sessão
            dpl = request.POST.get('disciplina')
            cursor.execute("select * from DisciplinaOfertada where nome_disciplina = '{}';".format(dpl))
            disciplina = cursor.fetchall()
            disciplina = dict(disciplina[0])

            resposta = render_to_response('professor/abrir_matricula.html', context)
            resposta.set_cookie("disciplina", disciplina, expires=datetime.timedelta(minutes=5), domain=None,
                                secure=False)
            resposta.set_cookie("codigo_acesso", codigo, max_age=30, domain=None, secure=False)

            crs = cnx.cursor()
            crs.execute("select email from Aluno;")
            emails = crs.fetchall()
            enviarLink(emails, "Acessem localhost:8000/matricular/")

            return resposta

    finally:
        fecharConexao(cursor, cnx)
    return render(request, 'professor/abrir_matricula.html', context)


def matricular(request):
    cnx = abrirConexao()
    cursor = None
    context = {}
    usuario_logado = ast.literal_eval(request.COOKIES['usuario_logado'])
    disciplina = ast.literal_eval(request.COOKIES['disciplina'])

    try:
        codigo = request.COOKIES['codigo_acesso']
    except KeyError:
        codigo = None

    if usuario_logado:
        context['usuario_logado'] = usuario_logado
    else:
        context['usuario_logado'] = None
    if disciplina:
        context['disciplina'] = disciplina
    else:
        context['disciplina'] = None
    if codigo:
        context['codigo_acesso'] = codigo
    else:
        context['codigo_acesso'] = None

    try:
        if cnx:
            cursor = cnx.cursor(dictionary=True)

        if request.POST and request.FILES['file']:
            erros = []

            nome = request.POST.get('nome')
            celular = request.POST.get('celular')
            email = request.POST.get('email')
            file = request.FILES['file']

            if nome.strip() == '':
                erros.append('Nome inválido')
            if celular.strip() == '':
                erros.append('Celular inválido')
            if email.strip() == '':
                erros.append('Email inválido')

            if not(erros):
                cursor.execute("select id_turma from CursoTurma where sigla_curso = '{}';".format(usuario_logado['sigla_curso']))
                id_turma = cursor.fetchall()[0][0]
                print(id_turma)
                #cursor.execute("insert into Matricula(ra_aluno, nome_disciplina, ano_ofertado, semestre_ofertado, id_turma) values ({}, '{}', {}, '{}', {});")
            else:
                context['erros'] = erros
    finally:
        fecharConexao(cursor, cnx)

    return render(request, 'aluno/matricular.html', context)


'''
O professor disponibiliza sua disciplina aos alunos fornecendo um link da disciplina e um código de acesso aos alunos.
Os alunos:
1.	Entram na página do link fornecido pelo professor utilizando o código de acesso que dará permissão para preencher seus dados de matrícula.
2.	Fornecem o nome completo, número de celular, foto do aluno e e-mail.
3.	Submetem os dados de matrícula ao professor.
O código de acesso tem duração de 30 segundos. Após esse tempo, o aluno precisa solicitar um novo código de acesso.
Após submissão, o aluno receberá um e-mail para que ele possa confirmar o seu desejo em se matricular na disciplina; tendo o tempo máximo de 5 minutos para essa submissão.

'''
