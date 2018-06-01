from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager,PermissionsMixin
from django.utils import timezone as timezone
import jwt
from datetime import timedelta,datetime
from TC_task import settings
import pytz,clearbit


class UserManager(BaseUserManager):
    def create_user(self, email,username,password=None,dada=None, **kwargs):
        # Ensure that an email address is set
        #print(kwargs)
        if not email:
            raise ValueError('Users must have a valid e-mail address')
        # Ensure that a username is set
        #print(email)
        #password = kwargs.get('password')
        #print(password)
        clearbit.key = settings.clearbit_key
    
        extra_data = clearbit.Person.find(email=email, stream=True)
        if(extra_data == None):
            extra_data = "{}"
        user = self.model(
            email=self.normalize_email(email),
            username=username,
            extra_data=extra_data
           # enrichjson= enrichjson,
        )
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, username, email, password=None, **kwargs):
        
        #username = kwargs.get('username')
        user = self.create_user(email, username,password, kwargs)
        #user.is_admin = True
        user.is_staff = True
        user.is_superuser = True 
        user.save()

        return user

class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(unique=True, max_length=60)
    name = models.CharField(max_length=60)
    email = models.EmailField(unique=True) 
    is_active = models.BooleanField(default=True)
    data = models.CharField(max_length=10000) #If I was using PostgreSQL I would have put JSONField instead.
    #is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    date_created = models.DateTimeField(default=timezone.now)
    objects = UserManager()
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    extra_data = models.CharField(max_length=900,default="{}") #would use JSONField for this if I was using PostgreSQL!!!
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']
    def generate_jwt_token(self):
        """
        Generates a JSON Web Token that stores this user's ID and has an expiry
        date set to 60 days into the future.
        """
        dt = datetime.now() + timedelta(days=60)

        token = jwt.encode({
            'id': self.pk,
            'exp': int(dt.strftime('%s'))
        }, settings.SECRET_KEY, algorithm='HS256')

        return token.decode('utf-8')


class Post(models.Model):
    title = models.CharField(max_length=120)
    body = models.TextField(max_length=9000)
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
class Like(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    post = models.ForeignKey('Post',related_name='likes', on_delete=models.CASCADE)
    date = models.DateTimeField('date liked',auto_now_add=True)

