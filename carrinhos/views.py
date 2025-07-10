from django.shortcuts import redirect, render, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from decimal import Decimal

from carrinhos.models import CarItem, Carrinho
from produtos.models import Produto

def _getCarId(request):
    car = request.session.session_key
    if not car:
        request.session.create()
        car = request.session.session_key
    return car

def visualizarCarrinho(request, total=0, quantidade=0, car_items=None):
    try:
        car = Carrinho.objects.get(car_id=_getCarId(request))
        car_items = CarItem.objects.filter(carrinho=car, esta_disponivel=True)
        
        total = Decimal('0.00')
        
        for car_item in car_items:
            total += (car_item.produto.preco * car_item.quantidade)
            quantidade += car_item.quantidade
            
    except ObjectDoesNotExist:
        pass
    
    # Calcular taxa de 5% usando Decimal
    taxa = total * Decimal('0.05')
    total_geral = total + taxa
    
    context = {
        'total': total,
        'quantidade': quantidade,
        'car_items': car_items,
        'taxa': taxa,
        'total_geral': total_geral,
    }
    return render(request, 'loja/carrinho.html', context)

def adicionarItemCarrinho(request, produto_id):
    produto = get_object_or_404(Produto, id=produto_id)
    
    # Pegar a quantidade do formulário (padrão 1)
    quantidade = int(request.POST.get('quantidade', 1))
    
    try:
        car = Carrinho.objects.get(car_id=_getCarId(request))
    except Carrinho.DoesNotExist:
        car = Carrinho.objects.create(
            car_id=_getCarId(request)
        )
        car.save()

    try:
        car_item = CarItem.objects.get(produto=produto, carrinho=car)
        car_item.quantidade += quantidade
        car_item.save()
    except CarItem.DoesNotExist:
        car_item = CarItem.objects.create(
            produto=produto,
            carrinho=car,
            quantidade=quantidade
        )
        car_item.save()
    
    messages.success(request, f'{produto.produto_nome} adicionado ao carrinho!')
    return redirect('carrinho')

def removerItemCarrinho(request, produto_id):
    car = Carrinho.objects.get(car_id=_getCarId(request))
    produto = get_object_or_404(Produto, id=produto_id)
    
    try:
        car_item = CarItem.objects.get(produto=produto, carrinho=car)
        car_item.delete()
        messages.success(request, f'{produto.produto_nome} removido do carrinho!')
    except CarItem.DoesNotExist:
        messages.error(request, 'Item não encontrado no carrinho.')
    
    return redirect('carrinho')

def diminuirItemCarrinho(request, produto_id):
    car = Carrinho.objects.get(car_id=_getCarId(request))
    produto = get_object_or_404(Produto, id=produto_id)
    
    try:
        car_item = CarItem.objects.get(produto=produto, carrinho=car)
        if car_item.quantidade > 1:
            car_item.quantidade -= 1
            car_item.save()
        else:
            car_item.delete()
        messages.success(request, f'Quantidade de {produto.produto_nome} atualizada!')
    except CarItem.DoesNotExist:
        messages.error(request, 'Item não encontrado no carrinho.')
    
    return redirect('carrinho')