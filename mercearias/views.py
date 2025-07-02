from django.shortcuts import render

from produtos.models import Produto

def visualizarHome(request):
    produtos = Produto.objects.all().filter(disponivel=True)
    context= {
        'produtos': produtos,
    }
    return render(request, 'home.html', context)
    #return render(request, 'carrinho.html')