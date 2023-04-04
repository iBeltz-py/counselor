from django import forms
from .models import Task
from .models import Messages
from .models import CounselorData, ContactUs
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["title","description"]
        widgets = {
            'title': forms.TextInput(attrs={"class":"form-control", "placeholder":"Write a title"}),
            'description': forms.Textarea(attrs={"class":"form-control", "placeholder":"Write a description"})
        }
        
class MessagesForm(forms.ModelForm):
    class Messages:
        model = Messages
        fields = ["text","created","bygpt","created"]
        widgets = {
            'text': forms.TextInput(attrs={"class":"form-control", "placeholder":"Write a title"}),
            
        }
        
class CounselorDataForm(forms.ModelForm):
    class CounselorData:
        model = CounselorData
        fields = ["user","userdescription","usercontacts"]
        widgets = {
            "user": forms.TextInput(attrs={"class":"form-control", "placeholder":"Write a title"}),
            "description":forms.Textarea(attrs={"class":"form-control", "placeholder":"Write a description"}),            
        }
        
class UserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
    def save(self, commit = True):
        user = super(UserCreationForm,self).save(commit= False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user
    
    
class ContactUsForm(forms.ModelForm):
    class Meta:
        model = ContactUs
        fields = ["mail","subject","text"]
        widgets = {
            'email': forms.TextInput(attrs={"class":"form-control", "placeholder":"Write your email adress"}),
            'subject': forms.TextInput(attrs={"class":"form-control", "placeholder":"Write the subject"}),
            'text': forms.Textarea(attrs={"class":"form-control", "placeholder":"Tell us what you need"})
        }