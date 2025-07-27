# Importiert das path-Objekt, um URL-Routen zu definieren
from django.urls import path

# Importiert die Views, die mit den jeweiligen Routen verbunden werden
from .views import (
    BoardsView,
    TasksView,
    BoardDetailView,
    TaskDetailView,
    EmailCheckView,
    TasksAssignedToMeView,
    Tasksreviewing,
    TaskCommentListView,
    TaskCommentDeleteView
)

# Definiert die URL-Routen für die App
urlpatterns = [

    # GET, POST: Liste aller Boards oder neues Board erstellen
    path('boards/', BoardsView.as_view()),

    # GET, PUT, DELETE: Details, Aktualisierung oder Löschen eines bestimmten Boards (nach ID)
    path('boards/<int:pk>/', BoardDetailView.as_view()),

    # POST: Prüft, ob eine E-Mail-Adresse bereits existiert (z. B. bei Registrierung)
    path('email-check/', EmailCheckView.as_view()),

    # GET: Gibt alle Aufgaben zurück, die dem aktuell angemeldeten Nutzer zugewiesen sind
    path('tasks/assigned-to-me/', TasksAssignedToMeView.as_view()),

    # GET: Gibt Aufgaben zurück, bei denen der aktuelle User Reviewer ist
    path('tasks/reviewing/', Tasksreviewing.as_view()),

    # GET, POST: Liste aller Tasks oder neuen Task erstellen
    path('tasks/', TasksView.as_view()),

    # GET, PUT, DELETE: Details, Aktualisierung oder Löschen eines Tasks (nach ID)
    path('tasks/<int:pk>/', TaskDetailView.as_view()),

    # GET, POST: Liste oder Erstellen von Kommentaren zu einem bestimmten Task
    path('tasks/<int:pk>/comments/', TaskCommentListView.as_view()),

    # DELETE: Löschen eines spezifischen Kommentars innerhalb eines Tasks
    path('tasks/<int:pk>/comments/<int:comment_pk>/', TaskCommentDeleteView.as_view()),
]
