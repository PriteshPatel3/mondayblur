from django.urls import path
from . import views
from .views import home,QuestionListView,QuestionDetailView,QuestionCreateView
urlpatterns = [
    path('', home, name='home'),
    path("QnA/", QuestionListView.as_view(), name="qna"),
    path("question/<slug:slug>/<int:pk>", QuestionDetailView.as_view(), name='question-detail'),
    path("newquestion/", QuestionCreateView.as_view(), name='new-question'),
    path("question/<slug:slug>/comment/", views.add_comment, name='add-comment'),
]