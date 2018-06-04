from django.shortcuts import render
from .models import User,Post,Like
# Create your views here.
from rest_framework.request import Request
from .serializers import UserSerializer,PostSerializer,LikeSerializer
from rest_framework.views import APIView
from rest_framework import generics,status
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.response import Response
import requests,json
from TC_task.settings import API_KEY


class UserPosts(APIView):
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticated,)
    def get(self, request,user_id):
        user = User.objects.get(id=user_id)
        queryset = Post.objects.filter(user=user)
        serializer = PostSerializer(queryset,many=True)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
    
class LikeView(APIView):
    serializer_class = LikeSerializer
    permission_classes = (IsAuthenticated,)
    def get(self, request,post_id=0):
        if (post_id==0): 
            queryset = Like.objects.all()
            #queryset = self.get_queryset()  
        else:
            post = Post.objects.get(id=post_id)
            queryset = Like.objects.get(post=post)
        serializer = LikeSerializer(queryset,many=True)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
    def post(self, request):
            #print(post_id)
            post_id = request.POST.get('post_id')
            post_obj = Post.objects.get(id=post_id)
            #user_id = request.user.id
            data = {
                    "message" : "Success"
                }
            try:
                dad = Like.objects.get(user=request.user,post=post_obj)
            except:
                obj = Like(user=request.user,post=post_obj)
                obj.save()
            else:
                dad.delete()

            return Response(data,status=status.HTTP_201_CREATED)
        
class UserView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)
    def post(self, request):
        email = request.data['email']
        url = 'https://api.hunter.io/v2/email-verifier?email=' + email + '&api_key=' + API_KEY
        r = requests.get(url)
        #print(r.text)
        dzejson = json.loads(r.text)
        try:
            score = dzejson.get('data').get('score')
        except:
            score=51
            print("Hunter API LIMIT REACHED.")
        #doing it like this because hunter has changed it's privacy policy recently hence the api is unclear'''
        
        if(int(score)>50): 
            serializer = self.serializer_class(data=request.data)
            
        else:
            data = {"message" : "Email undeliverable"}
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        
        
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
        #print(queryset)
        serializer_context = {
            'request': (request),
        }
        #queryset['num_likes'] = len(queryset.get('likes'))
       
        serializer = PostSerializer(queryset, many=True,context=serializer_context)
        #serializer.data['num_likes'] = len(serializer.data['likes'])
        return Response(serializer.data)
