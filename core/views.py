from django.shortcuts import render, redirect, render_to_response, HttpResponse
from core.util.connection_db_mysql import abrirConexao, fecharConexao
from core.util.EnviarEmail import enviarEmail, enviarLink
from core.util.UploadFoto import save as salvar_foto
from core.util.CodigoAcesso import gerar_codigo
import datetime, ast, random

# Create your views here.
def index(request):
    usuario_logado = ast.literal_eval(request.COOKIES['usuario_logado'])
    context = {'usuario_logado': usuario_logado}
    return render(request, 'index.html', context)

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
            senha = request.POST.get('senha')
            if ra.strip() == '':
                erros.append("Ra inválido")

            if not (erros):
                usuario = None
                if tipo == 'a':
                    cursor.execute("select * from Aluno where ra={} and senha='{}'".format(ra, senha))
                    usuario = cursor.fetchall()
                elif tipo == 'p':
                    cursor.execute("select * from Professor where ra={} and senha='{}'".format(ra, senha))
                    usuario = cursor.fetchall()
                elif tipo == 'c':
                    cursor.execute("select * from Coordenador where ra={} and senha='{}'".format(ra, senha))
                    usuario = cursor.fetchall()

                if not (usuario):
                    erros.append("Usuário não existe")
                    context["erros"] = erros
                else:
                    usuario_logado = dict(usuario[0])
                    context['usuario_logado'] = usuario_logado
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
            # salvar na sessão
            dpl = request.POST.get('disciplina')
            cursor.execute("select * from DisciplinaOfertada where nome_disciplina = '{}';".format(dpl))
            disciplina = cursor.fetchall()
            disciplina = dict(disciplina[0])

            resposta = render_to_response('index.html', context)
            resposta.set_cookie("disciplina", disciplina, expires=datetime.timedelta(minutes=5), domain=None,
                                secure=False)
            resposta.set_cookie("codigo_acesso", codigo, max_age=30, domain=None, secure=False)

            crs = cnx.cursor()
            crs.execute("select email from Aluno;")
            emails = crs.fetchall()
            enviarLink(emails, "Acessem localhost:8000/matricular/\n"
                               "Código de acesso: " + str(codigo))

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

            if not (erros):
                if usuario_logado['tipo'] == 'ALUNO':
                    caminho = salvar_foto(file)
                    caminho = caminho.replace('core/static/', '').replace('%20', ' ')
                    cursor.execute(
                        "insert into AlunoFoto(ra_aluno, caminho_foto) values ({}, '{}');".format(usuario_logado['ra'],
                                                                                                  caminho))
                    cursor.execute("select id_turma from CursoTurma where sigla_curso = '{}';".format(
                        usuario_logado['sigla_curso']))
                    id_turma = cursor.fetchall()[0]

                    matricula = {'nome': nome, 'celular': celular, 'email': email, 'caminho': caminho,
                                 'id_turma': id_turma}

                    resposta = render_to_response('index.html', context)
                    resposta.set_cookie("matricula", matricula, max_age=datetime.timedelta(minutes=5),
                                        expires=datetime.timedelta(minutes=5), domain=None,
                                        secure=False)
                    return resposta
            else:
                context['erros'] = erros
    finally:
        fecharConexao(cursor, cnx)

    return render(request, 'aluno/matricular.html', context)

