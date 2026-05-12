from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from .models import User

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        user_type = request.POST.get('user_type')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        
        if password1 != password2:
            messages.error(request, 'Les mots de passe ne correspondent pas')
            return redirect('register')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Ce nom existe déjà')
            return redirect('register')
        
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password1,
            user_type=user_type
        )
        if phone:
            user.phone = phone
        user.save()
        
        login(request, user)
        messages.success(request, f'Bienvenue {username}')
        return redirect('home')
    
    return render(request, 'accounts/register.html')
