from django.contrib import admin

from categoria.models import Categoria

#from categoria.models import Categoria
class CategoriaAdmin(admin.ModelAdmin):
    prepopulated_fields ={
        'slug':('categoria_nome',)
    }
    list_display=('categoria_nome',)
admin.site.register(Categoria,CategoriaAdmin)
# Register your models here.
