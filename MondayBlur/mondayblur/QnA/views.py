from django.shortcuts import render,get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import question,comment
from.forms import CommentForm
from django.contrib.auth.models import User
from django.views.generic import ListView,TemplateView,DetailView\

def home(request):
    context={
        
    }
    return render(request, 'QnA/homepage.html',context)

class QuestionListView(ListView):
    model = question
    template_name = 'QnA/question.html'
    context_object_name = 'question'


class QuestionDetailView(DetailView):
    model = question

def add_comment(request):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = CommentForm()
    context ={
        'form': form
    }
    
    return render(request,'QnA/add_comment',context)



    





