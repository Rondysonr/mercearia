from django.shortcuts import render
def visualizarCarrinho(request):
    return render(request, 'loja/carrinho.html',)
