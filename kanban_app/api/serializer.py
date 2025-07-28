from rest_framework import serializers
from kanban_app.models import Board, Task, Comment
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404


class SimpleUserSerializer(serializers.ModelSerializer):
    """
    A simplified serializer for the User model.

    Includes only basic identifying fields: ID, username, and email.
    Useful for nested representation in related objects.
    """
    class Meta:
        model = User  
        fields = ['id', 'username', 'email'] 


class BoardSerializer(serializers.ModelSerializer):
    """
    Serializer for the Board model.

    Includes custom fields for:
    - member_ids: IDs of assigned members (write-only)
    - member_count: total number of members
    - ticket_count: total number of tasks in the board
    - high_priority_count: tasks marked with high priority
    - tasks_to_do_count: tasks with status "to_do"
    """

    member_ids = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        many=True,
        write_only=True,
        source='members'  
    )

    member_count = serializers.SerializerMethodField()
    ticket_count = serializers.SerializerMethodField()
    high_priority_count = serializers.SerializerMethodField()
    tasks_to_do_count = serializers.SerializerMethodField()

    class Meta:
        model = Board
        fields = [
            'id', 'title', 'member_count', 'member_ids',
            'ticket_count', 'high_priority_count',
            'tasks_to_do_count', 'owner_id'
        ]
        read_only_fields = ['owner']

    def get_member_count(self, obj):
        """
        Returns the number of members assigned to the board.
        """
        return obj.members.count()

    def get_ticket_count(self, obj):
        """
        Returns the total number of tasks associated with the board.
        """
        return obj.task_set.count()

    def get_high_priority_count(self, obj):
        """
        Returns the number of tasks on the board with high priority.
        """
        return obj.task_set.filter(priority='H').count()

    def get_tasks_to_do_count(self, obj):
        """
        Returns the number of tasks on the board with status 'to_do'.
        """
        return obj.task_set.filter(status='to_do').count()


class TaskSerializer(serializers.ModelSerializer):
    """
    Serializer for the Task model.

    Includes:
    - board_ids: write-only field to assign board
    - assignee_ids / reviewer_ids: write-only fields for assigning users
    - assignees / reviewers: read-only nested user representations
    """

    board = serializers.PrimaryKeyRelatedField(read_only=True)
    board_ids = serializers.PrimaryKeyRelatedField(
        queryset=Board.objects.all(),
        many=False,
        write_only=True,
        source='board'
    )

    assignees = SimpleUserSerializer(many=True, read_only=True)
    reviewers = SimpleUserSerializer(many=True, read_only=True)

    assignee_ids = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        many=True,
        write_only=True,
        source='assignees'
    )

    reviewer_ids = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        many=True,
        write_only=True,
        required=False,
        source='reviewers'
    )

    class Meta:
        model = Task  
        exclude = []  # Includes all fields from the model

    def create(self, validated_data):
        """
        Creates a new Task instance with assigned assignees and reviewers.

        Args:
            validated_data (dict): Validated input data.

        Returns:
            Task: The newly created Task instance.
        """
        assignees = validated_data.pop('assignees', [])
        reviewers = validated_data.pop('reviewers', [])

        task = Task.objects.create(**validated_data)
        task.assignees.set(assignees)
        task.reviewers.set(reviewers)

        return task

    def update(self, instance, validated_data):
        """
        Updates an existing Task instance and reassigns assignees/reviewers if provided.

        Args:
            instance (Task): The task instance to update.
            validated_data (dict): Validated input data.

        Returns:
            Task: The updated Task instance.
        """
        assignees = validated_data.pop('assignees', None)
        reviewers = validated_data.pop('reviewers', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if assignees is not None:
            instance.assignees.set(assignees)

        if reviewers is not None:
            instance.reviewers.set(reviewers)

        return instance


class CommentSerializer(serializers.ModelSerializer):
    """
    Serializer for the Comment model.

    Includes a custom author field that returns the user's full name,
    or their username if full name is not set.
    """

    author = serializers.SerializerMethodField()

    class Meta:
        model = Comment 
        fields = ['id', 'created_at', 'author', 'content']

    def get_author(self, obj):
        """
        Returns the full name of the comment's author if available, otherwise the username.

        Args:
            obj (Comment): The comment instance.

        Returns:
            str: Full name or username of the author.
        """
        name = obj.author.get_full_name()
        return name if name else obj.author.username
