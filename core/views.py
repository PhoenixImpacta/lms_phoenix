from django.shortcuts import render
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

        cursor.execute("SELECT * FROM Perfis")
        context = {'perfis': cursor.fetchall()}

        if request.POST:

                query = ("INSERT INTO Usuarios(USR_IdRA, USR_DssNome, USR_DssSenha, USR_IdPerfil)VALUES({}, '{}', '{}', {})".format(request.POST.get('ra'), request.POST.get('nome'), request.POST.get('senha'), request.POST.get('perfil')))

                cursor.execute(query)

                cnx.commit()
    finally:
        fecharConexao(cursor, cnx)

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
