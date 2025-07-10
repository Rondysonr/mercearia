from django.db import models
from django.contrib.auth.models import User

# Estender o modelo User padrão com um Profile
class PerfilUsuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20, blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=2, blank=True)
    gender = models.CharField(max_length=1, choices=[('M', 'Masculino'), ('F', 'Feminino')], blank=True)
    
    def __str__(self):
        return f"Perfil de {self.user.first_name} {self.user.last_name}"
    
    class Meta:
        verbose_name = 'Perfil do Usuário'
        verbose_name_plural = 'Perfis dos Usuários'