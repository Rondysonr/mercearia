from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.visualizarCarrinho, name='carrinho'),
    path('adicionar/<int:produto_id>/', views.adicionarItemCarrinho, name='adicionarItemCarrinho'),
    path('remover/<int:produto_id>/', views.removerItemCarrinho, name='remover_carrinho'),
    path('diminuir/<int:produto_id>/', views.diminuirItemCarrinho, name='diminuir_carrinho'),
]