def confirmar_matricula(request):
    cnx = abrirConexao()
    cursor = None
    context = {}
    usuario_logado = ast.literal_eval(request.COOKIES['usuario_logado'])
    disciplina = ast.literal_eval(request.COOKIES['disciplina'])

    if usuario_logado:
        context['usuario_logado'] = usuario_logado
    else:
        context['usuario_logado'] = None
    if disciplina:
        context['disciplina'] = disciplina
    else:
        context['disciplina'] = None

    try:
        matricula = request.COOKIES['matricula']
    except KeyError:
        matricula = None

    try:
        if cnx:
            cursor = cnx.cursor(dictionary=True)

        if matricula:
            context['matricula'] = matricula

        if request.POST:
            if matricula and usuario_logado['tipo'] == 'PROFESSOR':
                opcao = request.POST.get('opcao')

                if opcao == 'yes':
                    cursor.execute(
                        "insert into Matricula(ra_aluno, nome_disciplina, ano_ofertado, semestre_ofertado, id_turma) values ({}, '{}', {}, '{}', {});".format(
                            usuario_logado['ra'], disciplina['nome_disciplina'], disciplina['ano'],
                            disciplina['semestre'], matricula['id_turma']))
                    enviarEmail(matricula['email'], "Parabéns sua matricula foi aprovada!")

                    context['usuario_logado'] = usuario_logado
                    resposta = render_to_response('index.html', context)
                    resposta.delete_cookie('disciplina')
                    return resposta
                else:
                    enviarEmail(matricula['email'],
                                "Sua matricula foi reprovada!!!\nPor favor fale com seu professor!")
                    context['usuario_logado'] = usuario_logado
                    resposta = render_to_response('index.html', context)
                    resposta.delete_cookie('disciplina')
                    return resposta
    finally:
        fecharConexao(cursor, cnx)

    return render(request, 'professor/confirmar_matricula.html', context)

def logout(request):
    usuario_logado = ast.literal_eval(request.COOKIES['usuario_logado'])
    context = {}
    context['usuario_logado'] = usuario_logado
    resposta = render_to_response('login', context)
    resposta.delete_cookie('usuario_logado')
    return resposta

#========================================================
def cadastro_perfis(request):
    context = {}

    usuario_logado = request.COOKIES['usuario_logado']

    if usuario_logado:
        context = {'usuario_logado': usuario_logado}

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

def cadastro_curso_turma(request):
    cnx = abrirConexao()
    cursor = None

    usuario_logado = request.COOKIES['usuario_logado']

    if usuario_logado:
        context = {'usuario_logado': usuario_logado}


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


                verifica = []
                for i in range(0, len(CT)):
                    CR = CT[i]
                    for n in range(0, len(lista)):
                        ver = (lista.get('sigla_curso') == CR.get('sigla_curso')and lista.get('nome_disciplina') == CR.get('nome_disciplina')and int(lista.get('id_turma')) == int(CR.get('id_turma')) and int(lista.get('ano_ofertado')) == int(CR.get('ano_ofertado'))and int(lista.get('semestre_ofertado')) == int(CR.get('semestre_ofertado')))
                        verifica.append(ver)
                        print(verifica)


                '''INSERE NA TABELA CURSOTURMA OS VALORES SELECIONADOS'''
                if True in verifica:
                    mensagem = ("ALERTA : Cadastro para {} já existente".format(curso))
                    context['mensagem'] = mensagem

                else:
                    cursoTurma = cursor.execute("insert into CursoTurma(sigla_curso, nome_disciplina, id_turma, ano_ofertado, semestre_ofertado) values('{}', '{}', {}, {}, {})".format(sig, disciplina, id_turma, ano, semestre))
                    cursor.execute(cursoTurma)
                    cnx.commit()

                    mensagem = ("{} editado com sucesso".format(curso))
                    context['mensagem'] = mensagem




            else:
                erros.append("Seleção invalida")
                context["erros"] = erros
    finally:
        fecharConexao(cursor, cnx)

    return render(request, 'admin/cad_curso_turma.html', context)

