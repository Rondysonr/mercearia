from django.contrib import admin

from .models import Produto
class ProdutoAdmin(admin.ModelAdmin):
    prepopulated_fields = {
        'slug': ('produto_nome',)
    }
    list_display = ('produto_nome','slug')
# Register your models here.
admin.site.register(Produto, ProdutoAdmin)