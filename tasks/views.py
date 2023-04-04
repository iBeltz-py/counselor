from django.shortcuts import render
from django.db import models
from django.shortcuts import redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import TaskForm
from .models import Task
from .forms import CounselorDataForm
from .models import CounselorData
from .forms import MessagesForm
from .models import Messages
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .apis import get_userapi
from .apis import get_orgid
import openai
from .models import FriendList
from .models import FriendRequest
from .forms import ContactUsForm
# Create your views here.
def home(request):
    return render(request,"home.html")
def signup(request):
    if request.method == "GET":
        return render(request,"signup.html",{
            "form":UserCreationForm
        })
    else: 
        if request.POST["password1"] == request.POST["password2"]:
            print(request.POST)
            try:
                #User = User.objects.create_user(username=request.POST["username"],password=request.POST["password1"])
                user = User.objects.create_user(username = request.POST['username'], password = request.POST['password1'])

                user.save()
                login(request, user)
                return redirect("home")
            except IntegrityError:
                return render(request,"signup.html",{
                    "form": UserCreationForm,
                    "error": "User already exists."
                }) 

        else:
            return render(request,"signup.html",{
                
                "form":UserCreationForm,
                "error":"Both passwords do not match."
            })  
@login_required
def signout(request):
    logout(request)
    return redirect("home")
def signin(request):
    if request.method =="GET":
        return render(request,"signin.html",{
            "form":AuthenticationForm
        })
        
    else:
        user = authenticate(request,username = request.POST["username"], password = request.POST["password"])
        print("hi")
        if user is None:
            return render(request,"signin.html",{
                "form":AuthenticationForm,
                "error": "Username or password is incorrect."
            })    
        else:
            login(request,user)
            return redirect("home")       
@login_required
def tasks(request):
    tasks = Task.objects.filter(user = request.user, datecompleted__isnull=True)
    return render(request,"tasks.html",{
        "tasks":tasks
    })
@login_required
def create_task(request):
    if request.method == "GET":
        return render(request,"create_task.html",{
            "form": TaskForm
        })
    else:
        try:
            form = TaskForm(request.POST)
            
            new_task = form.save(commit = False)
            new_task.user = request.user
            print(new_task)
            new_task.save()
            return redirect("tasks")
        except ValueError:
            return render(request,"create_task.html",{
            "form": TaskForm,
            "error": "Something did not work."
        })                 
@login_required
def task_detail(request,task_id):
    task = get_object_or_404(Task, pk = task_id)
    return render(request,"task_detail.html",{
        "task":task
    })
@login_required    
def task_complete(request, task_id):
    task = get_object_or_404(Task,pk = task_id, user = request.user)
    if request.method == "POST":
        task.datecompleted = timezone.now()
        task.save()
        return redirect("tasks")
@login_required    
def delete_task(request,task_id):
    task = get_object_or_404(Task,pk = task_id, user = request.user)
    if request.method == "POST":
       task.delete() 
       return redirect("tasks")
@login_required       
def completed_tasks(request):
    tasks = Task.objects.filter(user = request.user, datecompleted__isnull=False)
    return render(request,"tasks_completed.html",{
        "tasks":tasks
    })
    
def chat(request):
    messages = Messages.objects.filter(user = request.user)
    res = messages[::-1]
    if messages == None:
        
        pass
    if request.method == "GET":
        return render(request, "chat.html", {
            "messages": res,
        })
    else:
        openai.api_key = get_userapi()
        openai.organization= get_orgid()
        message = Messages.objects.create(
        text = request.POST.get("text"),  
        created =   models.DateTimeField(auto_now_add=True),
        bygpt = False,
        user = request.user   
        )
        
        
        context = {
            "role" : "system", 
            "content" : """
                You are a psychologist who is conducting a diagnosis on a patient. You must be aware of all their problems and limit yourself to requesting information 
                and asking questions about these problems. This is a social assistance website, designed to help people improve their personal relationships. You should have a 
                friendly and calm manner of speaking, making your patient feel comfortable, but not talking too much. Limit yourself to asking questions and gathering information 
                in order to make a diagnosis.
            """,
        }
        mensajes = [context]
        for message in messages:
            if message.bygpt == True:
                new_message = {"role" : "assistant", "content":message.text}    
                mensajes.append(new_message)
            else:
                new_message = {"role" : "user", "content":message.text}    
                mensajes.append(new_message)
        response = openai.ChatCompletion.create(
            model = "gpt-3.5-turbo", messages = mensajes,
        )     
        response_content = response.choices[0].message.content 
        message = Messages.objects.create(
        text = response_content,  
        created =   models.DateTimeField(auto_now_add=True),
        bygpt = True,
        user = request.user   
        )
        messages = Messages.objects.filter(user = request.user)
        res = messages[::-1]
        return render(request, "chat.html", {
            "messages": res,
        })        

