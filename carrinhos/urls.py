from django.urls import include, path

from carrinhos import views
urlpatterns = [
    path('', views.visualizarCarrinho, name = 'carrinho'),
    path('adicionar_carrinho/<int:produto_id>',views.adicionarItemCarrinho, name = 'adicionarItemCarrinho'),
]