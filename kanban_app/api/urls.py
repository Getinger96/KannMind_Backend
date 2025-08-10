from django.urls import path
from .views import BoardsView,BoardsDetailView,EmailCheckView,TaskView,TasksDetailView,TaskCommentsListCreateView,TasksAssignedToMeView,TasksReviewingView,TaskCommentDeleteView


urlpatterns = [
    path('boards/',BoardsView.as_view()),
    path('boards/<int:pk>/', BoardsDetailView.as_view()),
    path('email-check/', EmailCheckView.as_view()),
    path('tasks/assigned-to-me/', TasksAssignedToMeView.as_view()),
    path('tasks/reviewing/', TasksReviewingView.as_view()),
    path('tasks/', TaskView.as_view()),
    path('tasks/<int:pk>/',TasksDetailView.as_view()),
    path('tasks/<int:pk>/comments/', TaskCommentsListCreateView.as_view()),
    path('tasks/<int:pk>/comments/<int:comment_pk>/', TaskCommentDeleteView.as_view()),

]
