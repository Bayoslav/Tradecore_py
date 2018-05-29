from django.contrib.auth import update_session_auth_hash

from rest_framework import serializers
from datetime import datetime
from .models import User, Post

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'id', 'email', 'username')

class PostSerializer(serializers.ModelSerializer):
    #creator = serializers.PrimaryKeyRelatedField()
    #date = serializers.DateTimeField(default=datetime.now())
    likes = serializers.HyperlinkedRelatedField(
        many=True,read_oonly=True)
    class Meta:
        model = Post
        fields = ('author','title','body','id','likes','created_at')