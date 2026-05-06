from django.contrib import admin
from .models import Treinador, Modalidade, Socio, Aulas, Inscricao, PlanoTreino, Pagamento, Exercicio

@admin.register(Socio)
class SocioAdmin(admin.ModelAdmin):
    list_display = ('nome', 'email', 'contacto', 'dataAdesao')
    search_fields = ('nome', 'email')
    list_filter = ('dataAdesao',)

@admin.register(Treinador)
class TreinadorAdmin(admin.ModelAdmin):
    list_display = ('nome', 'especialidade')
    search_fields = ('nome', 'especialidade')

@admin.register(Modalidade)
class ModalidadeAdmin(admin.ModelAdmin):
    list_display = ('nome', 'intensidade')
    search_fields = ('nome',)

@admin.register(Aulas)
class AulasAdmin(admin.ModelAdmin):
    list_display = ('modalidade', 'treinador', 'data', 'hora', 'lotacao')
    list_filter = ('data',)

@admin.register(Inscricao)
class InscricaoAdmin(admin.ModelAdmin):
    list_display = ('socio', 'aula', 'dataRegisto') # No models está 'aula' e não 'aulas'
    list_filter = ('dataRegisto',)

@admin.register(PlanoTreino)
class PlanoTreinoAdmin(admin.ModelAdmin):
    list_display = ('socio', 'treinador', 'objetivo', 'data_inicio') # No models não tens 'nomePlano', usas 'objetivo'
    search_fields = ('socio__nome', 'objetivo')

@admin.register(Exercicio)
class ExercicioAdmin(admin.ModelAdmin):
    list_display = ('nome', 'series', 'repeticoes', 'planoTreino') # No models está 'nome' e 'planoTreino'
    search_fields = ('nome',)

@admin.register(Pagamento)
class PagamentoAdmin(admin.ModelAdmin):
    # Baseado na tua segunda classe Pagamento, que usa 'data_pago'
    list_display = ('socio', 'valor', 'data_pago', 'estado') 
    list_filter = ('estado', 'data_pago')
    search_fields = ('socio__nome',)