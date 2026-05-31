from django.shortcuts import render, redirect, get_object_or_404
from .models import Socio, Treinador, Aulas, Modalidade, Inscricao, PlanoTreino, Exercicio, Pagamento
from .forms import SocioForm, TreinadorForm, ModalidadeForm, AulasForm, InscricaoForm, PlanoTreinoForm, ExercicioForm, PagamentoForm
from datetime import date, timedelta
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib import messages
from functools import wraps

import qrcode
import base64
from io import BytesIO


def admin_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if not request.user.is_superuser:
            return redirect('redirecionar_login')
        return view_func(request, *args, **kwargs)
    return wrapper

def landing_page(request):
    """
    Página principal pública do site (Landing Page).
    """
    modalidades_destaque = Modalidade.objects.all()
    equipa_destaque = Treinador.objects.all()
    
    context = {
        'modalidades': modalidades_destaque,
        'treinadores': equipa_destaque,
        'total_modalidades': Modalidade.objects.count(),
        'total_treinadores': Treinador.objects.count(),
        'total_socios': Socio.objects.count(),
        'total_aulas': Aulas.objects.count(),
    }
    return render(request, 'ginasio/landing.html', context)

@login_required(login_url='login')
def index(request):
    """
    Dashboard de Administração com os dados preparados para os Gráficos Visuais.
    """
    if not request.user.is_superuser:
        # A nossa porta inteligente para expulsar clientes daqui
        return redirect('perfil_cliente')

    hoje = date.today()
    Pagamento.objects.filter(estado='Pendente', data_vencimento__lt=hoje).update(estado='Atrasado')

    # Contagens Financeiras isoladas para enviar para o Gráfico
    pendentes = Pagamento.objects.filter(estado='Pendente').count()
    atrasados = Pagamento.objects.filter(estado='Atrasado').count()
    pagos = Pagamento.objects.filter(estado='Liquidado').count()

    context = {
        'num_socios': Socio.objects.count(),
        'num_treinadores': Treinador.objects.count(),
        'num_aulas': Aulas.objects.count(),
        'num_modalidades': Modalidade.objects.count(),
        'num_inscricoes': Inscricao.objects.count(),
        'num_planos': PlanoTreino.objects.count(),
        'num_exercicios': Exercicio.objects.count(),
        'num_pagamentos': Pagamento.objects.count(),
        
        # Dados que os gráficos vão "beber"
        'num_pendentes': pendentes,
        'num_atrasados': atrasados,
        'num_pagos': pagos, 
    }
    return render(request, 'ginasio/index.html', context)

# --- SÓCIOS ---
@admin_required
def socio_list(request):
    socios = Socio.objects.all()
    return render(request, 'ginasio/socio_list.html', {'socios': socios})

@admin_required
def socio_detail(request, pk):
    socio = get_object_or_404(Socio, pk=pk)
    pagamentos_socio = Pagamento.objects.filter(socio=socio).order_by('-data_vencimento') # Corrigido para data_vencimento
    return render(request, 'ginasio/socio_detail.html', {'socio': socio, 'pagamentos': pagamentos_socio})

@admin_required
def socio_create(request):
    if request.method == 'POST':
        form = SocioForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('socio_list')
    else:
        form = SocioForm()
    return render(request, 'ginasio/socio_form.html', {'form': form})

@admin_required
def socio_update(request, pk):
    socio = get_object_or_404(Socio, pk=pk)
    if request.method == 'POST':
        form = SocioForm(request.POST, request.FILES, instance=socio)
        if form.is_valid():
            form.save()
            return redirect('socio_detail', pk=socio.pk)
    else:
        form = SocioForm(instance=socio)
    return render(request, 'ginasio/socio_form.html', {'form': form, 'socio': socio})

@admin_required
def socio_delete(request, pk):
    socio = get_object_or_404(Socio, pk=pk)
    if request.method == 'POST':
        socio.delete()
        return redirect('socio_list')
    return render(request, 'ginasio/socio_confirm_delete.html', {'socio': socio})

# --- TREINADORES ---
@admin_required
def treinador_list(request):
    treinadores = Treinador.objects.all()
    return render(request, 'ginasio/treinador_list.html', {'treinadores': treinadores})

@admin_required
def treinador_detail(request, pk):
    treinador = get_object_or_404(Treinador, pk=pk)
    return render(request, 'ginasio/treinador_detail.html', {'treinador': treinador})

