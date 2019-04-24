from django.shortcuts import render,get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import question,comment
from.forms import CommentForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.generic import ListView,TemplateView,DetailView,CreateView

def home(request):
    context={
        
    }
    return render(request, 'QnA/homepage.html',context)

class QuestionListView(ListView):
    model = question
    template_name = 'QnA/question.html'
    context_object_name = 'question'

class QuestionCreateView(CreateView):
    model = question
    fields = ['title','slug','content','category']

    def form_valid(self,form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class QuestionDetailView(DetailView):
    model = question

def add_comment(request,slug):
    post = get_object_or_404(question,slug=slug)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        form.instance.author = request.user
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            messages.success(request,f'You have successfully posted your comment!')
            return redirect('qna')
    else:
        form = CommentForm

    context ={
        'form':form
    }

    return render(request,'QnA/comment_form.html',context)


    
		


    





