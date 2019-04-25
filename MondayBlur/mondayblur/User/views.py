from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegisterForm, User

def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save() #adds user to database
            username = form.cleaned_data.get('username')
            messages.success(request, f'Successfully created account: {username}. Please login!')
            return redirect("login")
    else:
        form = UserRegisterForm()
    return render(request, 'User/register.html', {'form': form})

def profile(request):
    if User.is_anonymous:
        messages.warning(request, f'Please login!')
        return redirect("login")
        
    return render(request, 'user/profile.html')


