from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.utils import timezone
# Create your models here.

class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank = True)
    created = models.DateTimeField(auto_now_add=True)
    datecompleted = models.DateTimeField(null = True)
    bygpt = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self) -> str:
        return self.title + "-for " + self.user.username
    
class Messages(models.Model):
    text = models.TextField(blank = True)
    created = models.DateTimeField(auto_now_add=True)
    bygpt = models.BooleanField(default = False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
class CounselorData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    userdescription = models.TextField(blank=True)
    usercontacts = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    
    
        
        
class ContactUs(models.Model):
    mail = models.CharField(max_length=100)
    subject = models.CharField(max_length=100)
    text = models.TextField(blank = True)
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    
class Friends(models.Model):
    user1 = models.CharField(max_length=100)
    user2 = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)