from django.conf import settings
from django.contrib.auth.models import User
import random
from tasks.models import CounselorData, Task, Messages
import openai


def schedule_api():
    print("START TASK")
    users = User.objects.all()
    newtask_users = []
    for user in users:
        if random.randint(0,10) == 5:
            newtask_users.append(user.username)
            
    for user in newtask_users:
        assign_task(user)
    
    
def assign_task(user):
    user = User.objects.filter(username = user)[0]
    uid = user.id
    print(user)
    userdesc = ""
    hehe = 0
    if hehe:
        pass
    else:
        CounselorData.objects.filter(user = user).delete()
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
        messages = Messages.objects.filter(user = user)
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
        data = CounselorData(user = user, userdescription = userdesc)
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
         model = "gpt-3.5-turbo", messages = mensajes, max_tokens = 99, temperature = 0
    ) 
    title = response.choices[0].message.content 
    uid = User.objects.get(id=uid)
    print(title)     
    new_task = Task(
        title = title, description=task, bygpt = True, user = uid
    )
    
    new_task.save()  
    #tasks = Task.objects.filter(user = user.username, datecompleted__isnull=True)
    return