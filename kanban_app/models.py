from django.db import models
from django.contrib.auth.models import User


class Board(models.Model):
    """
    Represents a Kanban board where tasks are organized.

    Attributes:
        title (str): The title of the board.
        members (ManyToMany[User]): Users who are members of the board.
        owner (User): The user who owns and manages the board.
    """
    title = models.CharField(max_length=30)
    members = models.ManyToManyField(User, related_name='member_boards')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='boards')

    def __str__(self):
        return self.title


class Task(models.Model):
    """
    Represents a task within a board.

    Attributes:
        title (str): Title of the task.
        description (str): Detailed description of the task (optional).
        board (Board): The board to which this task belongs.
        priority (str): Priority level of the task. Choices: High, Medium, Low.
        status (str): Current status of the task. Choices: To Do, In Progress, In Review, Finished.
        due_date (date): The due date for task completion.
        owner (User): The user who created the task.
        assignees (ManyToMany[User]): Users assigned to work on the task.
        reviewers (ManyToMany[User]): Users assigned to review the task.
    """

    PRIORITY_CHOICES = {
        "high": "HIGH",
        "medium": "MEDIUM",
        "low": "LOW",
    }

    STATUS_CHOICES = {
        "to_do": "TO_DO",
        "progress": "IN_PROGRESS",
        "review": "IN_REVIEW",
        "finished": "FINISHED",
    }

    title = models.CharField(max_length=30)
    description = models.TextField(max_length=500, blank=True)
    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES.items())
    status = models.CharField(max_length=30, choices=STATUS_CHOICES.items())
    due_date = models.DateField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="created_tasks")
    assignees = models.ManyToManyField(User, related_name='assigned_tasks')
    reviewers = models.ManyToManyField(User, related_name='reviewed_tasks')

    def __str__(self):
        return self.title


class Comment(models.Model):
    """
    Represents a comment made on a task.

    Attributes:
        task (Task): The task to which this comment belongs.
        author (User): The user who authored the comment.
        content (str): The textual content of the comment.
        created_at (datetime): Timestamp when the comment was created.
    """
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