@admin_required
def treinador_create(request):
    if request.method == 'POST':
        form = TreinadorForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('treinador_list')
    else:
        form = TreinadorForm()
    return render(request, 'ginasio/treinador_form.html', {'form': form})

@admin_required
def treinador_update(request, pk):
    treinador = get_object_or_404(Treinador, pk=pk)
    if request.method == 'POST':
        form = TreinadorForm(request.POST, request.FILES, instance=treinador)
        if form.is_valid():
            form.save()
            return redirect('treinador_detail', pk=treinador.pk)
    else:
        form = TreinadorForm(instance=treinador)
    return render(request, 'ginasio/treinador_form.html', {'form': form, 'treinador': treinador})

@admin_required
def treinador_delete(request, pk):
    treinador = get_object_or_404(Treinador, pk=pk)
    if request.method == 'POST':
        treinador.delete()
        return redirect('treinador_list')
    return render(request, 'ginasio/treinador_confirm_delete.html', {'treinador': treinador})

# --- MODALIDADES ---
@admin_required
def modalidade_list(request):
    modalidades = Modalidade.objects.all()
    return render(request, 'ginasio/modalidade_list.html', {'modalidades': modalidades})

@admin_required
def modalidade_detail(request, pk):
    modalidade = get_object_or_404(Modalidade, pk=pk)
    return render(request, 'ginasio/modalidade_detail.html', {'modalidade': modalidade})

@admin_required
def modalidade_create(request):
    if request.method == 'POST':
        form = ModalidadeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('modalidade_list')
    else:
        form = ModalidadeForm()
    return render(request, 'ginasio/modalidade_form.html', {'form': form})

@admin_required
def modalidade_update(request, pk):
    modalidade = get_object_or_404(Modalidade, pk=pk)
    if request.method == 'POST':
        form = ModalidadeForm(request.POST, instance=modalidade)
        if form.is_valid():
            form.save()
            return redirect('modalidade_detail', pk=modalidade.pk)
    else:
        form = ModalidadeForm(instance=modalidade)
    return render(request, 'ginasio/modalidade_form.html', {'form': form, 'modalidade': modalidade})

@admin_required
def modalidade_delete(request, pk):
    modalidade = get_object_or_404(Modalidade, pk=pk)
    if request.method == 'POST':
        modalidade.delete()
        return redirect('modalidade_list')
    return render(request, 'ginasio/modalidade_confirm_delete.html', {'modalidade': modalidade})

# --- AULAS ---
@admin_required
def aula_list(request):
    aulas = Aulas.objects.all().order_by('data', 'hora')
    return render(request, 'ginasio/aula_list.html', {'aulas': aulas})

@admin_required
def aula_detail(request, pk):
    aula = get_object_or_404(Aulas, pk=pk)
    # MAGIA: Vamos buscar todas as inscrições que pertencem SÓ a esta aula!
    inscricoes_da_aula = Inscricao.objects.filter(aula=aula)
    
    return render(request, 'ginasio/aula_detail.html', {
        'aula': aula, 
        'inscricoes': inscricoes_da_aula  # Enviamos a lista para o HTML
    })

@admin_required
def aula_create(request):
    if request.method == 'POST':
        form = AulasForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('aula_list')
    else:
        form = AulasForm()
    return render(request, 'ginasio/aula_form.html', {'form': form})

@admin_required
def aula_update(request, pk):
    aula = get_object_or_404(Aulas, pk=pk)
    if request.method == 'POST':
        form = AulasForm(request.POST, instance=aula)
        if form.is_valid():
            form.save()
            return redirect('aula_detail', pk=aula.pk)
    else:
        form = AulasForm(instance=aula)
    return render(request, 'ginasio/aula_form.html', {'form': form, 'aula': aula})

@admin_required
def aula_delete(request, pk):
    aula = get_object_or_404(Aulas, pk=pk)
    if request.method == 'POST':
        aula.delete()
        return redirect('aula_list')
    return render(request, 'ginasio/aula_confirm_delete.html', {'aula': aula})

# --- INSCRIÇÕES ---
@admin_required
def inscricao_list(request):
    inscricoes = Inscricao.objects.all().order_by('-dataRegisto')
    return render(request, 'ginasio/inscricao_list.html', {'inscricoes': inscricoes})

@admin_required
def inscricao_detail(request, pk):
    inscricao = get_object_or_404(Inscricao, pk=pk)
    return render(request, 'ginasio/inscricao_detail.html', {'inscricao': inscricao})

