from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from .models import PerfilUsuario

def registro_view(request):
    if request.method == 'POST':
        # Obter dados do formulário
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        gender = request.POST.get('gender')
        city = request.POST.get('city')
        state = request.POST.get('state')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        
        # Validações
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Este email já está cadastrado!')
            return render(request, 'users/registro.html')  # Corrigido para users/
        
        if password != confirm_password:
            messages.error(request, 'As senhas não coincidem!')
            return render(request, 'users/registro.html')  # Corrigido para users/
        
        try:
            validate_password(password)
        except ValidationError as e:
            for error in e.messages:
                messages.error(request, error)
            return render(request, 'users/registro.html')  # Corrigido para users/
        
        # Criar usuário
        try:
            user = User.objects.create_user(
                username=email,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )
            
            # Criar perfil do usuário
            PerfilUsuario.objects.create(
                user=user,
                phone_number=phone_number,
                gender=gender,
                city=city,
                state=state
            )
            
            messages.success(request, 'Conta criada com sucesso!')
            return redirect('login')
            
        except Exception as e:
            messages.error(request, 'Erro ao criar conta. Tente novamente.')
            return render(request, 'users/registro.html')  # Corrigido para users/
    
    return render(request, 'users/registro.html')  # Corrigido para users/

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        # Tentar autenticar
        user = authenticate(request, username=email, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Bem-vindo, {user.first_name}!')
            
            # Redirecionar para página anterior ou home
            next_url = request.GET.get('next')
            if next_url:
                return redirect(next_url)
            else:
                return redirect('loja')
        else:
            messages.error(request, 'Email ou senha incorretos!')
    
    return render(request, 'users/login.html')  # Corrigido para users/

def logout_view(request):
    logout(request)
    messages.success(request, 'Você saiu da sua conta.')
    return redirect('loja')

def perfil_view(request):
    if not request.user.is_authenticated:
        messages.error(request, 'Você precisa fazer login primeiro.')
        return redirect('login')
    
    # Criar perfil se não existir
    perfil, created = PerfilUsuario.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        # Atualizar dados do usuário
        user = request.user
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.email = request.POST.get('email', user.email)
        user.save()
        
        # Atualizar perfil
        perfil.phone_number = request.POST.get('phone_number', perfil.phone_number)
        perfil.city = request.POST.get('city', perfil.city)
        perfil.state = request.POST.get('state', perfil.state)
        perfil.gender = request.POST.get('gender', perfil.gender)
        perfil.save()
        
        messages.success(request, 'Perfil atualizado com sucesso!')
        return redirect('perfil')
    
    context = {
        'perfil': perfil
    }
    return render(request, 'users/perfil.html', context)  # Corrigido para users/