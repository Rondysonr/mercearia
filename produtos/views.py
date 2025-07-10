from django.shortcuts import get_object_or_404, render
from django.http import Http404

from categoria.models import Categoria
from produtos.models import Produto

# Create your views here.
def visualizarLoja(request, categoria_slug=None):
    categorias = None
    produtos = None
    
    if categoria_slug != None:
        categorias = get_object_or_404(Categoria, slug=categoria_slug)
        produtos = Produto.objects.filter(categoria=categorias, disponivel=True)
        produtos_quant = produtos.count()
    else:
        produtos = Produto.objects.all().filter(disponivel=True)
        produtos_quant = produtos.count()
    
    context = {
        'produtos': produtos,
        'produtos_quant': produtos_quant,
    }
    
    return render(request, 'loja/loja.html', context)

def produto_detalhe(request, categoria_slug, produto_slug):
    try:
        produto = Produto.objects.get(categoria__slug=categoria_slug, slug=produto_slug)
    except Exception as e: 
        raise Http404('Produto não encontrado')
    
    context = {
        'produto': produto,
    }
    return render(request, 'loja/produto_detalhe.html', context)

def bolo_personalizado(request):
    massas = Produto.objects.filter(categoria__slug='massas')
    recheios = Produto.objects.filter(categoria__slug='recheios')
    coberturas = Produto.objects.filter(categoria__slug='coberturas')
    enfeites = Produto.objects.filter(categoria__slug='enfeites')
    formatos = Produto.objects.filter(categoria__slug='formatos')
    
    context = {
        'massas': massas,
        'recheios': recheios,
        'coberturas': coberturas,
        'enfeites': enfeites,
        'formatos': formatos,
    }
    
    return render(request, 'loja/bolo_personalizados.html', context)