@admin_required
def inscricao_create(request):
    if request.method == 'POST':
        form = InscricaoForm(request.POST)
        if form.is_valid():
            # MAGIA ANTI-DUPLICADOS: Verificamos quem é o sócio e qual é a aula antes de gravar!
            socio_escolhido = form.cleaned_data.get('socio')
            aula_escolhida = form.cleaned_data.get('aula')
            
            ja_existe = Inscricao.objects.filter(socio=socio_escolhido, aula=aula_escolhida).exists()
            
            if ja_existe:
                # Se já existe, bloqueamos a gravação e atiramos um erro ao Administrador!
                messages.error(request, f'Erro: O sócio {socio_escolhido.nome} já se encontra inscrito nesta aula!')
                return render(request, 'ginasio/inscricao_form.html', {'form': form})
            else:
                # Se não existe, gravamos com sucesso!
                form.save()
                messages.success(request, 'Inscrição registada com sucesso!')
                return redirect('inscricao_list')
    else:
        form = InscricaoForm()
        
    return render(request, 'ginasio/inscricao_form.html', {'form': form})

@admin_required
def inscricao_update(request, pk):
    inscricao = get_object_or_404(Inscricao, pk=pk)
    if request.method == 'POST':
        form = InscricaoForm(request.POST, instance=inscricao)
        if form.is_valid():
            form.save()
            return redirect('inscricao_detail', pk=inscricao.pk)
    else:
        form = InscricaoForm(instance=inscricao)
    return render(request, 'ginasio/inscricao_form.html', {'form': form, 'inscricao': inscricao})

@login_required
def inscricao_delete(request, pk):
    inscricao = get_object_or_404(Inscricao, pk=pk)

    if not request.user.is_superuser:
        if not hasattr(request.user, 'socio') or inscricao.socio_id != request.user.socio.id:
            return redirect('redirecionar_login')
    
    # Guardamos o ID da aula antes de a apagar, para sabermos para onde voltar
    aula_id = inscricao.aula.pk 
    
    if request.method == 'POST':
        inscricao.delete()
        
        # MAGIA DE REDIRECIONAMENTO INTELIGENTE:
        if request.user.is_superuser:
            # Se fores tu (Admin) a remover a pessoa, voltas para a página da Aula
            return redirect('aula_detail', pk=aula_id)
        else:
            # Se for o próprio Sócio a cancelar a sua aula, volta para a Área de Cliente
            return redirect('perfil_cliente')
            
    return render(request, 'ginasio/inscricao_confirm_delete.html', {'inscricao': inscricao})

# --- PLANOS DE TREINO ---
@admin_required
def planotreino_list(request):
    planos = PlanoTreino.objects.all().order_by('-data_inicio')
    return render(request, 'ginasio/planotreino_list.html', {'planos': planos})

@admin_required
def planotreino_detail(request, pk):
    plano = get_object_or_404(PlanoTreino, pk=pk)
    exercicios_do_plano = Exercicio.objects.filter(planoTreino=plano)
    return render(request, 'ginasio/planotreino_detail.html', {'plano': plano, 'exercicios': exercicios_do_plano})

@admin_required
def planotreino_create(request):
    if request.method == 'POST':
        form = PlanoTreinoForm(request.POST)
        if form.is_valid():
            plano = form.save()
            return redirect('planotreino_detail', pk=plano.pk)
    else:
        form = PlanoTreinoForm()
    return render(request, 'ginasio/planotreino_form.html', {'form': form})

@admin_required
def planotreino_update(request, pk):
    plano = get_object_or_404(PlanoTreino, pk=pk)
    if request.method == 'POST':
        form = PlanoTreinoForm(request.POST, instance=plano)
        if form.is_valid():
            form.save()
            return redirect('planotreino_detail', pk=plano.pk)
    else:
        form = PlanoTreinoForm(instance=plano)
    return render(request, 'ginasio/planotreino_form.html', {'form': form, 'plano': plano})

@admin_required
def planotreino_delete(request, pk):
    plano = get_object_or_404(PlanoTreino, pk=pk)
    if request.method == 'POST':
        plano.delete()
        return redirect('planotreino_list')
    return render(request, 'ginasio/planotreino_confirm_delete.html', {'plano': plano})

# --- EXERCÍCIOS ---
@admin_required
def exercicio_list(request):
    exercicios = Exercicio.objects.all()
    return render(request, 'ginasio/exercicio_list.html', {'exercicios': exercicios})

