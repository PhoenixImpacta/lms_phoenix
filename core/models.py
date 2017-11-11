from django.db import models


# Create your models here.
class Perfis(models.Model):
    PRF_IdPerfil = models.AutoField(primary_key=True)
    PRF_DssPerfil = models.CharField(max_length=15)

    def __str__(self):
        return self.PRF_DssPerfil


class Usuarios(models.Model):
    USR_IdRA = models.IntegerField(primary_key=True, unique=True)
    USR_DssNome = models.CharField(max_length=70, default='')
    USR_DssSenha = models.CharField(max_length=12, default='')
    USR_IdPerfil = models.ForeignKey(Perfis, default=None)

    def __str__(self):
        return self.USR_IdRA


class Cursos(models.Model):
    CUR_IdCurso = models.AutoField(primary_key=True)
    CUR_DssCurso = models.CharField(max_length=40, default='')

    def __str__(self):
        return self.CUR_DssCurso


class DisciplinasEmentas(models.Model):
    DIS_IdDisciplina = models.AutoField(primary_key=True)
    DIS_DssDisciplina = models.CharField(max_length=40, default='')
    DIS_DssEmenta = models.CharField(max_length=300, default='')

    def __str__(self):
        return self.DIS_DssDisciplina


class PlanosEnsinos(models.Model):
    PLE_IdPlanoEnsino = models.AutoField(primary_key=True)
    PLE_DssPlanoEnsino = models.CharField(max_length=30, default='')

    def __str__(self):
        return self.PLE_DssPlanoEnsino


class DisciplinasPlanosEnsinos(models.Model):
    DPL_IdDisciplina = models.ForeignKey(DisciplinasEmentas, primary_key=True)
    DPL_IdPlanoEnsino = models.ForeignKey(PlanosEnsinos)


class CursosDisciplinas(models.Model):
    CDS_IdCurso = models.ForeignKey(Cursos)
    CDS_IdDisciplina = models.ForeignKey(DisciplinasEmentas)
