from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegisterForm, User
from QnA.models import question
from django.views.generic import ListView

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
    return render(request, 'users/register.html', {'form': form})


class ProfileListView(ListView):
    model = question
    template_name : 'users/profile.html'
    context_object_name = 'question'
    ordering = ['-date_published']
    paginate_by = 5      