@admin_required
def exercicio_detail(request, pk):
    exercicio = get_object_or_404(Exercicio, pk=pk)
    return render(request, 'ginasio/exercicio_detail.html', {'exercicio': exercicio})

@admin_required
def exercicio_create(request):
    if request.method == 'POST':
        form = ExercicioForm(request.POST)
        if form.is_valid():
            exercicio = form.save()
            return redirect('planotreino_detail', pk=exercicio.planoTreino.pk)
    else:
        plano_id = request.GET.get('plano', None)
        if plano_id:
            form = ExercicioForm(initial={'planoTreino': plano_id})
        else:
            form = ExercicioForm()
    return render(request, 'ginasio/exercicio_form.html', {'form': form})

@admin_required
def exercicio_update(request, pk):
    exercicio = get_object_or_404(Exercicio, pk=pk)
    if request.method == 'POST':
        form = ExercicioForm(request.POST, instance=exercicio)
        if form.is_valid():
            form.save()
            return redirect('planotreino_detail', pk=exercicio.planoTreino.pk)
    else:
        form = ExercicioForm(instance=exercicio)
    return render(request, 'ginasio/exercicio_form.html', {'form': form, 'exercicio': exercicio})

@admin_required
def exercicio_delete(request, pk):
    exercicio = get_object_or_404(Exercicio, pk=pk)
    if request.method == 'POST':
        plano_id = exercicio.planoTreino.pk
        exercicio.delete()
        return redirect('planotreino_detail', pk=plano_id)
    return render(request, 'ginasio/exercicio_confirm_delete.html', {'exercicio': exercicio})

# --- PAGAMENTOS ---
@admin_required
def pagamento_list(request):
    hoje = date.today()
    Pagamento.objects.filter(estado='Pendente', data_vencimento__lt=hoje).update(estado='Atrasado')
    pagamentos = Pagamento.objects.all().order_by('-data_vencimento')
    return render(request, 'ginasio/pagamento_list.html', {'pagamentos': pagamentos})

@admin_required
def pagamento_detail(request, pk):
    pagamento = get_object_or_404(Pagamento, pk=pk)
    return render(request, 'ginasio/pagamento_detail.html', {'pagamento': pagamento})

@admin_required
def pagamento_create(request):
    if request.method == 'POST':
        form = PagamentoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('pagamento_list')
    else:
        form = PagamentoForm()
    return render(request, 'ginasio/pagamento_form.html', {'form': form})

@admin_required
def pagamento_update(request, pk):
    pagamento = get_object_or_404(Pagamento, pk=pk)
    estado_anterior = pagamento.estado
    
    if request.method == 'POST':
        form = PagamentoForm(request.POST, instance=pagamento)
        if form.is_valid():
            pagamento_guardado = form.save()
            
            # Se a fatura foi paga agora, gera a do próximo mês
            if estado_anterior != 'Liquidado' and pagamento_guardado.estado == 'Liquidado' and pagamento_guardado.frequencia == 'Mensal':
                nova_data_vencimento = pagamento_guardado.data_vencimento + timedelta(days=30)
                Pagamento.objects.create(
                    socio=pagamento_guardado.socio,
                    valor=pagamento_guardado.valor,
                    data_vencimento=nova_data_vencimento,
                    data_pago=date.today(), # <-- A CORREÇÃO ESTÁ AQUI TAMBÉM
                    estado='Pendente',
                    frequencia='Mensal'
                )
            return redirect('pagamento_list')
    else:
        form = PagamentoForm(instance=pagamento)
    
    return render(request, 'ginasio/pagamento_form.html', {'form': form, 'pagamento': pagamento})

@admin_required
def pagamento_delete(request, pk):
    pagamento = get_object_or_404(Pagamento, pk=pk)
    if request.method == 'POST':
        pagamento.delete()
        return redirect('pagamento_list')
    return render(request, 'ginasio/pagamento_confirm_delete.html', {'pagamento': pagamento})


# --- SISTEMA DE CONTAS E LOGIN ---

@login_required
def redirecionar_login(request):
    """
    Porta Inteligente: Avalia quem fez login e manda para o sítio certo.
    """
    if request.user.is_superuser:
        return redirect('index')
    elif hasattr(request.user, 'treinador'):
        return redirect('perfil_treinador') # Se for Treinador, vai para o dashboard dele
    else:
        return redirect('perfil_cliente') # Se for Sócio, vai para o perfil de cliente

