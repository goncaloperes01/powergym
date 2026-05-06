from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # --- PÁGINA PRINCIPAL E DASHBOARD ---
    # Agora a página inicial vazia ('') vai para a landing page pública
    path('', views.landing_page, name='landing'),
    
    # O teu painel de administração passou para o caminho '/dashboard/'
    path('dashboard/', views.index, name='index'),
    
    # --- ROTAS DE AUTENTICAÇÃO ---
    path('login/', auth_views.LoginView.as_view(template_name='ginasio/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('registo/', views.registo_socio, name='registo_socio'),
    path('redirecionar/', views.redirecionar_login, name='redirecionar_login'),
    path('perfil/', views.perfil_cliente, name='perfil_cliente'),
    
    # --- ROTAS DE GESTÃO (SÓCIOS, EQUIPA, ETC) ---
    path('socios/', views.socio_list, name='socio_list'),
    path('socios/<int:pk>/', views.socio_detail, name='socio_detail'),
    path('socios/novo/', views.socio_create, name='socio_create'),
    path('socios/<int:pk>/editar/', views.socio_update, name='socio_update'),
    path('socios/<int:pk>/apagar/', views.socio_delete, name='socio_delete'),
    
    path('treinadores/', views.treinador_list, name='treinador_list'),
    path('treinadores/<int:pk>/', views.treinador_detail, name='treinador_detail'),
    path('treinadores/novo/', views.treinador_create, name='treinador_create'),
    path('treinadores/<int:pk>/editar/', views.treinador_update, name='treinador_update'),
    path('treinadores/<int:pk>/apagar/', views.treinador_delete, name='treinador_delete'),
    
    path('modalidades/', views.modalidade_list, name='modalidade_list'),
    path('modalidades/<int:pk>/', views.modalidade_detail, name='modalidade_detail'),
    path('modalidades/novo/', views.modalidade_create, name='modalidade_create'),
    path('modalidades/<int:pk>/editar/', views.modalidade_update, name='modalidade_update'),
    path('modalidades/<int:pk>/apagar/', views.modalidade_delete, name='modalidade_delete'),
    
    path('aulas/', views.aula_list, name='aula_list'),
    path('aulas/<int:pk>/', views.aula_detail, name='aula_detail'),
    path('aulas/novo/', views.aula_create, name='aula_create'),
    path('aulas/<int:pk>/editar/', views.aula_update, name='aula_update'),
    path('aulas/<int:pk>/apagar/', views.aula_delete, name='aula_delete'),
    
    path('inscricoes/', views.inscricao_list, name='inscricao_list'),
    path('inscricoes/<int:pk>/', views.inscricao_detail, name='inscricao_detail'),
    path('inscricoes/novo/', views.inscricao_create, name='inscricao_create'),
    path('inscricoes/<int:pk>/editar/', views.inscricao_update, name='inscricao_update'),
    path('inscricoes/<int:pk>/apagar/', views.inscricao_delete, name='inscricao_delete'),

    # ROTAS PARA PLANOS DE TREINO
    path('planos/', views.planotreino_list, name='planotreino_list'),
    path('planos/<int:pk>/', views.planotreino_detail, name='planotreino_detail'),
    path('planos/novo/', views.planotreino_create, name='planotreino_create'),
    path('planos/<int:pk>/editar/', views.planotreino_update, name='planotreino_update'),
    path('planos/<int:pk>/apagar/', views.planotreino_delete, name='planotreino_delete'),

    # ROTAS PARA EXERCÍCIOS
    path('exercicios/', views.exercicio_list, name='exercicio_list'),
    path('exercicios/<int:pk>/', views.exercicio_detail, name='exercicio_detail'),
    path('exercicios/novo/', views.exercicio_create, name='exercicio_create'),
    path('exercicios/<int:pk>/editar/', views.exercicio_update, name='exercicio_update'),
    path('exercicios/<int:pk>/apagar/', views.exercicio_delete, name='exercicio_delete'),

    # ROTAS PARA PAGAMENTOS
    path('pagamentos/', views.pagamento_list, name='pagamento_list'),
    path('pagamentos/novo/', views.pagamento_create, name='pagamento_create'),
    path('pagamentos/<int:pk>/', views.pagamento_detail, name='pagamento_detail'),
    path('pagamentos/<int:pk>/editar/', views.pagamento_update, name='pagamento_update'),
    path('pagamentos/<int:pk>/apagar/', views.pagamento_delete, name='pagamento_delete'),
    
    path('perfil-treinador/', views.perfil_treinador, name='perfil_treinador'),
    
    path('gestao-acessos/', views.gestao_acessos, name='gestao_acessos'),
]