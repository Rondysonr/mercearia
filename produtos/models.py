from django.db import models

from categoria.models import Categoria

# Create your models here.
class Produto(models.Model):
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    produto_nome =models.CharField(max_length=200, unique=True)
    slug= models.SlugField(max_length=200, unique=True, null=True)# atributo que auxilia na criação da url, para acessar um produto
    descricao = models.TextField(max_length=300, unique=True)
    preco = models.DecimalField(max_digits=12, decimal_places=2)
    imagem = models.ImageField(upload_to='fotos/produtos', unique=True)
    estoque = models.IntegerField()
    disponivel = models.BooleanField(default=True)
    
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    def get_url(self):
        return reverse('produto_detalhe', args=[self.categoria_slug])