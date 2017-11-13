from django.shortcuts import render, redirect
from core.util.connection_db_mysql import abrirConexao, fecharConexao


# Create your views here.
def index(request):
    cnx = abrirConexao()
    cursor = None

    if cnx:
        cursor = cnx.cursor(buffered=True, dictionary=True)


    try:
        cursor.execute("SELECT * FROM Usuarios")

        context = {'usuarios': cursor.fetchall()}

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
                cursor.execute("select * from Usuarios where ra={} and senha ={}".format(ra, senha))
                usuario = cursor.fetchall()

                if usuario:
                    erros.append("Usuário não existe")
                    context["erros"] = erros
                else:
                    pass
                    # Salvar Sessão

            else:
                context["erros"] = erros
                print("***************** ", context)
                print("***************** ", erros)
    finally:
        fecharConexao(cursor, cnx)

    print("============ ", context)
    return render(request, 'login.html', context)
