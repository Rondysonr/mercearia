from django.db import models
from decimal import Decimal
from django.contrib.auth.models import User
from produtos.models import Produto

class Carrinho(models.Model):
    car_id = models.CharField(max_length=250, blank=True)
    data_adicionado = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.car_id
    
    class Meta:
        verbose_name = 'Carrinho'
        verbose_name_plural = 'Carrinhos'

class CarItem(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE, null=True, blank=True)
    carrinho = models.ForeignKey(Carrinho, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    quantidade = models.IntegerField(default=1)
    preco_unitario = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    dados_personalizacao = models.TextField(blank=True, null=True)
    esta_disponivel = models.BooleanField(default=True)
    data_adicao = models.DateTimeField(auto_now_add=True)
    
    def subtotal(self):
        """Calcular subtotal do item"""
        if self.produto:
            return self.produto.preco * self.quantidade
        else:
            return self.preco_unitario * self.quantidade
    
    def __str__(self):
        if self.produto:
            return f"{self.produto.produto_nome} - Qtd: {self.quantidade}"
        else:
            return f"Bolo Personalizado - Qtd: {self.quantidade}"
    
    class Meta:
        verbose_name = "Item do Carrinho"
        verbose_name_plural = "Itens do Carrinho"

# Alias para compatibilidade
ItemCarrinho = CarItem