from rest_framework import serializers
from kanban_app.models import Board,Task,Comment
from auth_app.models import User
from auth_app.api.serializers import UserSerializer



class SimplifiedUserSerializer(serializers.ModelSerializer):
    fullname = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'email', 'fullname']

    def get_fullname(self, obj):
        return f"{obj.first_name} {obj.last_name}".strip()

class BoardSerializer(serializers.ModelSerializer):
    members=serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        many=True,
        write_only=True,
    )
    owner_id=serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
       
    )
    member_count = serializers.SerializerMethodField()
    ticket_count = serializers.SerializerMethodField()
    tasks_to_do_count = serializers.SerializerMethodField()
    tasks_high_prio_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Board
        fields = ['id','title','members','owner_id', 'member_count', 'ticket_count', 'tasks_to_do_count', 'tasks_high_prio_count']
    
    def get_member_count(self, obj):
        return obj.members.count()
    
    def get_ticket_count(self, obj):
        return obj.tasks.count()

    def get_tasks_to_do_count(self, obj):
        return obj.tasks.filter(status='to_do').count()

    def get_tasks_high_prio_count(self, obj):
        return obj.tasks.filter(priority='high').count()
    


class BoardCreateSerializer(serializers.ModelSerializer):
    members=serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        many=True,
        write_only=True,
    )
    
       
    class Meta:
        model = Board
        fields = ['title','members']


class TasksofBoardSerializer(serializers.ModelSerializer):
     comments_count = serializers.SerializerMethodField()
     assignees=SimplifiedUserSerializer(many=True,read_only=True) 
     reviewers=SimplifiedUserSerializer(many=True,read_only=True)

     class Meta:
        model = Task
        fields = ['id','title','description','status','priority','assignees','reviewers','due_date','comments_count']
    
     def get_comments_count(self, obj):
         return obj.comments.count()  


       
    
class BoardDetailSerializer(serializers.ModelSerializer):
    members= UserSerializer(many=True,read_only=True)
    owner_id=serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),)
    tasks=TasksofBoardSerializer(many=True,read_only=True)
    
    
    class Meta:
        model = Board
        fields = ['id','title','owner_id','members','tasks']



class BoardUpdateSerializer(serializers.ModelSerializer):
    owner_data=UserSerializer(read_only=True,source='owner')
    members_data= UserSerializer(many=True,read_only=True,source='members')
    

    class Meta:
        model = Board
        fields = ['id','title','owner_data','members_data']




class TaskCreateSerializer(serializers.ModelSerializer):
    assignee_id= serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        write_only=True
    )
    reviewer_id=serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        write_only=True
    )


    class Meta:
        model=Task
        exclude= ['assignees','reviewers']
    
    def create(self, validated_data):
        assignee = validated_data.pop('assignee_id')
        reviewer = validated_data.pop('reviewer_id')

        task = Task.objects.create(**validated_data)
        task.assignees.add(assignee)
        task.reviewers.add(reviewer)

        return task
    
    def update(self, instance, validated_data):
     assignee = validated_data.pop('assignee_id', None)
     reviewer = validated_data.pop('reviewer_id', None)

     # Update normale Felder
     for attr, value in validated_data.items():
        setattr(instance, attr, value)
     instance.save()

    # Update ManyToMany-Felder nur, wenn angegeben
     if assignee is not None:
        instance.assignees.set([assignee])
     if reviewer is not None:
        instance.reviewers.set([reviewer])

     return instance




class TaskSerializer(serializers.ModelSerializer):
    board=serializers.PrimaryKeyRelatedField( queryset=Board.objects.all(),
        )
    comments_count = serializers.SerializerMethodField()
    assignees=UserSerializer(many=True,read_only=True) 
    reviewers=UserSerializer(many=True,read_only=True) 


    class Meta:
        model=Task
        fields = [
            'id', 'board', 'title', 'description', 'status', 'priority',
            'assignees', 'reviewers', 'due_date', 'comments_count'
        ]

        
    def get_comments_count(self, obj):
         return obj.comments.count()  



class TaskDetailSerializer(serializers.ModelSerializer):
    assignees=UserSerializer(many=True,read_only=True) 
    reviewers=UserSerializer(many=True,read_only=True) 

   

    class Meta:
        model = Task
        fields = [
            'id', 'title', 'description', 'status', 'priority',
            'assignees', 'reviewers', 'due_date'
        ]

    


class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['content']



class CommentResponseSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'created_at', 'author', 'content']

    def get_author(self, obj):
        return obj.author.username
    





