from rest_framework import serializers
from kanban_app.models import Board
from auth_app.api.serializers import UserProfileSerializer
from auth_app.models import User

class BoardSerializer(serializers.Serializer):
    id= serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=30)
    members= UserProfileSerializer(many=True,write_only=True) 

    def create(self, validated_data):
        return Board.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
         instance.title = validated_data.get('title', instance.title)
        
         instance.save()
         return instance
    
    
class BoardCreateSerializer(serializers.Serializer):
     title = serializers.CharField(max_length=30)
     members= serializers.ListField(child=serializers.IntegerField(),write_only=True) 

     def validate_boards(self,value):
        members=User.objects.filter(id__in=value)
        if len(members) != len(value):
            raise serializers.ValidationError("some members id not found")
        
     def create(self,validated_data):
         member_ids=validated_data.pop('members')
         board= Board.objects.create(**validated_data)
         members = User.objects.filter(id__in=member_ids)
         board.members.set(members)
         return board
       