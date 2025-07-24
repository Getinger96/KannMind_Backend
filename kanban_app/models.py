from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Board(models.Model):
    title = models.CharField(max_length=30)
    members = models.ManyToManyField(User, related_name='member_boards')
    owner=models.ForeignKey(User,on_delete=models.CASCADE,related_name='boards')
    


    



class Task(models.Model):

     PRIORITY_CHOICES = {
        "H": "HIGH",
        "M": "MEDIUM",
        "L": "LOW",
    }

     STATUS_CHOICES = {
        "to_do": "TO_DO",
        "in_progress": "IN_PROGRESS",
        "in_review": "IN_REVIEW",
        "finished": "FINISHED",
    }

     title = models.CharField(max_length=30)
     description = models.TextField(max_length=500, blank=True)
     board = models.ForeignKey(Board, on_delete=models.CASCADE)
     priority = models.CharField(max_length=1, choices=PRIORITY_CHOICES.items())
     status = models.CharField(max_length=30, choices=STATUS_CHOICES.items())
     due_date = models.DateField()
     owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="created_tasks")

     assignees = models.ManyToManyField(User, related_name='assigned_tasks')
     reviewers = models.ManyToManyField(User, related_name='reviewed_tasks')


      
class Comment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    