def asktask(request):
    openai.api_key = get_userapi()
    openai.organization= get_orgid()
    user_data = CounselorData.objects.filter(user = request.user)
    if user_data:
        pass
    else:
        pass
        context = {
            "role" : "system", 
            "content" : """
                You are a psychologist who is conducting a diagnosis on a patient. You must be aware of all their problems and limit yourself to requesting information 
                and asking questions about these problems. This is a social assistance website, designed to help people improve their personal relationships. You should have a 
                friendly and calm manner of speaking, making your patient feel comfortable, but not talking too much. Limit yourself to asking questions and gathering information 
                in order to make a diagnosis.
            """,
        }
        mensaje = [context]
        messages = Messages.objects.filter(user = request.user)
        for index in messages:
            mensaje.append({"role" : "user", "content": index.text})
    
        context2 = {
            "role" : "system", 
            "content" : """
                Now, based on all the details you've learned about the user in this conversation, create a very detailed description of their situation 
                (problems, thought patterns, personality, etc.)
            """,
        }
        mensaje.append(context2)
        #new_message = {"role" : "user", "content": "Please, tell me a description of my situation AS MUCH DETAILED AS POSSIBLE."}
        #mensaje.append(new_message)    
        
        response = openai.ChatCompletion.create(
            model = "gpt-3.5-turbo", messages = mensaje,
        ) 
        response_content = response.choices[0].message.content 
        print(response_content)
        return render(request,"tasks.html")
        
    user_data = CounselorData.objects.filter(user = request.user)
    description = user_data[0].userdescription
    print(description)
    context = {
        "role" : "system", 
        "content" : """
            You are a psychologist who is conducting a diagnosis on a patient. You must be aware of all their problems and limit yourself to requesting information 
            and asking questions about these problems. This is a social assistance website, designed to help people improve their personal relationships. You should have a 
            friendly and calm manner of speaking, making your patient feel comfortable, but not talking too much. Limit yourself to asking questions and gathering information 
            in order to make a diagnosis.
        """,
        }
    context2 = {
        "role" : "system", 
        "content" : """
            Create a VERY VERY VERY specific task, for slowly improving the situiation of this person, (I mean very specific, task that is not
            too direct, for example, is someone feels his marriage is losing magic, a task example would be something like: Send him a good morning message).
            The situation of the user is as follows: 
            
        """ + description,
    }
    mensajes = [context,context2]
    response = openai.ChatCompletion.create(
         model = "gpt-3.5-turbo", messages = mensajes,
    ) 
    response_content = response.choices[0].message.content 
    print(response_content)        
    return render(request,"tasks.html")



def contacts(request):
    print("hi")
    return render(request,"contacts.html",{
        "friends": ["Julian","Marta","kslfj"]
    })


def account_search_view(request,*args,**kwargs):
    context = {}
    if request.method == "POST":
        search_query = request.POST.get("search")
        if len(search_query)>0:
            search_results = User.objects.filter(username__icontains = search_query)
            #user = request.user
            accounts = [] # [(account1, True), (account2,False)]
            for account in search_results:
                accounts.append((account, False))
            context["accounts"] = accounts
    return render(request, "search_results.html", context)
            
            
def contact_us(request):
    if request.method == "GET":
        return render(request,"contact_us.html",{
            "form": ContactUsForm
        })
    else:
        try:
            form = ContactUsForm(request.POST)
            
            new_message = form.save(commit = False)
            new_message.user = request.user
            new_message.save()

            
            return redirect("home")
        except ValueError:
            print(ValueError)
            return render(request,"contact_us.html",{
            "form": ContactUsForm,
            "error": "Something did not work."
        })         

