from django.urls import path
from . import views
from .views import home,QuestionListView,QuestionDetailView,CommentCreateView

urlpatterns = [
    path('', home, name='home'),
    path("QnA/", QuestionListView.as_view(), name="qna"),
    path("question/<int:pk>/", QuestionDetailView.as_view(), name='question-detail'),
    path('newcomment/', CommentCreateView.as_view(),name='add-comment'),
    

]