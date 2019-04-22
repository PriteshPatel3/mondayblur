from django.shortcuts import render,get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import question,comment
from.forms import CommentForm
from django.contrib.auth.models import User
from django.views.generic import ListView,TemplateView,DetailView,CreateView

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

class CommentCreateView(LoginRequiredMixin, CreateView):
	model = comment
	fields = ['comment','question']

	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)
		


    





