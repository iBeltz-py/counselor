from django.conf import settings
from django.contrib.auth.models import User
import random


def schedule_api():
    users = User.objects.all()
    for user in users:
        if random.randint(0,10) == 5:
            print(user.username)
    