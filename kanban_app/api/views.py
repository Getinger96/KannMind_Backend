from rest_framework.views import APIView
from kanban_app.models import Board, Task,Comment
from kanban_app.api.serializer import BoardSerializer,TaskSerializer,SimpleUserSerializer,CommentSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated,IsAuthenticatedOrReadOnly,AllowAny
from django.db import models 
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied, NotFound





class BoardsView(generics.ListCreateAPIView):
   
    queryset = Board.objects.all()
    serializer_class = BoardSerializer
    permission_classes= [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)





class BoardDetailView(generics.RetrieveUpdateDestroyAPIView):
   
    queryset = Board.objects.all()
    serializer_class = BoardSerializer
    permission_classes= [IsAuthenticated]


    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)



class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
   
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes= [IsAuthenticated]


    
    def perform_update(self, serializer):
        task = self.get_object()
        user = self.request.user

        if not task.board.members.filter(id=user.id).exists():
            raise PermissionDenied("Du musst Mitglied des Boards sein, um diese Aufgabe zu bearbeiten.")

        serializer.save()

    def perform_destroy(self, instance):
        user = self.request.user

        
        if instance.owner != user and instance.board.owner != user:
            raise PermissionDenied("Nur der Ersteller oder der Eigentümer des Boards darf diese Aufgabe löschen.")

        
        instance.delete()
    


class TasksView(generics.ListCreateAPIView):
    queryset= Task.objects.all()
    serializer_class= TaskSerializer
    permission_classes= [IsAuthenticated]


class EmailCheckView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user 
        
       
        
        serializer = SimpleUserSerializer(user)
        return Response(serializer.data)
    

class TasksAssignedToMeView(generics.ListAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Task.objects.filter(assignees=user)
    


class Tasksreviewing(generics.ListAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Task.objects.filter(reviewer_id=user)

class TaskCommentListView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_task(self):
        task_id = self.kwargs.get('pk')
        try:
            task = Task.objects.get(id=task_id)
        except Task.DoesNotExist:
            raise NotFound("Task nicht gefunden.")

        if self.request.user not in task.board.members.all():
            raise PermissionDenied("Du bist kein Mitglied dieses Boards.")
        return task

    def get_queryset(self):
        task = self.get_task()
        return task.comments.all().order_by("created_at")

    def perform_create(self, serializer):
        task = self.get_task()
        print("DEBUG USER:", self.request.user, self.request.user.is_authenticated)
        serializer.save(task=task, author=self.request.user)




class TaskCommentDeleteView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]

    def get_object(self):
        task_id = self.kwargs.get('task_id')
        comment_id = self.kwargs.get('comment_id')

        try:
            task = Task.objects.get(id=task_id)
        except Task.DoesNotExist:
            raise NotFound("Task nicht gefunden.")

        try:
            comment = Comment.objects.get(id=comment_id, task=task)
        except Comment.DoesNotExist:
            raise NotFound("Kommentar nicht gefunden.")

        if comment.author != self.request.user:
            raise PermissionDenied("Nur der Ersteller darf diesen Kommentar löschen.")

        return comment