from django.db import models
from decimal import Decimal
from produtos.models import Produto

class Carrinho(models.Model):
    car_id = models.CharField(max_length=250, blank=True)
    data_adicionado = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.car_id

class CarItem(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    carrinho = models.ForeignKey(Carrinho, on_delete=models.CASCADE, null=True)
    quantidade = models.IntegerField()
    esta_disponivel = models.BooleanField(default=True)
    
    def subtotal(self):
        """Calcula o subtotal do item (preço × quantidade)"""
        return self.produto.preco * Decimal(str(self.quantidade))
    
    def __str__(self):
        return f"{self.produto.produto_nome} - Qtd: {self.quantidade}"
    
    class Meta:
        verbose_name = "Item do Carrinho"
        verbose_name_plural = "Itens do Carrinho"