from django.urls import path
from . import views
from .views import home,QuestionListView,QuestionDetailView,QuestionCreateView,SolutionView,QuestionUpdateView,QuestionDeleteView,CommentDeleteView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', home, name='home'),
    path("QnA/", QuestionListView.as_view(), name="qna"),
    path("question/<slug:slug>/<int:pk>/", QuestionDetailView.as_view(), name='question-detail'),
    path('question/<slug:slug>/<int:pk>/update/', QuestionUpdateView.as_view(),name='question-update'),
    path('question/<slug:slug>/<int:pk>/delete/', QuestionDeleteView.as_view(),name='question-delete'),
    path('comment/<int:pk>/delete/', CommentDeleteView.as_view(),name='comment-delete'),
    path("newquestion/", QuestionCreateView.as_view(), name='new-question'),
    path("question/<slug:slug>/<int:pk>/comment/", views.add_comment, name='add-comment'),
    path("comment/<int:pk>/solution/", views.SolutionView, name='solution'),
    path("comment/<int:pk>/vote/", views.comment_like, name='vote'),
    path("question/<slug:slug>/<int:pk>/vote/", views.question_like, name='vote_question'),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
