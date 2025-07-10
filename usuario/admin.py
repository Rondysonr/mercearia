from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import PerfilUsuario

# Inline para mostrar o perfil junto com o usuário
class PerfilUsuarioInline(admin.StackedInline):
    model = PerfilUsuario
    can_delete = False
    verbose_name_plural = 'Perfil'

# Customizar o admin do User
class CustomUserAdmin(UserAdmin):
    inlines = (PerfilUsuarioInline,)

# Re-registrar o User com as customizações
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

# Registrar o PerfilUsuario separadamente também
admin.site.register(PerfilUsuario)