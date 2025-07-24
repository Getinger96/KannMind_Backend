from rest_framework import serializers
from kanban_app.models import Board, Task, Comment
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404



class SimpleUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email'] 

class BoardSerializer(serializers.ModelSerializer):
    
    member_ids = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        many=True,
         write_only=True,
         source= 'members'
    )
   


    member_count= serializers.SerializerMethodField()
    ticket_count = serializers.SerializerMethodField()
    high_priority_count = serializers.SerializerMethodField()
    tasks_to_do_count = serializers.SerializerMethodField()

    class Meta:
        model = Board
        fields=['id','title','member_count','member_ids','ticket_count','high_priority_count','tasks_to_do_count','owner_id']
        read_only_fields= ['owner']

    def get_member_count(self,obj):
        return obj.members.count()
    
    def get_ticket_count(self, obj):
        return obj.task_set.count()
    
    def get_high_priority_count(self, obj):
        return obj.task_set.filter(priority='H').count()
    
    def get_tasks_to_do_count(self, obj):
        return obj.task_set.filter(status='to_do').count()
        



    


class TaskSerializer(serializers.ModelSerializer):
    board=serializers.PrimaryKeyRelatedField(read_only=True)
    board_ids = serializers.PrimaryKeyRelatedField(
        queryset=Board.objects.all(),
        many=False,
        write_only=True,
        source='board'
    )
    assignees = SimpleUserSerializer(many=True, read_only=True)
    reviewers = SimpleUserSerializer(many=True, read_only=True)

    # Write-only Felder für IDs, source verweist auf Modelfeld
    assignee_ids = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        many=True,
        write_only=True,
        source='assignees'   # source hier, weil Feldname assignee_ids != Modelfeld assignees
    )
    reviewer_ids = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        many=True,
        write_only=True,
        required=False,
        source='reviewers'  # ebenso hier
    )
    

   
    class Meta:
        model = Task
        exclude=[]
    
    def create(self, validated_data):
     assignees = validated_data.pop('assignees', [])
     reviewers = validated_data.pop('reviewers', [])

     task = Task.objects.create(**validated_data)

     task.assignees.set(assignees)
     task.reviewers.set(reviewers)

     return task

def update(self, instance, validated_data):
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
     author = serializers.SerializerMethodField()

     class Meta:
        model = Comment
        fields = ['id', 'created_at', 'author', 'content']

     def get_author(self, obj):
      name = obj.author.get_full_name()
      return name if name else obj.author.username