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
from django.contrib.auth.decorators import login_required

def home(request):
    context={
        
    }
    return render(request, 'QnA/homepage.html',context)



#### Question Module ####

class QuestionListView(ListView):
    model = question #choosing the database 
    template_name = 'QnA/question.html' #specifying the template
    context_object_name = 'question' #the object name in the template
    ordering = ['-date_published'] #to arrange the post from the latest date published
    paginate_by = 5 #to limit 5 question per page

class QuestionDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = question #choosing the database 
    success_url ='/QnA/' #the redirect after any action is done successfully

    def test_func(self): #to test the user input 
        post = self.get_object() #to get data from the model question
        if self.request.user == post.author: #to check whether the requesting user is the question author
            return True
        return False

class QuestionCreateView(CreateView):
    model = question #choosing the database
    fields = ['title','content','image','category'] #to specify what user needs to input

    def form_valid(self,form): #this is needed to tell the server what to do after the form is valid
        form.instance.author = self.request.user #the author of the new question is the user requesting the new post
        return super().form_valid(form)

class QuestionDetailView(DetailView): 
    model = question #choosing the database


class QuestionUpdateView(UpdateView):
    model = question #choosing the database
    fields = ['title','content','image'] #to specify what user needs to input
    
    def form_valid(self,form): #this is needed to tell the server what to do after the form is valid
        form.instance.author = self.request.user #the author will be the one requesting the changes
        return super().form_valid(form)

class QuestionCategory(ListView):
    model = question #choosing the database 
    template_name='QnA/category.html' #specifying the template
    ordering = ['-date_published'] #to arrange the post from the latest date published
    paginate_by = 5 #to limit 5 question per page

    def get_queryset(self): #determines the list of objects that you want to display
        self.Category = get_object_or_404(category,slug=self.kwargs['slug']) #it will try to get the category from database which has the same slug as the requesting slug
        return question.objects.filter(category=self.Category) #it will filter the question which is having the same slug as the requesting slug

    def get_context_data(self,**kwargs):#to retrieve the data in list form (question_list)
        context = super(QuestionCategory,self).get_context_data(**kwargs) #to get data from the parent class QuestionCategory I used **kwargs is needed so that it will pass in variable that is not yet defined
        context['category']= self.Category #it will return the question in a list form
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

@login_required
def add_comment(request,pk):
    post = get_object_or_404(question,pk=pk)
    reward = get_object_or_404(Reward,user=post.author)
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
            reward.accu_rtoken += 1 
            reward.points += 10.0
            try: 
                reward.accu_rtoken_percentage = round(((reward.accu_rtoken*10)/reward.points)*100,2)
                reward.accu_quest_likes_percentage = round(((reward.accu_quest_likes)/reward.points)*100,2)
                reward.accu_comment_likes_percentage = round(((reward.accu_comment_likes)/reward.points)*100,2)
            except ZeroDivisionError: 
                reward.accu_rtoken_percentage = 0
                reward.accu_quest_likes_percentage = 0
                reward.accu_comment_likes_percentage = 0
            post.save()
            reward.save()
        else:
            post.r_token = False
            reward.accu_rtoken -= 1
            reward.points -= 10.0
            try:
                reward.accu_rtoken_percentage = round(((reward.accu_rtoken*10)/reward.points)*100,2)
                reward.accu_quest_likes_percentage = round(((reward.accu_quest_likes)/reward.points)*100,2)
                reward.accu_comment_likes_percentage = round(((reward.accu_comment_likes)/reward.points)*100,2)
            except ZeroDivisionError:
                reward.accu_rtoken_percentage = 0
                reward.accu_quest_likes_percentage = 0
                reward.accu_comment_likes_percentage = 0
            post.save()
            reward.save()
        return redirect('qna')
    
    return render(request,'QnA/solution_form.html')

#### End Of Reward Module ###

#### Question Likes Module ####

def question_like(request,pk):
    post = get_object_or_404(question,pk=pk)
    reward = get_object_or_404(Reward,user=post.author)
    if request.method == 'POST':
        if post.liked_by.filter(id=request.user.id).exists():
            post.liked_by.remove(request.user)
            post.like -= 1
            reward.points -= 1
            reward.accu_quest_likes -= 1
            try:
                reward.accu_rtoken_percentage = round(((reward.accu_rtoken*10)/reward.points)*100,2)
                reward.accu_quest_likes_percentage = round(((reward.accu_quest_likes)/reward.points)*100,2)
                reward.accu_comment_likes_percentage = round(((reward.accu_comment_likes)/reward.points)*100,2)
            except ZeroDivisionError: 
                reward.accu_rtoken_percentage = 0
                reward.accu_quest_likes_percentage = 0
                reward.accu_comment_likes_percentage = 0
            post.save()
            reward.save()
        else:
            post.liked_by.add(request.user)
            post.like += 1
            reward.points += 1
            reward.accu_quest_likes += 1
            try:
                reward.accu_rtoken_percentage = round(((reward.accu_rtoken*10)/reward.points)*100,2)
                reward.accu_quest_likes_percentage = round(((reward.accu_quest_likes)/reward.points)*100,2)
                reward.accu_comment_likes_percentage = round(((reward.accu_comment_likes)/reward.points)*100,2)
            except ZeroDivisionError:
                reward.accu_rtoken_percentage = 0
                reward.accu_quest_likes_percentage = 0
                reward.accu_comment_likes_percentage = 0
            post.save()
            reward.save()
        return redirect('qna')
    
    context={

    }

    return render(request,'QnA/questionlike_form.html',context)

#### End Of Question Likes Module ###

#### CommentLikes Module ####

def comment_like(request,pk):
    post = get_object_or_404(comment,pk=pk)
    reward = get_object_or_404(Reward,user=post.author)
    if request.method == 'POST':
        if post.liked_by.filter(id=request.user.id).exists():
            post.liked_by.remove(request.user)
            post.like -= 1
            reward.points -= 1
            reward.accu_comment_likes -= 1
            try: 
                reward.accu_rtoken_percentage = round(((reward.accu_rtoken*10)/reward.points)*100,2)
                reward.accu_quest_likes_percentage = round(((reward.accu_quest_likes)/reward.points)*100,2)
                reward.accu_comment_likes_percentage = round(((reward.accu_comment_likes)/reward.points)*100,2)
            except ZeroDivisionError:
                reward.accu_rtoken_percentage = 0
                reward.accu_quest_likes_percentage = 0
                reward.accu_comment_likes_percentage = 0
            post.save()
            reward.save()
        else:
            post.liked_by.add(request.user)
            post.like += 1
            reward.points += 1
            reward.accu_comment_likes += 1
            try:
                reward.accu_rtoken_percentage = round(((reward.accu_rtoken*10)/reward.points)*100,2)
                reward.accu_quest_likes_percentage = round(((reward.accu_quest_likes)/reward.points)*100,2)
                reward.accu_comment_likes_percentage = round(((reward.accu_comment_likes)/reward.points)*100,2)
            except ZeroDivisionError:
                reward.accu_rtoken_percentage = 0
                reward.accu_quest_likes_percentage = 0
                reward.accu_comment_likes_percentage = 0    
            post.save()
            reward.save()
        return redirect('qna')
    
    context={

    }


    return render(request,'QnA/like_form.html',context)

#### End Of Comment Likes Module ###


#### Search Module ###





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
    

        


    





