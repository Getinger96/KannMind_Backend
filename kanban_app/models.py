# Importiert das Models-Modul von Django für die Datenbankmodelle
from django.db import models

# Importiert das eingebaute User-Modell von Django
from django.contrib.auth.models import User


# Modell für ein Kanban-Board
class Board(models.Model):
    # Titel des Boards, max. 30 Zeichen
    title = models.CharField(max_length=30)
    
    # Mitglieder des Boards (viele-zu-viele Beziehung zu Usern)
    members = models.ManyToManyField(User, related_name='member_boards')
    
    # Eigentümer des Boards (ein User besitzt mehrere Boards)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='boards')


# Modell für eine Aufgabe (Task) auf einem Board
class Task(models.Model):
    # Mögliche Prioritäten für Aufgaben
    PRIORITY_CHOICES = {
        "H": "HIGH",
        "M": "MEDIUM",
        "L": "LOW",
    }

    # Mögliche Statuswerte für Aufgaben
    STATUS_CHOICES = {
        "to_do": "TO_DO",
        "in_progress": "IN_PROGRESS",
        "in_review": "IN_REVIEW",
        "finished": "FINISHED",
    }

    # Titel der Aufgabe, max. 30 Zeichen
    title = models.CharField(max_length=30)

    # Beschreibung, optional, max. 500 Zeichen
    description = models.TextField(max_length=500, blank=True)

    # Zugehöriges Board (jede Aufgabe gehört zu genau einem Board)
    board = models.ForeignKey(Board, on_delete=models.CASCADE)

    # Priorität (ein Buchstabe, z. B. 'H', 'M', 'L')
    priority = models.CharField(max_length=1, choices=PRIORITY_CHOICES.items())

    # Status der Aufgabe
    status = models.CharField(max_length=30, choices=STATUS_CHOICES.items())

    # Fälligkeitsdatum
    due_date = models.DateField()

    # Ersteller der Aufgabe
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="created_tasks")

    # Zugewiesene Nutzer (Assignees) – viele-zu-viele Beziehung
    assignees = models.ManyToManyField(User, related_name='assigned_tasks')

    # Reviewer – viele-zu-viele Beziehung
    reviewers = models.ManyToManyField(User, related_name='reviewed_tasks')


# Modell für einen Kommentar zu einer Aufgabe
class Comment(models.Model):
    # Verknüpfung mit der Aufgabe, zu der der Kommentar gehört
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="comments")

    # Autor des Kommentars
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    # Inhalt des Kommentars (max. 1000 Zeichen)
    content = models.TextField(max_length=1000)

    # Zeitstempel bei Erstellung (wird automatisch gesetzt)
    created_at = models.DateTimeField(auto_now_add=True)
