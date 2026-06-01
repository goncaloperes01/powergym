from django import forms
from .models import Socio, Treinador, Modalidade, Aulas, Inscricao, PlanoTreino, Exercicio, Pagamento

class SocioForm(forms.ModelForm):
    class Meta:
        model = Socio
        fields = '__all__'
        widgets = {
            'dataNascimento': forms.DateInput(attrs={'type': 'date'}),
            'dataAdesao': forms.DateInput(attrs={'type': 'date'}),
            'foto': forms.FileInput(attrs={'accept': 'image/*'}),
        }

class TreinadorForm(forms.ModelForm):
    class Meta:
        model = Treinador
        fields = '__all__'
        widgets = {
            'foto': forms.FileInput(attrs={'accept': 'image/*'}),
        }

class ModalidadeForm(forms.ModelForm):
    class Meta:
        model = Modalidade
        fields = '__all__'

class AulasForm(forms.ModelForm):
    class Meta:
        model = Aulas
        fields = '__all__'
        widgets = {
            'data': forms.DateInput(attrs={'type': 'date'}),
            'hora': forms.TimeInput(attrs={'type': 'time'}),
        }

class InscricaoForm(forms.ModelForm):
    class Meta:
        model = Inscricao
        fields = '__all__'
        # dataRegisto é automático, não precisa de form

class PlanoTreinoForm(forms.ModelForm):
    class Meta:
        model = PlanoTreino
        fields = '__all__'
        widgets = {
            'data_inicio': forms.DateInput(attrs={'type': 'date'}),
        }

class ExercicioForm(forms.ModelForm):
    planoTreino = forms.ModelChoiceField(
        queryset=PlanoTreino.objects.all(),
        required=False,
        label='Plano de treino',
        empty_label='Catálogo geral (sem plano associado)'
    )

    class Meta:
        model = Exercicio
        fields = '__all__'

# Adiciona isto no final do teu forms.py
from django import forms
from .models import Pagamento

class PagamentoForm(forms.ModelForm):
    class Meta:
        model = Pagamento
        fields = ['socio', 'valor', 'data_pago', 'estado', 'data_vencimento', 'frequencia', 'descritivo']
        labels = {
            'data_pago': 'Data',  # Altera a etiqueta para mostrar apenas "Data"
            'data_vencimento': 'Data de Vencimento',
            'descritivo': 'Descritivo (Máx. 25 letras)',
        }
        widgets = {
            # Força o HTML a usar um calendário (date picker)
            'data_pago': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'data_vencimento': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            
            # Adiciona classes do Bootstrap e IDs aos outros campos para o Javascript funcionar
            'socio': forms.Select(attrs={'class': 'form-select'}),
            'valor': forms.NumberInput(attrs={'class': 'form-control'}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
            'frequencia': forms.Select(attrs={'class': 'form-select', 'id': 'id_frequencia'}),
            'descritivo': forms.TextInput(attrs={'class': 'form-control', 'id': 'id_descritivo'}),
        }
