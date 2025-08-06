from django.urls import path
from .views import first_view,first_single_view


urlpatterns = [
    path('boards/',first_view),
    path('boards/<int:pk>/', first_single_view),
#     path('email-check/', EmailCheckView.as_view()),
#     path('tasks/assigned-to-me/', TasksAssignedToMeView.as_view()),
#     path('tasks/reviewing/', Tasksreviewing.as_view()),
#     path('tasks/', TasksView.as_view()),
#     path('tasks/<int:pk>/', TaskDetailView.as_view()),
#     path('tasks/<int:pk>/comments/', TaskCommentListView.as_view()),
#     path('tasks/<int:pk>/comments/<int:comment_pk>/', TaskCommentDeleteView.as_view()),
# 
]
