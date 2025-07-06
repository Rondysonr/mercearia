from django.contrib import admin

from carrinhos.models import CarItem, Carrinho

class CarrinhoAdmin(admin.ModelAdmin):
    list_display = ('car_id', 'data_adicionado')
    

class CarItemAdmin(admin.ModelAdmin):
    list_display = ('carrinho', 'produto', 'quantidade',)
    

admin.site.register(Carrinho, CarrinhoAdmin)
admin.site.register(CarItem, CarItemAdmin)
