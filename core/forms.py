from django import forms

from core.models import Usuarios, Cursos, Perfis, DisciplinasEmentas, PlanosEnsinos, DisciplinasPlanosEnsinos, CursosDisciplinas


class UsuariosForm(forms.ModelForm):
    class Meta:
        model = Usuarios
        fields = ('USR_IdRA', 'USR_DssNome', 'USR_DssSenha', 'USR_IdPerfil')


class CursosForm(forms.ModelForm):
    class Meta:
        model = Cursos
        fields = ('CUR_DssCurso',)


class PerfisForm(forms.ModelForm):
    class Meta:
        model = Perfis
        fields = ('PRF_DssPerfil',)


class DisciplinasEmentasForm(forms.ModelForm):
    class Meta:
        model = DisciplinasEmentas
        fields = ('DIS_DssDisciplina', 'DIS_DssEmenta')


class PlanosEnsinosForm(forms.ModelForm):
    class Meta:
        model = PlanosEnsinos
        fields = ('PLE_DssPlanoEnsino',)


class DisciplinasPlanosEnsinosForm(forms.ModelForm):
    class Meta:
        model = DisciplinasPlanosEnsinos
        fields = ('DPL_IdDisciplina', 'DPL_IdPlanoEnsino')

class CursosDisciplinasForm(forms.ModelForm):
    class Meta:
        model = CursosDisciplinas
        fields = ('CDS_IdCurso', 'CDS_IdDisciplina')