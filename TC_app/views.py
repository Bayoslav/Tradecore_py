from django.shortcuts import render
from .models import User,Post,Like
# Create your views here.
from rest_framework.request import Request
from .serializers import UserSerializer,PostSerializer
from rest_framework.views import APIView
from rest_framework import generics,status
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.response import Response

class LikeView(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request,post_id):
        print(post_id)
        post_obj = Post.objects.get(id=post_id)
        #user_id = request.user.id
        obj = Like(user=request.user,post=post_obj)
        obj.save()
        data = {
            "message" : "Success"
        }
        return Response(data)
class UserView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def list(self, request):
        # Note the use of `get_queryset()` instead of `self.queryset`
        queryset = self.get_queryset()
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)
#class Register(APIView):

class PostView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticated,)


    def post(self, request):
        if not request.data._mutable:
            request.data._mutable = True
        request.data['user'] = request.user.id
        print(request.data['user'])
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def list(self, request):
        # Note the use of `get_queryset()` instead of `self.queryset`
        queryset = self.get_queryset()
        print(queryset)
        serializer_context = {
            'request': (request),
        }
        #queryset['num_likes'] = len(queryset.get('likes'))
       
        serializer = PostSerializer(queryset, many=True,context=serializer_context)
        #serializer.data['num_likes'] = len(serializer.data['likes'])
        return Response(serializer.data)