@login_required
def perfil_treinador(request):
    """
    Dashboard exclusivo do Treinador. Mostra as suas aulas agendadas.
    """
    if hasattr(request.user, 'treinador'):
        treinador = request.user.treinador
        
        # Vai buscar apenas as aulas em que este treinador é o professor
        minhas_aulas = Aulas.objects.filter(treinador=treinador).order_by('data', 'hora')
        
        context = {
            'treinador': treinador,
            'minhas_aulas': minhas_aulas,
        }
        return render(request, 'ginasio/perfil_treinador.html', context)
    else:
        return redirect('redirecionar_login')

def registo_socio(request):
    """
    Função para o cliente se "Tornar Sócio".
    Inclui Faturação Automática na adesão e Upload de Fotografia!
    """
    if request.method == 'POST':
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        data_nascimento = request.POST.get('data_nascimento')
        telefone_inserido = request.POST.get('telefone')
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # MAGIA DA FOTO: Apanha o ficheiro enviado pelo HTML
        foto_inserida = request.FILES.get('foto') 
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Esse Nome de Utilizador já está em uso. Por favor, escolhe outro.')
            return render(request, 'ginasio/registo.html')
            
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Esse Email já está registado no nosso sistema. Tenta fazer login.')
            return render(request, 'ginasio/registo.html')
        
        user = User.objects.create_user(username=username, email=email, password=password)
        
        try:
            # 1. Cria a ficha de Sócio com a FOTO
            novo_socio = Socio.objects.create(
                user=user,
                nome=nome,
                email=email,
                contacto=telefone_inserido,
                dataNascimento=data_nascimento,
                dataAdesao=date.today(),
                foto=foto_inserida  # <-- GUARDA A FOTO AQUI
            )
            
            # 2. Faturação Automática Segura (com data_pago preenchida)
            Pagamento.objects.create(
                socio=novo_socio,
                valor=35.00, 
                data_vencimento=date.today() + timedelta(days=5),
                data_pago=date.today(),
                estado='Pendente',
                frequencia='Mensal'
            )
            
        except Exception as e:
            user.delete()
            messages.error(request, f'Erro na Base de Dados ao criar Sócio: {e}')
            return render(request, 'ginasio/registo.html')
        
        login(request, user)
        return redirect('perfil_cliente')

    return render(request, 'ginasio/registo.html')

@login_required
def perfil_cliente(request):
    """
    Dashboard do Sócio. Mostra Aulas, Faturas, Plano de Treino e Passe QR Code!
    """
    if hasattr(request.user, 'socio'):
        socio = request.user.socio
        
        # --- MAGIA DO QR CODE ---
        # Criamos o conteúdo do QR (ID do sócio)
        qr_data = f"SOCIO_ID:{socio.id}" 
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(qr_data)
        qr.make(fit=True)
        
        # Transforma o QR numa imagem que o HTML consegue ler via Base64
        img = qr.make_image(fill_color="black", back_color="white")
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        qr_base64 = base64.b64encode(buffer.getvalue()).decode()
        # ------------------------

        # Lógica de Inscrição em Aulas (POST)
        if request.method == 'POST':
            aula_id = request.POST.get('aula_id')
            if aula_id:
                ja_inscrito = Inscricao.objects.filter(socio=socio, aula_id=aula_id).exists()
                if ja_inscrito:
                    messages.warning(request, 'Já estás inscrito nesta aula!')
                else:
                    Inscricao.objects.create(socio=socio, aula_id=aula_id)
                    messages.success(request, 'Inscrição realizada com sucesso! Bom treino!')
                return redirect('perfil_cliente')

        # Dados para o Dashboard
        inscricoes = Inscricao.objects.filter(socio=socio)
        pagamentos = Pagamento.objects.filter(socio=socio).order_by('-data_vencimento')
        
        from .models import Aulas 
        aulas_disponiveis = Aulas.objects.all()
        
        # --- MAGIA DO PLANO DE TREINO ---
        try:
            plano_atual = PlanoTreino.objects.filter(socio=socio).order_by('-data_inicio').first()
            if plano_atual:
                exercicios_do_plano = Exercicio.objects.filter(planoTreino=plano_atual)
            else:
                exercicios_do_plano = []
        except:
            plano_atual = None
            exercicios_do_plano = []
        # --------------------------------
        
        context = {
            'socio': socio,
            'inscricoes': inscricoes,
            'pagamentos': pagamentos,
            'aulas_disponiveis': aulas_disponiveis,
            'plano_atual': plano_atual,
            'exercicios': exercicios_do_plano,
            'qr_code': qr_base64, # Enviamos a imagem codificada para o template
        }
        return render(request, 'ginasio/perfil_cliente.html', context)
    else:
        # Redirecionamento inteligente conforme o tipo de conta
        if request.user.is_superuser:
            return redirect('index')
        elif hasattr(request.user, 'treinador'):
            return redirect('perfil_treinador')
        else:
            messages.error(request, 'A tua conta de login existe, mas o teu Perfil de Sócio está incompleto. Por favor, contacta a nossa equipa.')
            return redirect('landing')
        
