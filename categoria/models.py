from django.db import models
from django.urls import reverse
class Categoria(models.Model):
    categoria_nome = models.CharField(max_length=80, unique=True)
    slug= models.SlugField(max_length=200, unique=True, null=True)
    categoria_descrição = models.TextField(max_length=255, blank=True)
    categoria_imagem =models.ImageField(upload_to='fotos/categorias', blank=True)
    
    def __str__(self):
        return self.categoria_nome
    def get_url(self):
        return reverse('produtos_por_categoria', args=[self.slug])
    
    
# Create your models here.
