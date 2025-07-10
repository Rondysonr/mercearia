from django.urls import path
from . import views

urlpatterns = [
    path('', views.visualizarLoja, name='loja'),
    path('bolo-personalizado/', views.bolo_personalizado, name='bolo_personalizado'),
    path('<slug:categoria_slug>/', views.visualizarLoja, name='produtos_por_categoria'),
    path('<slug:categoria_slug>/<slug:produto_slug>/', views.produto_detalhe, name='produto_detalhe'),
    # path('carrinho/', views.carrinho, name='carrinho'),
]