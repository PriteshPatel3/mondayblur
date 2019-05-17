from django.shortcuts import render,get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from .models import question,category,comment
from.forms import CommentForm,SolutionForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.generic import ListView,TemplateView,DetailView,CreateView,UpdateView,DeleteView
from django.shortcuts import render
from django.http import HttpResponse
from users.models import Reward

def home(request):
    context={
        
    }
    return render(request, 'QnA/homepage.html',context)



#### Question Module ####

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

class QuestionCreateView(CreateView):
    model = question
    fields = ['title','content','image','category']

    def form_valid(self,form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class QuestionDetailView(DetailView):
    model = question


class QuestionUpdateView(UpdateView):
    model = question
    fields = ['title','content']
    
    def form_valid(self,form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class QuestionCategory(ListView):
    model = question
    template_name='QnA/category.html'

    def get_queryset(self):
        self.Category = get_object_or_404(category,slug=self.kwargs['slug'])
        return question.objects.filter(category=self.Category)

    def get_context_data(self,**kwargs):
        context = super(QuestionCategory,self).get_context_data(**kwargs)
        context['category']= self.Category
        return context

#### End of Question Module ###

#### User Profile Module ####

class UserProfileView(ListView):
    model = question
    template_name = 'QnA/user_profile.html'
    context_object_name = 'question'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return question.objects.filter(author=user).order_by('-date_published')

#### End Of User Profile Module ####


#### Comment Module ####

class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = comment
    success_url = '/QnA/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

def add_comment(request,pk):
    post = get_object_or_404(question,pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        form.instance.author = request.user
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            messages.success(request,f'You have successfully posted your comment!')
            return redirect('question-detail',pk=pk)
    else:
        form = CommentForm()

    context ={
        'form':form
    }

    return render(request,'QnA/comment_form.html',context)

#### End Of Comment Module ###

#### Reward Module ####

def SolutionView(request,pk):
    post = get_object_or_404(comment,pk=pk)
    reward = get_object_or_404(Reward,user=post.author)
    if request.method =='POST':
        if post.r_token == False:
            post.r_token = True  
            reward.points += 10
            post.save()
            reward.save()
        else:
            post.r_token = False
            reward.points -= 10
            post.save()
            reward.save()

        return redirect('qna')
    
    return render(request,'QnA/solution_form.html')

def question_like(request,pk):
    post = get_object_or_404(question,pk=pk)
    reward = get_object_or_404(Reward,user=post.author)
    if request.method == 'POST':
        if post.liked_by.filter(id=request.user.id).exists():
            post.liked_by.remove(request.user)
            post.like -= 1
            post.save()
            reward.points -= 1
            reward.save()
        else:
            post.liked_by.add(request.user)
            post.like += 1
            post.save()
            reward.points += 1
            reward.save()
        return redirect('qna')
    
    context={

    }


    return render(request,'QnA/questionlike_form.html',context)

def comment_like(request,pk):
    post = get_object_or_404(comment,pk=pk)
    reward = get_object_or_404(Reward,user=post.author)
    if request.method == 'POST':
        if post.liked_by.filter(id=request.user.id).exists():
            post.liked_by.remove(request.user)
            post.like -= 1
            post.save()
            reward.points -= 1
            reward.save()
        else:
            post.liked_by.add(request.user)

            post.like += 1
            post.save()
            reward.points += 1
            reward.save()
        return redirect('qna')
    
    context={

    }


    return render(request,'QnA/like_form.html',context)

#### End Of Reward Module ###



def search_form(request):
    return render(request, 'QnA/search_form.html')



def search(request):
    error = False
    if 'search' in request.GET:
        search = request.GET['search']
        if not search:
            error = True
        else:

            questions = question.objects.filter(title__icontains=search)
            return render(request, 'QnA/search_results.html', {'questions': questions, 'query': search})
    return render(request, 'QnA/search_form.html', {'error': error})

#### End Of Search Module ####
    


    
        


    





