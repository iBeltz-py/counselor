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
    
    
class FriendList(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete = models.CASCADE, related_name="user")
    friends = models.ManyToManyField(settings.AUTH_USER_MODEL, blank = True)
    def __str__(self) -> str:
        return self.user.username
    def add_friend(self,account):
        if not account in self.friends.all():
            self.friends.add(account)
            self.save
    def remove_friend(self,account):
        if account in self.friends.all():
            self.friends.remove(account)
            self.save()
            
    def unfriend(self,removee):
        remover_friends_list = self 
        remover_friends_list.remove_friend(removee)
        
        friends_list = FriendList.objects.get(user = removee)
        friends_list.remove_friend(self.user)
        
    def is_mutual_friend(self,friend):
        if friend in self.friends.all():
            return True
        return False
    
    def get_friends(self):
        return self.friends
    
class FriendRequest(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="sender")
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="receiver")
    
    is_active = models.BooleanField(blank = True, null = False, default = True)
    
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return self.sender.username
    
    def accept(self):
        receiver_friend_list = FriendList.objects.get(user = self.receiver)
        if receiver_friend_list:
            receiver_friend_list.add_friend(self.sender)
            sender_friend_list = FriendList.objects.get(user=self.sender)
            
            if sender_friend_list:
                sender_friend_list.add_friend(self.receiver)
                self.is_active = False
                self.save()
            
    def decline(self):
        self.is_active = False
        self.save()
        
    def cancel(self):
        self.is_active= False
        self.save()
        
        
class ContactUs(models.Model):
    mail = models.CharField(max_length=100)
    subject = models.CharField(max_length=100)
    text = models.TextField(blank = True)
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)