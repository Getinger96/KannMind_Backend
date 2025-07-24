from django.urls import path
from .views import BoardsView,TasksView,BoardDetailView,TaskDetailView,EmailCheckView,TasksAssignedToMeView,Tasksreviewing,TaskCommentListView,TaskCommentDeleteView


urlpatterns = [
    path('boards/',BoardsView.as_view()),
    path('boards/<int:pk>/',BoardDetailView.as_view()),
    path('email-check/',EmailCheckView.as_view()),
    path('tasks/assigned-to-me/',TasksAssignedToMeView.as_view()),
    path('tasks/reviewing/',Tasksreviewing.as_view()),
    path('tasks/',TasksView.as_view()),
    path('tasks/<int:pk>/',TaskDetailView.as_view()),
    path('tasks/<int:pk>/comments/',TaskCommentListView.as_view()),
    path('tasks/<int:pk>/comments/<int:comment_pk>/',TaskCommentDeleteView.as_view()),
    
]