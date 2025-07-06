from django.shortcuts import render

from carrinhos.models import CarItem, Carrinho
from produtos.models import Produto
def _getCarId(request):
    car = request.session.session_key
    if not car:
        car = request.session.create()
        return car
def visualizarCarrinho(request):
    return render(request, 'loja/carrinho.html',)
def adicionarItemCarrinho(request, produto_id):
    # Lógica para adicionar item ao carrinho
    prod = Produto.objects.get(id=produto_id)
    try:
        car = request.session(car_id= _getCarId(request))
    except Carrinho.DoesNotExist:
        car= Carrinho.objects.create(
            car_id = _getCarId(request)
        )
    carrinho.save()

    try:
        car_item = CarItem.objects.get(produto=produto, carrinho=car)
        car_item.quantidade += 1
    except CarItem.DoesNotExist:
        car_item = CarItem.objects.create(
            produto=prod,
            carrinho=car,
            quantidade=1
        )
        car_item.save()    
    return render(Carrinho)