@login_required
def gestao_acessos(request):
    """
    Central de Gestão de Acessos: Cria Admins, Staff, Associa Sócios ou Apaga Contas.
    """
    if not request.user.is_superuser:
        return redirect('perfil_cliente')

    # Dados para as opções do formulário
    treinadores_sem_conta = Treinador.objects.filter(user__isnull=True)
    socios_sem_conta = Socio.objects.filter(user__isnull=True)
    # Lista de utilizadores que podem ser apagados (exclui superusers por segurança)
    utilizadores_comuns = User.objects.filter(is_superuser=False).order_by('username')

    if request.method == 'POST':
        tipo_conta = request.POST.get('tipo_conta') 

        # --- NOVA LÓGICA: APAGAR UTILIZADOR ---
        if tipo_conta == 'apagar_utilizador':
            user_id = request.POST.get('user_id')
            try:
                user_a_apagar = User.objects.get(pk=user_id)
                nome_apagado = user_a_apagar.username
                user_a_apagar.delete()
                messages.success(request, f'Conta de acesso "{nome_apagado}" eliminada com sucesso!')
            except User.DoesNotExist:
                messages.error(request, 'Utilizador não encontrado.')
            return redirect('gestao_acessos')

        # --- LÓGICA: RESET DE PASSWORD ---
        if tipo_conta == 'reset_password':
            user_id = request.POST.get('reset_user_id')
            nova_password = request.POST.get('nova_password')
            if not nova_password:
                messages.error(request, 'Indica a nova palavra-passe.')
                return redirect('gestao_acessos')

            try:
                user_a_alterar = User.objects.get(pk=user_id, is_superuser=False)
                user_a_alterar.set_password(nova_password)
                user_a_alterar.save()
                messages.success(request, f'Palavra-passe de "{user_a_alterar.username}" alterada com sucesso!')
            except (User.DoesNotExist, ValueError):
                messages.error(request, 'Utilizador nao encontrado.')
            return redirect('gestao_acessos')

        # --- LÓGICA EXISTENTE: CRIAR CONTAS ---
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Este Nome de Utilizador já está em uso.')
            return redirect('gestao_acessos')
            
        if email and User.objects.filter(email=email).exists():
            messages.error(request, 'Este Email já está associado a outra conta.')
            return redirect('gestao_acessos')

        try:
            user = User.objects.create_user(username=username, email=email, password=password)

            if tipo_conta == 'admin':
                user.is_superuser = True 
                user.is_staff = True
                user.save()
                messages.success(request, f'Conta de Administrador ({username}) criada com sucesso!')

            elif tipo_conta == 'treinador_existente':
                treinador_id = request.POST.get('treinador_id')
                treinador = get_object_or_404(Treinador, pk=treinador_id)
                treinador.user = user 
                treinador.save()
                messages.success(request, f'Acesso criado e associado ao treinador {treinador.nome}!')

            elif tipo_conta == 'treinador_novo':
                nome = request.POST.get('nome_treinador')
                especialidade = request.POST.get('especialidade')
                foto = request.FILES.get('foto')
                Treinador.objects.create(user=user, nome=nome, especialidade=especialidade, foto=foto)
                messages.success(request, 'Novo Treinador e respetiva conta criados com sucesso!')
                
            elif tipo_conta == 'socio_existente':
                socio_id = request.POST.get('socio_id')
                socio = get_object_or_404(Socio, pk=socio_id)
                socio.user = user 
                socio.save()
                messages.success(request, f'Acesso criado e devolvido ao sócio {socio.nome}!')

        except Exception as e:
            if 'user' in locals() and user.id:
                user.delete()
            messages.error(request, f'Erro ao processar o pedido: {e}')

        return redirect('gestao_acessos')

    context = {
        'treinadores_sem_conta': treinadores_sem_conta,
        'socios_sem_conta': socios_sem_conta,
        'utilizadores_comuns': utilizadores_comuns,
    }
    return render(request, 'ginasio/gestao_acessos.html', context)
