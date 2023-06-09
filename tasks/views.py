from django.shortcuts import render
from django.db import models
from django.shortcuts import redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import TaskForm
from heyoo import WhatsApp
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
from .forms import ContactUsForm
from .models import Friends
from django.views.decorators.csrf import csrf_exempt
import json
import re
from django.core.management.base import BaseCommand
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
                user = User.objects.create_user(username = request.POST['username'], email = request.POST["email"], password = request.POST['password1'])

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
    userdesc = ""
    hehe = 0
    if hehe:
        pass
    else:
        CounselorData.objects.filter(user = request.user).delete()
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
        userdesc = response.choices[0].message.content 
        print(userdesc)
        data = CounselorData(user = request.user, userdescription = userdesc)
        data.save()
        #return render(request,"tasks.html")
        
    description = userdesc
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
    mensajes = []
    mensajes.append(context)

    context2 = {
        "role" : "system", 
        "content" : """
            You will now assign a task to the main user:
            Create a VERY VERY VERY specific task, for slowly improving the situiation of this person, (I mean very specific, task that is not
            too direct, for example, if someone feels his marriage is losing magic, a task example would be something like: Send him a good morning message).
            REMEMBER IT MUST BE A VERY SPECIFIC TASK, ONLY ONE TASK, NO MORE.
            The task must be written directly to the user, and it should be completed within a week.
            Do not type Task: at the beginning, nor quote the task, just say the task as a normal message.
            The situation of the user is as follows: 
            
        """ + description,
    }
    mensajes.append(context2)
    response = openai.ChatCompletion.create(
         model = "gpt-3.5-turbo", messages = mensajes,
    ) 
    task = response.choices[0].message.content 
    print(task)  
    task2 = {"role":"assistant", "content":task}
    mensajes.append(task2)
    context3 = {
        "role" : "system", 
        "content" : """
            Now tell me a short title for this task.
            JUST send the title, do not write any introduction, do not quote it or anything else.
            
        """ + description,
    }
    mensajes.append(context3)
    response = openai.ChatCompletion.create(
         model = "gpt-3.5-turbo", messages = mensajes,
    ) 
    title = response.choices[0].message.content 
    print(title)     
    new_task = Task(
        title = title, description=task, bygpt = True, user = request.user
    )
    new_task.save()  
    tasks = Task.objects.filter(user = request.user, datecompleted__isnull=True)
    return render(request,"tasks.html",{
        "tasks":tasks
    })
@login_required   
def contacts(request):
    friends = Friends.objects.filter(user1 = request.user)
    friends2 = Friends.objects.filter(user2 = request.user)
    return render(request,"contacts.html",{
        "friends": friends,
        "friends2":friends2
        
    })
@login_required   
def account_search_view(request):
    context = {}
    if request.method == "POST":
        search_query = request.POST.get("search")
        if len(search_query)>0:
            search_results = User.objects.filter(username__icontains = search_query)
            #user = request.user
            accounts = [] # [(account1, True), (account2,False)]
            friends = []
            friends = get_friends(request)
            isfriend = False
            for account in search_results:
                               
                for friend in friends:
                    if str(account) == str(friend):
                        isfriend = True
                        
                if isfriend == False:
                    accounts.append((account, isfriend))
            context["accounts"] = accounts
    return render(request, "search_results.html", context)
@login_required               
def get_friends(request):
    friends = []
    friends1 = Friends.objects.filter(user1=request.user)
    for acc in friends1:
        friends.append(acc)
        
    friends2 = Friends.objects.filter(user2=request.user)
    for acc in friends2:
        friends.append(acc)
    return friends
          
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
@login_required   
def add_contact(request,user2):
    f = Friends(user1 = request.user, user2 = user2)
    f.save()
    friends = Friends.objects.filter(user1 = request.user)
    friends2 = Friends.objects.filter(user2 = request.user)
    return render(request,"contacts.html",{
        "friends": friends,
        "friends2":friends2
        
    })
@login_required       
def remove_contact(request,user2):
    Friends.objects.filter(user1=request.user, user2=user2).delete()
    Friends.objects.filter(user2=request.user, user1=user2).delete()
    friends = Friends.objects.filter(user1 = request.user)
    friends2 = Friends.objects.filter(user2 = request.user)
    return render(request,"contacts.html",{
        "friends": friends,
        "friends2":friends2
        
    })
    
    
@csrf_exempt
def webhook(request):
    if request.method == 'GET':
        hub_challenge = request.GET.get('hub.challenge')
        return HttpResponse(hub_challenge)
    
    else:
        # Parse the request body from the POST
        body = json.loads(request.body.decode('utf-8'))

        # Check the Incoming webhook message
        #print(json.dumps(body, indent=2))

        # Check if the request is from WhatsApp API

        for entry in body['entry']:
            for change in entry['changes']:
                if change.get('value') and change['value'].get('messages'):
                    message = change['value']['messages'][0]
                    phone_number_id = change['value']['metadata']['phone_number_id']
                    sender = message['from']
                    text = message['text']['body']

        # Print sender and message text
        
        print("Sender: ", sender)
        print("Text: ", text) 
        
        if sender ==  34640520819:
            messages = []
            messages = Messages.objects.filter(user = "aritzjl")
            if not messages:
                
                context = {
                "role" : "system", 
                "content" : """
                    Todos los mensajes enviados por ti, están basados en la personalidad y forma de pensar de Aritz, eres el sustituto de aritz
                    y estás hecho para hacerte pasar por el en conversaciones de Whatsapp, debes basar tus respuestas, en la forma que has expresado todas tus respuestas
                    anteriores (las cuales están basadas en la personalidad de Aritz)
            """,
            }    
            with open('_chat.txt', 'r') as file:
                lines = file.readlines()

            # Inicializar arrays para mensajes de cada usuario

            # Expresión regular para buscar mensajes
            message_regex = re.compile(r'\d+/\d+/\d+\s\d+:\d+\s-\s')

            # Recorrer cada línea del archivo
            for line in lines:
                # Si la línea es un mensaje (no es una fecha o nombre de usuario)
                if message_regex.match(line):
                    # Quitar fecha y nombre de usuario del mensaje
                    message = re.sub(message_regex, '', line).strip()
                    # Si el mensaje fue enviado por Angel
                    if line.startswith('Angel'):
                        mensaje = Messages.objects.create(user = "aritzjl", text = message, bygpt = False)
                        mensaje.save()
                    # Si el mensaje fue enviado por Aritz
                    else:
                        mensaje = Messages.objects.create(user = "aritzjl", text = message, bygpt = True)
                        mensaje.save()      
            mensajes = []
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
            print(response_content)
            response_content = response.choices[0].message.content 
            message = Messages.objects.create(
            text = response_content,  
            created =   models.DateTimeField(auto_now_add=True),
            bygpt = True,
            user = "aritzjl"
            )
            webhook_url = 'https://secret-counselor-58lp.onrender.com/wsppwebhook/'
            messenger = WhatsApp('EAAIqRBAuZCO8BAEaAqyqrgXgeswH0epGfiHLKgZCJZCrAvVTarWQT2OLFGkGSqJ4tr1ZADLM5lgZAa9lfUogmzS7Xplg4vI8gShzYCAp1nZAHlNBEvpLlaZBfkF7NZCghE8tD6tWKtjAMqOJdyeBFoZAPrufPcgZCz1xyQAhvBs0ldq94vkCKLfd6E92RDTIdDbtXXtHycZB8er68crz2jFlsZAO',phone_number_id='104311552638205')
            messenger.send_message(response_content, '34640520819')
        return HttpResponse(status=200)
    
    
