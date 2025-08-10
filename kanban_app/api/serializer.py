from rest_framework import serializers
from kanban_app.models import Board,Task,Comment
from auth_app.models import User
from auth_app.api.serializers import UserSerializer



class SimplifiedUserSerializer(serializers.ModelSerializer):
    """
    Vereinfachter User-Serializer, der nur ID, E-Mail und
    den vollständigen Namen zurückgibt.
    """
    fullname = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'email', 'fullname']

    def get_fullname(self, obj):
        """
        Kombiniert Vor- und Nachname zu einem vollständigen Namen.
        """
        return f"{obj.first_name} {obj.last_name}".strip()


class BoardSerializer(serializers.ModelSerializer):
    """
    Serializer zur Darstellung von Boards inklusive
    Mitglieder, Eigentümer sowie verschiedenen
    Zählwerten (Mitglieder, Tickets, Aufgabenstatus).
    """
    members = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        many=True,
        write_only=True,
    )
    owner_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
    )
    member_count = serializers.SerializerMethodField()
    ticket_count = serializers.SerializerMethodField()
    tasks_to_do_count = serializers.SerializerMethodField()
    tasks_high_prio_count = serializers.SerializerMethodField()

    class Meta:
        model = Board
        fields = ['id', 'title', 'members', 'owner_id', 'member_count', 'ticket_count', 'tasks_to_do_count', 'tasks_high_prio_count']

    def get_member_count(self, obj):
        """Gibt die Anzahl der Mitglieder zurück."""
        return obj.members.count()

    def get_ticket_count(self, obj):
        """Gibt die Anzahl aller Tasks im Board zurück."""
        return obj.tasks.count()

    def get_tasks_to_do_count(self, obj):
        """Gibt die Anzahl der Tasks im Status 'to_do' zurück."""
        return obj.tasks.filter(status='to_do').count()

    def get_tasks_high_prio_count(self, obj):
        """Gibt die Anzahl der Tasks mit hoher Priorität zurück."""
        return obj.tasks.filter(priority='high').count()


class BoardCreateSerializer(serializers.ModelSerializer):
    """
    Serializer zur Erstellung eines Boards mit Angabe
    von Titel und Mitgliedern (nur Schreibzugriff auf Mitglieder).
    """
    members = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        many=True,
        write_only=True,
    )

    class Meta:
        model = Board
        fields = ['title', 'members']


class TasksofBoardSerializer(serializers.ModelSerializer):
    """
    Serializer für Tasks eines Boards inklusive
    Anzahl der Kommentare sowie vereinfachte User-Informationen
    für Assignees und Reviewer.
    """
    comments_count = serializers.SerializerMethodField()
    assignees = SimplifiedUserSerializer(many=True, read_only=True)
    reviewers = SimplifiedUserSerializer(many=True, read_only=True)

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'status', 'priority', 'assignees', 'reviewers', 'due_date', 'comments_count']

    def get_comments_count(self, obj):
        """Gibt die Anzahl der Kommentare zu einer Task zurück."""
        return obj.comments.count()


class BoardDetailSerializer(serializers.ModelSerializer):
    """
    Detaillierter Serializer für Boards mit vollständigen
    Nutzerinformationen der Mitglieder und der Tasks.
    """
    members = UserSerializer(many=True, read_only=True)
    owner_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    tasks = TasksofBoardSerializer(many=True, read_only=True)

    class Meta:
        model = Board
        fields = ['id', 'title', 'owner_id', 'members', 'tasks']


class BoardUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer für Updates am Board, zeigt Besitzer und
    Mitglieder mit UserSerializer als schreibgeschützte Felder.
    """
    owner_data = UserSerializer(read_only=True, source='owner')
    members_data = UserSerializer(many=True, read_only=True, source='members')

    class Meta:
        model = Board
        fields = ['id', 'title', 'owner_data', 'members_data']


class TaskCreateSerializer(serializers.ModelSerializer):
    """
    Serializer zur Erstellung und Aktualisierung von Tasks,
    die 'assignee_id' und 'reviewer_id' als ForeignKey-IDs erwartet.
    """
    assignee_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        write_only=True
    )
    reviewer_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        write_only=True
    )

    class Meta:
        model = Task
        exclude = ['assignees', 'reviewers']

    def create(self, validated_data):
        """
        Erstellt eine Task und weist assignee und reviewer zu.
        """
        assignee = validated_data.pop('assignee_id')
        reviewer = validated_data.pop('reviewer_id')

        task = Task.objects.create(**validated_data)
        task.assignees.add(assignee)
        task.reviewers.add(reviewer)
        return task

    def update(self, instance, validated_data):
        """
        Aktualisiert Task-Felder und setzt assignee und reviewer,
        wenn neue Werte angegeben wurden.
        """
        assignee = validated_data.pop('assignee_id', None)
        reviewer = validated_data.pop('reviewer_id', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if assignee is not None:
            instance.assignees.set([assignee])
        if reviewer is not None:
            instance.reviewers.set([reviewer])

        return instance


class TaskSerializer(serializers.ModelSerializer):
    """
    Vollständiger Task-Serializer inklusive Board-Zuordnung,
    Nutzerinfos für Assignees und Reviewer sowie Kommentaranzahl.
    """
    board = serializers.PrimaryKeyRelatedField(queryset=Board.objects.all())
    comments_count = serializers.SerializerMethodField()
    assignees = UserSerializer(many=True, read_only=True)
    reviewers = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Task
        fields = [
            'id', 'board', 'title', 'description', 'status', 'priority',
            'assignees', 'reviewers', 'due_date', 'comments_count'
        ]

    def get_comments_count(self, obj):
        """Gibt die Anzahl der Kommentare zu einer Task zurück."""
        return obj.comments.count()


class TaskDetailSerializer(serializers.ModelSerializer):
    """
    Detaillierter Serializer für eine einzelne Task
    mit Assignees und Reviewern als verschachtelte User-Daten.
    """
    assignees = UserSerializer(many=True, read_only=True)
    reviewers = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Task
        fields = [
            'id', 'title', 'description', 'status', 'priority',
            'assignees', 'reviewers', 'due_date'
        ]


class CommentCreateSerializer(serializers.ModelSerializer):
    """
    Serializer zum Erstellen von Kommentaren mit nur dem Content-Feld.
    """

    class Meta:
        model = Comment
        fields = ['content']


class CommentResponseSerializer(serializers.ModelSerializer):
    """
    Serializer zur Rückgabe von Kommentaren mit Autor-Username.
    """
    author = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'created_at', 'author', 'content']

    def get_author(self, obj):
        """Gibt den Nutzernamen des Autors zurück."""
        return obj.author.username






