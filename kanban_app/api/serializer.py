# Importiert das Serialisierungsmodul von Django REST Framework
from rest_framework import serializers

# Importiert die Modelle aus der Kanban-App
from kanban_app.models import Board, Task, Comment

# Importiert das eingebaute User-Modell von Django
from django.contrib.auth.models import User

# Hilfsfunktion zum sicheren Abrufen eines Objekts (gibt 404 zurück, wenn nicht gefunden)
from django.shortcuts import get_object_or_404


# Serializer zur Darstellung eines einfachen Users (z. B. für Aufgaben oder Kommentare)
class SimpleUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User  # Nutzt das eingebaute User-Modell
        fields = ['id', 'username', 'email']  # Gibt nur ausgewählte Felder aus


# Serializer für Boards (Kanban-Boards)
class BoardSerializer(serializers.ModelSerializer):

    # Ermöglicht das Setzen von Mitgliedern über deren IDs beim Erstellen/Ändern (write_only)
    member_ids = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        many=True,
        write_only=True,
        source='members'  # Mapped auf das tatsächliche Feld im Modell: `members`
    )

    # Zusätzliche Felder, die automatisch berechnet werden (read-only)
    member_count = serializers.SerializerMethodField()         # Anzahl Mitglieder
    ticket_count = serializers.SerializerMethodField()         # Anzahl Aufgaben
    high_priority_count = serializers.SerializerMethodField()  # Anzahl Aufgaben mit hoher Priorität
    tasks_to_do_count = serializers.SerializerMethodField()    # Anzahl Aufgaben im Status "to_do"

    class Meta:
        model = Board  # Verwendetes Modell
        fields = [
            'id', 'title', 'member_count', 'member_ids',
            'ticket_count', 'high_priority_count',
            'tasks_to_do_count', 'owner_id'
        ]
        read_only_fields = ['owner']  # Das Owner-Feld kann nicht über die API verändert werden

    # Gibt Anzahl der Mitglieder zurück
    def get_member_count(self, obj):
        return obj.members.count()

    # Gibt Anzahl der Aufgaben zurück
    def get_ticket_count(self, obj):
        return obj.task_set.count()

    # Gibt Anzahl der Aufgaben mit Priorität "H" (High) zurück
    def get_high_priority_count(self, obj):
        return obj.task_set.filter(priority='H').count()

    # Gibt Anzahl der offenen Aufgaben zurück (Status = "to_do")
    def get_tasks_to_do_count(self, obj):
        return obj.task_set.filter(status='to_do').count()


# Serializer für Aufgaben (Tasks)
class TaskSerializer(serializers.ModelSerializer):
    # Board-ID (nur lesbar)
    board = serializers.PrimaryKeyRelatedField(read_only=True)

    # Zum Setzen der Board-ID beim Erstellen (write_only)
    board_ids = serializers.PrimaryKeyRelatedField(
        queryset=Board.objects.all(),
        many=False,
        write_only=True,
        source='board'  # schreibt ins Feld `board`
    )

    # Assignees und Reviewer werden als eingebettete Benutzer dargestellt (read-only)
    assignees = SimpleUserSerializer(many=True, read_only=True)
    reviewers = SimpleUserSerializer(many=True, read_only=True)

    # Zum Setzen von Assignee-IDs (write-only)
    assignee_ids = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        many=True,
        write_only=True,
        source='assignees'  # schreibt ins Feld `assignees`
    )

    # Zum Setzen von Reviewer-IDs (optional, write-only)
    reviewer_ids = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        many=True,
        write_only=True,
        required=False,
        source='reviewers'  # schreibt ins Feld `reviewers`
    )

    class Meta:
        model = Task  # Modell, das serialisiert wird
        exclude = []  # Keine Felder ausschließen (alles wird serialisiert)

    # Erstellen einer neuen Aufgabe mit Assignees und Reviewern
    def create(self, validated_data):
        assignees = validated_data.pop('assignees', [])  # Entnimmt Assignees aus den Daten
        reviewers = validated_data.pop('reviewers', [])  # Entnimmt Reviewer aus den Daten

        task = Task.objects.create(**validated_data)  # Erstellt die Aufgabe
        task.assignees.set(assignees)  # Setzt die Assignees
        task.reviewers.set(reviewers)  # Setzt die Reviewer

        return task

    # Aktualisiert eine bestehende Aufgabe (inkl. Assignees & Reviewer)
    def update(self, instance, validated_data):
        assignees = validated_data.pop('assignees', None)  # Optional: neue Assignees
        reviewers = validated_data.pop('reviewers', None)  # Optional: neue Reviewer

        # Setzt alle anderen Felder
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Setzt neue Assignees, falls angegeben
        if assignees is not None:
            instance.assignees.set(assignees)

        # Setzt neue Reviewer, falls angegeben
        if reviewers is not None:
            instance.reviewers.set(reviewers)

        return instance


# Serializer für Kommentare
class CommentSerializer(serializers.ModelSerializer):
    # Gibt den Autor als vollständigen Namen oder Username zurück
    author = serializers.SerializerMethodField()

    class Meta:
        model = Comment  # Kommentarmodell
        fields = ['id', 'created_at', 'author', 'content']  # Felder, die serialisiert werden

    # Ermittelt, wie der Autorname dargestellt wird
    def get_author(self, obj):
        name = obj.author.get_full_name()  # Versucht, den vollständigen Namen zu bekommen
        return name if name else obj.author.username  # Fallback: Benutzername