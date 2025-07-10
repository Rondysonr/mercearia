from django.shortcuts import get_object_or_404, render
from django.http import Http404, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import json
import time

from categoria.models import Categoria
from produtos.models import Produto
from carrinhos.models import CarItem  # Usar CarItem em vez de ItemCarrinho

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
    """View para exibir a página de bolo personalizado"""
    try:
        # Buscar produtos por categoria usando slug
        massas = Produto.objects.filter(categoria__slug='massas', disponivel=True)
        recheios = Produto.objects.filter(categoria__slug='recheios', disponivel=True)
        coberturas = Produto.objects.filter(categoria__slug='coberturas', disponivel=True)
        enfeites = Produto.objects.filter(categoria__slug='enfeites', disponivel=True)
        formatos = Produto.objects.filter(categoria__slug='formatos', disponivel=True)
        
        context = {
            'massas': massas,
            'recheios': recheios,
            'coberturas': coberturas,
            'enfeites': enfeites,
            'formatos': formatos,
        }
        
        return render(request, 'loja/bolo_personalizados.html', context)
    
    except Exception as e:
        # Se houver erro, retornar página com contexto vazio
        context = {
            'massas': [],
            'recheios': [],
            'coberturas': [],
            'enfeites': [],
            'formatos': [],
            'erro': 'Erro ao carregar opções de personalização'
        }
        return render(request, 'loja/bolo_personalizados.html', context)

@login_required
def adicionar_bolo_personalizado(request):
    """View para adicionar bolo personalizado ao carrinho"""
    if request.method == 'POST':
        try:
            # Obter dados do formulário
            formato_slug = request.POST.get('formato')
            massa_slug = request.POST.get('massa')
            recheio_slug = request.POST.get('recheio')
            cobertura_slug = request.POST.get('cobertura')
            enfeite_slug = request.POST.get('enfeite', '')
            peso = float(request.POST.get('peso', 0))
            preco_total = float(request.POST.get('preco_total', 0))
            observacoes = request.POST.get('observacoes', '')
            
            # Validar dados obrigatórios
            if not all([formato_slug, massa_slug, recheio_slug, cobertura_slug]) or peso < 0.5:
                return JsonResponse({
                    'success': False,
                    'message': 'Todos os campos obrigatórios devem ser preenchidos'
                })
            
            # Buscar produtos
            try:
                formato = Produto.objects.get(slug=formato_slug)
                massa = Produto.objects.get(slug=massa_slug)
                recheio = Produto.objects.get(slug=recheio_slug)
                cobertura = Produto.objects.get(slug=cobertura_slug)
                enfeite = None
                if enfeite_slug:
                    enfeite = Produto.objects.get(slug=enfeite_slug)
            except Produto.DoesNotExist:
                return JsonResponse({
                    'success': False,
                    'message': 'Produto não encontrado'
                })
            
            # Criar descrição do bolo personalizado
            descricao = f"Bolo Personalizado - {peso}kg\n"
            descricao += f"Formato: {formato.produto_nome}\n"
            descricao += f"Massa: {massa.produto_nome}\n"
            descricao += f"Recheio: {recheio.produto_nome}\n"
            descricao += f"Cobertura: {cobertura.produto_nome}\n"
            if enfeite:
                descricao += f"Enfeite: {enfeite.produto_nome}\n"
            if observacoes:
                descricao += f"Observações: {observacoes}\n"
            
            # Adicionar ao carrinho
            carrinho_id = _obter_carrinho_id(request)
            
            # Obter ou criar o carrinho
            try:
                from carrinhos.models import Carrinho
                carrinho = Carrinho.objects.get(car_id=carrinho_id)
            except Carrinho.DoesNotExist:
                carrinho = Carrinho.objects.create(car_id=carrinho_id)
            
            # Criar novo item no carrinho para bolo personalizado
            CarItem.objects.create(
                carrinho=carrinho,  # Associar ao carrinho
                produto=None,  # Bolo personalizado não tem produto fixo
                user=request.user if request.user.is_authenticated else None,
                quantidade=1,
                preco_unitario=preco_total,
                dados_personalizacao=json.dumps({
                    'formato': formato.produto_nome,
                    'massa': massa.produto_nome,
                    'recheio': recheio.produto_nome,
                    'cobertura': cobertura.produto_nome,
                    'enfeite': enfeite.produto_nome if enfeite else '',
                    'peso': peso,
                    'observacoes': observacoes,
                    'descricao': descricao,
                    'nome': f'Bolo Personalizado {peso}kg',
                    'tipo': 'bolo_personalizado'
                })
            )
            
            return JsonResponse({
                'success': True,
                'message': 'Bolo personalizado adicionado ao carrinho com sucesso!'
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'Erro interno: {str(e)}'
            })
    
    return JsonResponse({
        'success': False,
        'message': 'Método não permitido'
    })

def _obter_carrinho_id(request):
    """Função auxiliar para obter o ID do carrinho"""
    carrinho_id = request.session.get('carrinho_id')
    if not carrinho_id:
        carrinho_id = request.session.session_key
        if not carrinho_id:
            request.session.create()
            carrinho_id = request.session.session_key
        request.session['carrinho_id'] = carrinho_id
    return carrinho_id