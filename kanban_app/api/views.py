from django.http import Http404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializer import BoardSerializer,BoardCreateSerializer,BoardDetailSerializer,BoardUpdateSerializer,TaskCreateSerializer,TaskSerializer,TaskDetailSerializer,CommentCreateSerializer,CommentResponseSerializer
from kanban_app.models import Board,Task,Comment
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics, status
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from django.core.validators import EmailValidator
from rest_framework.exceptions import ValidationError
from .permissions import IsBoardMemberOrOwner,IsBoardMember,IsTaskCreatorOrBoardOwner,IsBoardMemberForTask,IsCommentAuthor



class BoardsView(APIView):
    """
    API view for listing and creating boards.
    GET: Returns all boards where the user is a member or owner.
    POST: Creates a new board with the logged-in user as the owner.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        boards = Board.objects.filter(members=request.user) | Board.objects.filter(owner=request.user)
        boards = boards.distinct()
        serializer = BoardSerializer(boards, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = BoardCreateSerializer(data=request.data)
        if serializer.is_valid():
            board = serializer.save(owner=request.user)
            response_serializer = BoardSerializer(board)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BoardsDetailView(generics.GenericAPIView):
    """
    API view for retrieving details, updating (PATCH), and deleting a board.
    Access rights: Only board owners or members.
    """
    queryset = Board.objects.all()
    serializer_class = BoardDetailSerializer
    permission_classes = [IsAuthenticated, IsBoardMemberOrOwner]

    def get_object(self):
        board = super().get_object()
        self.check_object_permissions(self.request, board)
        return board

    def get(self, request, *args, **kwargs):
        board = self.get_object()
        serializer = BoardDetailSerializer(board)
        return Response(serializer.data)

    def patch(self, request, *args, **kwargs):
        board = self.get_object()
        input_serializer = BoardSerializer(board, data=request.data, partial=True)
        if input_serializer.is_valid():
            input_serializer.save()
            board.refresh_from_db()
            response_serializer = BoardUpdateSerializer(board)
            return Response(response_serializer.data)
        return Response(input_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        board = self.get_object()
        board.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class EmailCheckView(APIView):
    """
    API view to check if a given email address exists and is valid.
    Only authenticated users can use this view.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        email = request.query_params.get('email')
        if not email:
            return Response({'error': 'Email address is required.'}, status=status.HTTP_400_BAD_REQUEST)

        validator = EmailValidator()
        try:
            validator(email)
        except ValidationError:
            return Response({'error': 'Invalid email format.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'detail': 'Email not found.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception:
            return Response({'error': 'Internal server error.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        fullname = f"{user.first_name} {user.last_name}".strip()
        return Response({"id": user.id, "email": user.email, "fullname": fullname}, status=status.HTTP_200_OK)


class TaskView(APIView):
    """
    API view for creating tasks.
    Access permission: Only members of the related board.
    """
    permission_classes = [IsAuthenticated, IsBoardMember]

    def post(self, request, format=None):
        serializer = TaskCreateSerializer(data=request.data)
        if serializer.is_valid():
            task = serializer.save()
            response_serializer = TaskSerializer(task)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TasksDetailView(generics.GenericAPIView):
    """
    API view for retrieving details, updating (PATCH), and deleting tasks.
    Access permissions:
      - Authenticated users
      - Members of the related board
      - Only task creators or board owners can make changes
    """
    queryset = Task.objects.all()
    serializer_class = TaskCreateSerializer
    permission_classes = [IsAuthenticated, IsBoardMember, IsTaskCreatorOrBoardOwner]

    def get_object(self):
        task = generics.get_object_or_404(Task, pk=self.kwargs['pk'])
        self.check_object_permissions(self.request, task.board)
        return task

    def get(self, request, *args, **kwargs):
        task = self.get_object()
        serializer = TaskDetailSerializer(task)
        return Response(serializer.data)

    def patch(self, request, *args, **kwargs):
        task = self.get_object()
        data = request.data.copy()

        if "board" in data and data["board"] != str(task.board.id):
            return Response({"error": "The board of a task cannot be changed."}, status=status.HTTP_400_BAD_REQUEST)

        board_members = list(task.board.members.all()) + [task.board.owner]
        assignee_id = data.get("assignee_id")
        reviewer_id = data.get("reviewer_id")

        if assignee_id and not any(user.id == int(assignee_id) for user in board_members):
            return Response({"error": "Assignee must be a member of the board."}, status=status.HTTP_400_BAD_REQUEST)

        if reviewer_id and not any(user.id == int(reviewer_id) for user in board_members):
            return Response({"error": "Reviewer must be a member of the board."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = TaskCreateSerializer(task, data=data, partial=True)
        if serializer.is_valid():
            task = serializer.save()
            response_serializer = TaskDetailSerializer(task)
            return Response(response_serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        task = self.get_object()
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TaskCommentsListCreateView(generics.GenericAPIView):
    """
    API view for listing and creating comments on a task.
    Access permission: Only board members of the respective task.
    """
    permission_classes = [IsAuthenticated, IsBoardMemberForTask]
    serializer_class = CommentResponseSerializer
    queryset = Comment.objects.all()

    def get_task(self, pk):
        task = generics.get_object_or_404(Task, pk=pk)
        self.check_object_permissions(self.request, task)
        return task

    def get(self, request, pk):
        task = self.get_task(pk)
        comments = task.comments.order_by('created_at')
        serializer = CommentResponseSerializer(comments, many=True)
        return Response(serializer.data)

    def post(self, request, pk):
        task = self.get_task(pk)
        serializer = CommentCreateSerializer(data=request.data)
        if serializer.is_valid():
            comment = serializer.save(task=task, author=request.user)
            response_serializer = CommentResponseSerializer(comment)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TaskCommentDeleteView(generics.DestroyAPIView):
    """
    API view for deleting a comment.
    Only the author of the comment is allowed to delete it.
    """
    queryset = Comment.objects.all()
    permission_classes = [IsAuthenticated, IsCommentAuthor]

    def get_object(self):
        comment = generics.get_object_or_404(Comment, pk=self.kwargs['comment_pk'])
        if comment.task_id != int(self.kwargs['pk']):
            raise Http404("Comment does not belong to the specified task.")
        self.check_object_permissions(self.request, comment)
        return comment


class TasksAssignedToMeView(APIView):
    """
    API view to retrieve all tasks assigned to the current user.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        tasks = Task.objects.filter(assignees=user)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)


class TasksReviewingView(APIView):
    """
    API view to retrieve all tasks where the current user is a reviewer.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        tasks = Task.objects.filter(reviewers=user)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)
