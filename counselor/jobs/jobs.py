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
    user = User.objects.filter(username = user)["User"]
    print(user)
    return