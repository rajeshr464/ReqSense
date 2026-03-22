from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from .forms import UserRegisterForm, UserProfileForm

def register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful.')
            return redirect('dashboard:index')
        messages.error(request, 'Unsuccessful registration. Invalid information.')
    else:
        form = UserRegisterForm()
    return render(request, 'accounts/register.html', {'form': form})

@never_cache
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f'You are now logged in as {username}.')
                return redirect('dashboard:index')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

@never_cache
def logout_view(request):
    # Clear existing messages before logging out the user
    storage = messages.get_messages(request)
    storage.used = True
    
    logout(request)
    messages.info(request, 'You have successfully logged out.')
    return redirect('accounts:login')

def forgot_password_view(request):
    if request.method == 'POST':
        messages.success(request, 'If an account matches that email, a standard reset link has been dispatched to your inbox.')
        return redirect('accounts:login')
    return render(request, 'accounts/forgot_password.html')

@login_required
def profile_view(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('accounts:profile')
    else:
        form = UserProfileForm(instance=request.user)
    return render(request, 'accounts/profile.html', {'form': form})
