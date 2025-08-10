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
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        # Filter Boards, bei denen user Owner oder Member ist
        boards = Board.objects.filter(members=request.user) | Board.objects.filter(owner=request.user)
        boards = boards.distinct()
        serializer = BoardSerializer(boards, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
       serializer = BoardCreateSerializer(data=request.data)
        
       if serializer.is_valid():
            board=serializer.save(owner=request.user)
            Response_serializer=BoardSerializer(board)
            return Response(Response_serializer.data, status=status.HTTP_201_CREATED)
       else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)



class BoardsDetailView(generics.GenericAPIView):
    queryset = Board.objects.all()
    serializer_class = BoardDetailSerializer  # Zum Aktualisieren
    permission_classes = [IsAuthenticated, IsBoardMemberOrOwner]

    

    def get_object(self):
        board = super().get_object()  # oder alternativ: self.queryset.get(pk=self.kwargs['pk'])
        self.check_object_permissions(self.request, board)  # <- wichtig für IsBoardMemberOrOwner
        return board
    
    def get(self, request, *args, **kwargs):
     board = self.get_object()
     serializer = BoardDetailSerializer(board)
     return Response(serializer.data)

    def patch(self, request, *args, **kwargs):
     board = self.get_object()

    # 1. Schreiben mit BoardSerializer (enthält members als write_only)
     input_serializer = BoardSerializer(board, data=request.data, partial=True)
    
     if input_serializer.is_valid():
        input_serializer.save()  # persistiert Änderungen

        # 2. Neuladen aus DB für aktualisierte Daten (optional, aber sicherer)
        board.refresh_from_db()

        # 3. Antwort mit dem ausführlichen Output-Serializer
        response_serializer = BoardUpdateSerializer(board)
        return Response(response_serializer.data)

     return Response(input_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, *args, **kwargs):
        board = self.get_object()
        board.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


    

class EmailCheckView(APIView):
    permission_classes = [IsAuthenticated]  # Benutzer muss eingeloggt sein

    def get(self, request):
        email = request.query_params.get('email')
        if not email:
            return Response(
                {'error': 'E-Mail-Adresse ist erforderlich.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # E-Mail-Format validieren
        validator = EmailValidator()
        try:
            validator(email)
        except ValidationError:
            return Response(
                {'error': 'Ungültiges E-Mail-Format.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response(
                {'detail': 'E-Mail nicht gefunden.'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception:
            # Für alle anderen Fehler (Datenbank etc.)
            return Response(
                {'error': 'Interner Serverfehler.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
        fullname = f"{user.first_name} {user.last_name}".strip()

        return Response(
            {
                "id": user.id,
                "email": user.email,
                "fullname": fullname,
            },
            status=status.HTTP_200_OK
        )
    

class TaskView(APIView):
    permission_classes = [IsAuthenticated, IsBoardMember]
    def post(self, request, format=None):
       serializer =TaskCreateSerializer(data=request.data)
       
        
       if serializer.is_valid():
            task=serializer.save()
            Response_serializer=TaskSerializer(task)
            return Response(Response_serializer.data, status=status.HTTP_201_CREATED)
       else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)




class TasksDetailView(generics.GenericAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskCreateSerializer  # Zum Aktualisieren
    permission_classes = [IsAuthenticated, IsBoardMember,IsTaskCreatorOrBoardOwner] 

    

    def get_object(self):
        task = generics.get_object_or_404(Task, pk=self.kwargs['pk'])
        self.check_object_permissions(self.request, task.board)  # ✅ Permission prüfen für das zugehörige Board
        return task
    
    def get(self, request, *args, **kwargs):
        task = self.get_object()
        serializer = TaskDetailSerializer(task)
        return Response(serializer.data)

    def patch(self, request, *args, **kwargs):
        task = self.get_object()
        data = request.data.copy()

        # ✅ Verhindere Änderung der board-ID
        if "board" in data and data["board"] != str(task.board.id):
            return Response(
                {"error": "Das Board einer Task kann nicht geändert werden."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # ✅ Überprüfen: assignee/reviewer müssen Mitglieder des Boards sein
        board_members = list(task.board.members.all()) + [task.board.owner]
        assignee_id = data.get("assignee_id")
        reviewer_id = data.get("reviewer_id")

        if assignee_id and not any(user.id == int(assignee_id) for user in board_members):
            return Response(
                {"error": "Assignee muss Mitglied des Boards sein."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if reviewer_id and not any(user.id == int(reviewer_id) for user in board_members):
            return Response(
                {"error": "Reviewer muss Mitglied des Boards sein."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # ✅ Serialisieren und speichern
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

    def delete(self, request, *args, **kwargs):
        task = self.get_object()
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



class TaskCommentsListCreateView(generics.GenericAPIView):
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
        print("request.data:", request.data)
        task = self.get_task(pk)
        serializer = CommentCreateSerializer(data=request.data)
        if serializer.is_valid():
            comment = serializer.save(task=task, author=request.user)
            response_serializer = CommentResponseSerializer(comment)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TaskCommentDeleteView(generics.DestroyAPIView):
    queryset = Comment.objects.all()
    permission_classes = [IsAuthenticated, IsCommentAuthor]

    def get_object(self):
        comment = generics.get_object_or_404(Comment, pk=self.kwargs['comment_pk'])
        if comment.task_id != int(self.kwargs['pk']):
            raise Http404("Kommentar gehört nicht zur angegebenen Task.")
        self.check_object_permissions(self.request, comment)
        return comment



class TasksAssignedToMeView(APIView):
     permission_classes = [IsAuthenticated]

     def get(self, request):
        user = request.user
        tasks = Task.objects.filter(assignees=user)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)
     


class TasksReviewingView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        tasks = Task.objects.filter(reviewers=user)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)