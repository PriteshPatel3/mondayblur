from django.shortcuts import render,get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from .models import question,comment
from.forms import CommentForm,SolutionForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.generic import ListView,TemplateView,DetailView,CreateView,UpdateView,DeleteView

def home(request):
    context={
        
    }
    return render(request, 'QnA/homepage.html',context)




class QuestionListView(ListView):
    model = question
    template_name = 'QnA/question.html'
    context_object_name = 'question'
    ordering = ['-date_published']
    paginate_by = 5


class QuestionDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
	model = question
	success_url ='/QnA/'

	def test_func(self):
		post = self.get_object()
		if self.request.user == post.author:
			return True
		return False

class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
	model = comment
	success_url = '/QnA/'

	def test_func(self):
		post = self.get_object()
		if self.request.user == post.author:
			return True
		return False

class QuestionCreateView(CreateView):
    model = question
    fields = ['title','slug','content','category']

    def form_valid(self,form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class QuestionDetailView(DetailView):
    model = question

class SolutionView(UpdateView):
    model = comment
    template_name = 'QnA/solution_form.html'
    fields = ['r_token']

    def form_valid(self,form):
        if form.instance.r_token == False:
            form.instance.r_token = True
        elif form.instance.r_token == True:
            form.instance.r_token = False
        return super().form_valid(form)

class QuestionUpdateView(UpdateView):
    model = question
    fields = ['title','content']
    
    def form_valid(self,form):
        form.instance.author = self.request.user
        return super().form_valid(form)        

def vote(request,pk):
    post = get_object_or_404(comment,pk=pk)
    if request.method == 'POST':
        if post.liked_by.filter(id=request.user.id).exists():
            post.liked_by.remove(request.user)
            post.like -= 1
            post.save()
        else:
            post.liked_by.add(request.user)
            post.like += 1
            post.save()
        return redirect('qna')


    return render(request,'QnA/like_form.html',co)

def add_comment(request,slug,pk):
    post = get_object_or_404(question,slug=slug,pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        form.instance.author = request.user
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            messages.success(request,f'You have successfully posted your comment!')
            return redirect('question-detail',slug=slug,pk=pk)
    else:
        form = CommentForm()

    context ={
        'form':form
    }

    return render(request,'QnA/comment_form.html',context)

    


    
		


    





