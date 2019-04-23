from django.urls import path
from . import views
from .views import home,QuestionListView,QuestionDetailView
urlpatterns = [
    path('', home, name='home'),
    path("QnA/", QuestionListView.as_view(), name="qna"),
    path("question/<slug:slug>/", QuestionDetailView.as_view(), name='question-detail'),
    path("question/<slug:slug>/comment/", views.add_comment, name='add-comment'),
    

]