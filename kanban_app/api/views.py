# Importiert die APIView-Basisklasse für eigene Views
from rest_framework.views import APIView

# Importiert die Modelle aus der Kanban-App
from kanban_app.models import Board, Task, Comment

# Importiert die zugehörigen Serializer
from kanban_app.api.serializer import BoardSerializer, TaskSerializer, SimpleUserSerializer, CommentSerializer

# Für HTTP-Antworten wie Response(data, status)
from rest_framework.response import Response

# Importiert HTTP-Statuscodes (z. B. 200 OK, 403 FORBIDDEN)
from rest_framework import status

# Generische Views für CRUD-Operationen
from rest_framework import viewsets
from rest_framework import generics

# Berechtigungsklassen von DRF
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny

# Django-Modelle (nicht direkt verwendet hier)
from django.db import models

# Das eingebaute User-Modell
from django.contrib.auth.models import User

# Für benutzerdefinierte Fehler
from rest_framework.exceptions import PermissionDenied, NotFound


# View zum Anzeigen & Erstellen von Boards
class BoardsView(generics.ListCreateAPIView):
    # Queryset: Alle Boards
    queryset = Board.objects.all()
    # Serializer für Darstellung & Validierung
    serializer_class = BoardSerializer
    # Nur eingeloggte Nutzer dürfen POST machen
    permission_classes = [IsAuthenticatedOrReadOnly]

    # Setzt den aktuellen Nutzer als Besitzer beim Erstellen
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


# View für einzelne Boards (GET, PUT, DELETE)
class BoardDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer
    permission_classes = [IsAuthenticated]

    # (Optional – in dieser View eher nicht notwendig)
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


# View zum Bearbeiten und Löschen einzelner Tasks
class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    # Nur Mitglieder des Boards dürfen Tasks bearbeiten
    def perform_update(self, serializer):
        task = self.get_object()
        user = self.request.user

        # Prüft ob User im Board ist
        if not task.board.members.filter(id=user.id).exists():
            raise PermissionDenied("Du musst Mitglied des Boards sein, um diese Aufgabe zu bearbeiten.")

        serializer.save()

    # Nur Ersteller oder Board-Owner dürfen löschen
    def perform_destroy(self, instance):
        user = self.request.user

        # Berechtigungsprüfung für Löschen
        if instance.owner != user and instance.board.owner != user:
            raise PermissionDenied("Nur der Ersteller oder der Eigentümer des Boards darf diese Aufgabe löschen.")

        instance.delete()


# View zum Anzeigen und Erstellen von Aufgaben
class TasksView(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]


# View zur Rückgabe der aktuell eingeloggten User-Daten
class EmailCheckView(APIView):
    permission_classes = [IsAuthenticated]

    # Gibt aktuelle User-Daten (z. B. für Profil oder Auth-Check)
    def get(self, request):
        user = request.user
        serializer = SimpleUserSerializer(user)
        return Response(serializer.data)


# View für alle Aufgaben, bei denen der User als "assignee" eingetragen ist
class TasksAssignedToMeView(generics.ListAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    # Gibt nur Aufgaben zurück, die dem aktuellen User zugewiesen sind
    def get_queryset(self):
        user = self.request.user
        return Task.objects.filter(assignees=user)


# View für Aufgaben, bei denen der User Reviewer ist
class Tasksreviewing(generics.ListAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    # Gibt alle Tasks zurück, bei denen der Nutzer Reviewer ist
    def get_queryset(self):
        user = self.request.user
        return Task.objects.filter(reviewers=user)


# View zum Auflisten und Erstellen von Kommentaren zu einem Task
class TaskCommentListView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    # Holt den Task, prüft ob der User Mitglied im Board ist
    def get_task(self):
        task_id = self.kwargs.get('pk')
        try:
            task = Task.objects.get(id=task_id)
        except Task.DoesNotExist:
            raise NotFound("Task nicht gefunden.")

        # Zugriff nur für Mitglieder des Boards
        if self.request.user not in task.board.members.all():
            raise PermissionDenied("Du bist kein Mitglied dieses Boards.")
        return task

    # Holt alle Kommentare zu einem Task, sortiert nach Erstellungszeit
    def get_queryset(self):
        task = self.get_task()
        return task.comments.all().order_by("created_at")

    # Erstellt neuen Kommentar zum Task
    def perform_create(self, serializer):
        task = self.get_task()
        print("DEBUG USER:", self.request.user, self.request.user.is_authenticated)
        serializer.save(task=task, author=self.request.user)


# View zum Löschen eines Kommentars innerhalb eines Tasks
class TaskCommentDeleteView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]

    # Holt den Kommentar und prüft Berechtigung
    def get_object(self):
        task_id = self.kwargs.get('task_id')  # In URL als task_id übergeben
        comment_id = self.kwargs.get('comment_id')  # In URL als comment_id übergeben

        # Holt den Task
        try:
            task = Task.objects.get(id=task_id)
        except Task.DoesNotExist:
            raise NotFound("Task nicht gefunden.")

        # Holt den Kommentar zum Task
        try:
            comment = Comment.objects.get(id=comment_id, task=task)
        except Comment.DoesNotExist:
            raise NotFound("Kommentar nicht gefunden.")

        # Nur Autor darf löschen
        if comment.author != self.request.user:
            raise PermissionDenied("Nur der Ersteller darf diesen Kommentar löschen.")

        return comment
