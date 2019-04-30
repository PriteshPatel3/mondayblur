from django.urls import path
from . import views
from .views import home,QuestionListView,QuestionDetailView,QuestionCreateView,SolutionView,QuestionUpdateView,QuestionDeleteView,CommentDeleteView
urlpatterns = [
    path('', home, name='home'),
    path("QnA/", QuestionListView.as_view(), name="qna"),
    path("question/<slug:slug>/<int:pk>/", QuestionDetailView.as_view(), name='question-detail'),
    path('question/<slug:slug>/<int:pk>/update/', QuestionUpdateView.as_view(),name='question-update'),
    path('question/<slug:slug>/<int:pk>/delete/', CommentDeleteView.as_view(),name='question-delete'),
    path('comment/<int:pk>/delete/', QuestionDeleteView.as_view(),name='comment-delete'),
    path("newquestion/", QuestionCreateView.as_view(), name='new-question'),
    path("question/<slug:slug>/comment/", views.add_comment, name='add-comment'),
    path("comment/<int:pk>/solution/", SolutionView.as_view(), name='solution'),
]
