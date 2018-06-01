from django.contrib.auth import update_session_auth_hash

from rest_framework import serializers
from datetime import datetime
from .models import User, Post,Like

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

    class Meta:
        model = User
        fields = (
            'id', 'email', 'username','password')

class PostSerializer(serializers.ModelSerializer):
    #creator = serializers.PrimaryKeyRelatedField()
    #date = serializers.DateTimeField(default=datetime.now())
    likes = serializers.PrimaryKeyRelatedField(
        many=True,read_only=True)
    #print(len(likes))
    #user = serializers.Field(source='user.id')
    class Meta:
        model = Post
        fields = ('user','title','body','likes','id','created_at')