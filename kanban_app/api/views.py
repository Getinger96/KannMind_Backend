from rest_framework.views import APIView
from kanban_app.models import Board, Task, Comment
from kanban_app.api.serializer import BoardSerializer, TaskSerializer, SimpleUserSerializer, CommentSerializer
from rest_framework.response import Response
from rest_framework import status, viewsets, generics
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from django.db import models
from django.contrib.auth.models import User
from rest_framework.exceptions import PermissionDenied, NotFound


class BoardsView(generics.ListCreateAPIView):
    """
    API view to list all boards or create a new one.

    GET: Returns a list of all boards.
    POST: Creates a new board with the authenticated user as the owner.
    """
    queryset = Board.objects.all()
    serializer_class = BoardSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        """
        Sets the authenticated user as the board owner during creation.
        """
        serializer.save(owner=self.request.user)


class BoardDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    API view to retrieve, update, or delete a specific board.

    Only authenticated users can access this view.
    """
    queryset = Board.objects.all()
    serializer_class = BoardSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """
        (Optional) Ensures the authenticated user is set as owner.
        This may not be called unless overridden specifically.
        """
        serializer.save(owner=self.request.user)


class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    API view to retrieve, update, or delete a specific task.

    Only authenticated users can perform these actions.
    Update and delete permissions depend on board membership and ownership.
    """
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        """
        Ensures the user is a board member before allowing task updates.

        Raises:
            PermissionDenied: If user is not a board member.
        """
        task = self.get_object()
        user = self.request.user

        if not task.board.members.filter(id=user.id).exists():
            raise PermissionDenied("You must be a board member to edit this task.")

        serializer.save()

    def perform_destroy(self, instance):
        """
        Ensures only the task creator or board owner can delete the task.

        Raises:
            PermissionDenied: If the user is not authorized.
        """
        user = self.request.user

        if instance.owner != user and instance.board.owner != user:
            raise PermissionDenied("Only the creator or board owner can delete this task.")

        instance.delete()


class TasksView(generics.ListCreateAPIView):
    """
    API view to list all tasks or create a new task.

    Only authenticated users are allowed.
    """
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]


class EmailCheckView(APIView):
    """
    API view to return basic user info (for email check, profile display, etc.).

    GET: Returns authenticated user's basic information.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Returns user data using the SimpleUserSerializer.
        """
        user = request.user
        serializer = SimpleUserSerializer(user)
        return Response(serializer.data)


class TasksAssignedToMeView(generics.ListAPIView):
    """
    API view to list all tasks assigned to the authenticated user.
    """
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Filters tasks where the user is listed as an assignee.
        """
        user = self.request.user
        return Task.objects.filter(assignees=user)


class Tasksreviewing(generics.ListAPIView):
    """
    API view to list all tasks the user is assigned to review.
    """
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Filters tasks where the user is listed as a reviewer.
        """
        user = self.request.user
        return Task.objects.filter(reviewers=user)


class TaskCommentListView(generics.ListCreateAPIView):
    """
    API view to list or add comments to a specific task.

    The user must be a member of the board to view or comment.
    """
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_task(self):
        """
        Retrieves the task based on the URL parameter `pk`.

        Raises:
            NotFound: If task doesn't exist.
            PermissionDenied: If user is not a board member.

        Returns:
            Task: The task instance.
        """
        task_id = self.kwargs.get('pk')
        try:
            task = Task.objects.get(id=task_id)
        except Task.DoesNotExist:
            raise NotFound("Task not found.")

        if self.request.user not in task.board.members.all():
            raise PermissionDenied("You are not a member of this board.")

        return task

    def get_queryset(self):
        """
        Returns the queryset of comments for the given task.
        """
        task = self.get_task()
        return task.comments.all().order_by("created_at")

    def perform_create(self, serializer):
        """
        Creates a new comment on the task with the current user as the author.
        """
        task = self.get_task()
        serializer.save(task=task, author=self.request.user)


class TaskCommentDeleteView(generics.DestroyAPIView):
    """
    API view to delete a comment on a task.

    Only the comment author can delete their own comment.
    """
    permission_classes = [IsAuthenticated]

    def get_object(self):
        """
        Retrieves the comment instance based on task and comment IDs in the URL.

        Raises:
            NotFound: If task or comment is not found.
            PermissionDenied: If the user is not the comment's author.

        Returns:
            Comment: The comment instance to delete.
        """
        task_id = self.kwargs.get('task_id')  
        comment_id = self.kwargs.get('comment_id')  

        try:
            task = Task.objects.get(id=task_id)
        except Task.DoesNotExist:
            raise NotFound("Task not found.")

        try:
            comment = Comment.objects.get(id=comment_id, task=task)
        except Comment.DoesNotExist:
            raise NotFound("Comment not found.")

        if comment.author != self.request.user:
            raise PermissionDenied("Only the author can delete this comment.")

        return comment
