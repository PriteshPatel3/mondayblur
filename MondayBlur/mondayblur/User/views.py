from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import UserRegisterForm

def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save() #adds user to database
            username = form.cleaned_data.get('username')
            messages.success(request, f'Successfully created for {username}!')
            return redirect("qna")
    else:
        form = UserRegisterForm()
    return render(request, 'User/register.html', {'form': form})


