from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.core.validators import MinLengthValidator,MaxLengthValidator
# Create your models here.


class User(AbstractUser):
    mobile_number=models.CharField(max_length=10,unique=True,validators=[MaxLengthValidator(10),MinLengthValidator(10)])
    admin=models.BooleanField(default=False)

    def __str__(self):
        return self.username




class EmailBackend(object):
    def authenticate(self,request,username=None,password=None,**kwargs):
        User=get_user_model()
        try:
            user=User.objects.get(email=username)
        except User.DoesNotExist:
            return None
        else:
            if getattr(user,'is_active',False) and user.check_password(password):
                return user
        return None

    def get_user(self,user_id):
        User=get_user_model()
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None


