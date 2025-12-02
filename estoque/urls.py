from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # ROTAS DE AUTENTICAÇÃO
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    path('', views.dashboard, name='dashboard'),
    path('recalcular/', views.recalcular_estoque, name='recalcular_estoque'),
    path('movimentacao/', views.registrar_saida_rapida, name='registrar_saida_rapida'), # Nova rota
    path('historico/', views.historico_movimentacoes, name='historico'),
    path('exportar/', views.exportar_relatorio, name='exportar_relatorio'),
]