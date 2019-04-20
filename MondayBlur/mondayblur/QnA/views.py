from django.shortcuts import render,get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import question,comment
from django.contrib.auth.models import User
from .forms import *
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



    





