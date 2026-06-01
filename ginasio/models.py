from django.db import models
from django.contrib.auth.models import User


class Socio(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    nome = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    contacto = models.CharField(max_length=15, null=True, blank=True)
    dataNascimento = models.DateField(null=True, blank=True)
    dataAdesao = models.DateField(auto_now_add=True)
    foto = models.ImageField(upload_to='socios_fotos/', null=True, blank=True)

    def __str__(self):
        return self.nome


class Treinador(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    nome = models.CharField(max_length=100)
    especialidade = models.CharField(max_length=100)
    biografia = models.TextField(blank=True, null=True)
    foto = models.ImageField(upload_to='fotos/', null=True, blank=True)

    def __str__(self):
        return f"{self.nome} ({self.especialidade})"


class Modalidade(models.Model):
    nome = models.CharField(max_length=50)
    descricao = models.TextField(blank=True, null=True)
    intensidade = models.CharField(max_length=20, blank=True, null=True, help_text="Ex: Baixa, Media, Alta")

    def __str__(self):
        return self.nome


class Aulas(models.Model):
    modalidade = models.ForeignKey(Modalidade, on_delete=models.CASCADE)
    treinador = models.ForeignKey(Treinador, on_delete=models.CASCADE)
    data = models.DateField()
    hora = models.TimeField()
    lotacao = models.IntegerField()

    def __str__(self):
        return f"{self.modalidade.nome} - {self.data} as {self.hora}"


class Inscricao(models.Model):
    socio = models.ForeignKey(Socio, on_delete=models.CASCADE)
    aula = models.ForeignKey(Aulas, on_delete=models.CASCADE)
    dataRegisto = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.socio.nome} -> {self.aula.modalidade.nome}"


class PlanoTreino(models.Model):
    socio = models.ForeignKey(Socio, on_delete=models.CASCADE)
    treinador = models.ForeignKey(Treinador, on_delete=models.CASCADE)
    objetivo = models.CharField(max_length=100)
    data_inicio = models.DateField()

    def __str__(self):
        return f"Plano de {self.socio.nome} ({self.objetivo})"


class Exercicio(models.Model):
    planoTreino = models.ForeignKey(PlanoTreino, on_delete=models.SET_NULL, null=True, blank=True)
    nome = models.CharField(max_length=50)
    series = models.IntegerField()
    repeticoes = models.IntegerField()
    descanso_segundos = models.IntegerField()

    def __str__(self):
        return f"{self.nome} ({self.series}x{self.repeticoes})"


class Pagamento(models.Model):
    ESTADO_CHOICES = [
        ('Liquidado', 'Liquidado'),
        ('Pendente', 'Pendente'),
        ('Atrasado', 'Atrasado'),
    ]
    FREQUENCIA_CHOICES = [
        ('Unico', 'Pagamento Unico'),
        ('Mensal', 'Mensalidade'),
    ]

    socio = models.ForeignKey(Socio, on_delete=models.CASCADE)
    valor = models.FloatField()
    data_vencimento = models.DateField()
    data_pago = models.DateField()
    estado = models.CharField(max_length=50, choices=ESTADO_CHOICES, default='Pendente')
    frequencia = models.CharField(max_length=50, choices=FREQUENCIA_CHOICES, default='Mensal')
    descritivo = models.CharField(max_length=25, blank=True, null=True)

    def __str__(self):
        return f"{self.socio.nome} - {self.valor} EUR ({self.estado})"