def cadastro_curso(request):
    context = {}

    usuario_logado = request.COOKIES['usuario_logado']

    if usuario_logado:
        context = {'usuario_logado': usuario_logado}

    if request.POST:
        cnx = abrirConexao()
        cursor = None

        if cnx:
            cursor = cnx.cursor()

        try:
            erros = []
            curso = request.POST.get("curso")
            sigla = request.POST.get("sigla")

            cursor.execute("select * from Curso")
            cursos = cursor.fetchall()

            if curso.strip() == '':
                erros.append("Curso inválido!")

            if not (erros):


                lista = {'curso': curso, 'sigla': sigla}
                lista_curso = []

                cs = lista.get('curso')
                sig = lista.get('sigla')

                for i in range(0, len(cursos)):
                    lc = cursos[i]
                    for n in lc:
                        lista_curso.append(n)

                print(lista_curso)

                if cs in lista_curso or sig in lista_curso:
                    mensagem = ('ALERTA: {} ja existente'.format(curso))
                    context['mensagem'] = mensagem
                else:

                    query = ("INSERT INTO Curso(sigla, nome)VALUES('{}', '{}');".format(sigla, curso))
                    cursor.execute(query)
                    cnx.commit()
                    mensagem = ('{} adicionado com sucesso'.format(curso))
                    context['mensagem'] = mensagem


            else:
                context["erros"] = erros
        finally:
            fecharConexao(cursor, cnx)

    return render(request, 'admin/cadastro_cursos.html', context)

def cadastro_disciplina(request):
    context = {}

    usuario_logado = request.COOKIES['usuario_logado']

    if usuario_logado:
        context = {'usuario_logado': usuario_logado}


    if request.POST:
        cnx = abrirConexao()
        cursor = None

        if cnx:
            cursor = cnx.cursor()
        try:
            erros = []
            disciplina = request.POST.get('disciplina')

            cursor.execute("select * from Disciplina")
            dis = cursor.fetchall()
            if not (erros):

                lista_dis = {"nome": disciplina}
                lista = []

                dex = lista_dis.get('nome')

                for i in range(0, len(dis)):
                    lc = dis[i]
                    for n in lc:
                        lista.append(n)

                if dex in lista:
                    mensagem = ('{} ja existente'.format(disciplina))
                    context['mensagem'] = mensagem

                else:
                    query = cursor.execute("insert into Disciplina(nome) values('{}')".format(disciplina))
                    cursor.execute(query)
                    cnx.commit()
                    mensagem = ('{} adicionado com sucesso'.format(disciplina))
                    context['mensagem'] = mensagem

                if disciplina.strip() == '':
                    erros.append("Disciplina inválida!")

            else:
                context["erros"] = erros


        finally:
            fecharConexao(cursor, cnx)

    return render(request, 'admin/cadastro_disciplina.html', context)

def editar_disciplina(request):
    cnx = abrirConexao()
    cursor = None
    if cnx:
        cursor = cnx.cursor(dictionary=True)

    usuario_logado = request.COOKIES['usuario_logado']

    if usuario_logado:
        context = {'usuario_logado': usuario_logado}

    erros = []
    cursor.execute("select * from Disciplina")
    dis = cursor.fetchall()
    context = {'disciplina': dis}





    if request.POST:


        try:
            erros = []
            disciplina = request.POST.get('disciplina')
            carga_horaria = request.POST.get('carga_horaria')
            teoria = request.POST.get('teoria')
            pratica = request.POST.get('pratica')
            ementa = request.POST.get('ementa')
            competencias = request.POST.get('competencias')
            habilidades = request.POST.get('habilidades')
            conteudo = request.POST.get('conteudo')
            bibliografia_basica = request.POST.get('bibliografia_basica')
            bibliografia_complementar = request.POST.get('bibliografia_complementar')

            print(disciplina, '-----------------------')


            if not (erros):
                if disciplina == None:
                    mensagem = ("ESCOLHA UMA DISCIPLINA")
                    context['mensagem'] = mensagem

                else:
                    query = cursor.execute(
                    "update Disciplina set carga_horaria = '{}', teoria = '{}', pratica = '{}', ementa = '{}', competencias = '{}', habilidades = '{}', conteudo = '{}', bibliografia_basica = '{}', bibliografia_complementar = '{}' where nome='{}'".format(
                            carga_horaria, teoria, pratica, ementa, competencias, habilidades, conteudo,
                            bibliografia_basica, bibliografia_complementar, disciplina))
                    cursor.execute(query)
                    cnx.commit()

                mensagem = ("{} editado".format(disciplina))
                context['mensagem'] = mensagem

            else:
                context["erros"] = erros


        finally:
            fecharConexao(cursor, cnx)

    return render(request, 'admin/edit_disciplina.html', context)

