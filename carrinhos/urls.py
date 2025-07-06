from django.urls import include, path

from carrinhos import views
urlpatterns = [
    path('', views.visualizarCarrinho, name = 'carrinho'),
]