def deleta_disciplina(request):


    cnx = abrirConexao()
    cursor = None
    if cnx:
        cursor = cnx.cursor(dictionary=True)

    usuario_logado = request.COOKIES['usuario_logado']

    if usuario_logado:
        context = {'usuario_logado': usuario_logado}

    erros = []
    cursor.execute("select * from Disciplina")
    dis = cursor.fetchall()
    context = {'disciplina': dis}
    title = ('Deleta disciplina')
    context['title'] = title


    if request.POST:


        try:
            erros = []
            disciplina = request.POST.get('disciplina')

            print(disciplina, '-----------------------')


            if not (erros):
                if disciplina == None:
                    mensagem = ("ESCOLHA UMA DISCIPLINA")
                    context['mensagem'] = mensagem

                else:
                    query = cursor.execute("delete from Disciplina where nome = '{}'".format(disciplina))
                    cursor.execute(query)
                    cnx.commit()

                mensagem = ("{} deletado".format(disciplina))
                context['mensagem'] = mensagem

            else:
                context["erros"] = erros


        finally:
            fecharConexao(cursor, cnx)

    return render(request, 'admin/deleta_disciplina.html', context)

def deleta_curso(request):


    cnx = abrirConexao()
    cursor = None
    if cnx:
        cursor = cnx.cursor(dictionary=True)

    usuario_logado = request.COOKIES['usuario_logado']

    if usuario_logado:
        context = {'usuario_logado': usuario_logado}

    erros = []
    cursor.execute("select * from Curso")
    cs = cursor.fetchall()
    context = {'curso': cs}
    title = ('Deleta curso')
    context['title'] = title


    if request.POST:


        try:
            erros = []
            curso = request.POST.get('curso')

            print(curso, '-----------------------')


            if not (erros):
                if curso == None:
                    mensagem = ("ESCOLHA UM CURSO")
                    context['mensagem'] = mensagem

                else:
                    query = cursor.execute("delete from Curso where nome = '{}'".format(curso))
                    cursor.execute(query)
                    cnx.commit()

                mensagem = ("{} deletado".format(curso))
                context['mensagem'] = mensagem

            else:
                context["erros"] = erros


        finally:
            fecharConexao(cursor, cnx)

    return render(request, 'admin/deleta_curso.html', context)

def lista_disciplina(request):
    cnx = abrirConexao()
    cursor = None
    context = {}

    usuario_logado = request.COOKIES['usuario_logado']

    if usuario_logado:
        context['usuario_logado'] = usuario_logado


    if cnx:
        cursor = cnx.cursor(dictionary=True)

    try:
        cursor.execute("select * from Disciplina")
        dis = cursor.fetchall()

        context['disciplina'] = dis

        title = ('Lista de disciplinas')

        context['title'] = title


    finally:
        fecharConexao(cursor, cnx)

    return render(request, 'admin/lista_disciplina.html', context)

def lista_curso(request):
    cnx = abrirConexao()
    cursor = None
    context = {}

    usuario_logado = request.COOKIES['usuario_logado']

    if usuario_logado:
        context['usuario_logado'] = usuario_logado


    if cnx:
        cursor = cnx.cursor(dictionary=True)

    try:
        cursor.execute("select * from Curso")
        curso = cursor.fetchall()

        context['curso'] = curso

        title = ('Lista de cursos')

        context['title'] = title


    finally:
        fecharConexao(cursor, cnx)

    return render(request, 'admin/lista_curso.html', context)
