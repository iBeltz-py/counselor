"""counselor URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from tasks import views
from wsppwebhook import views 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name = "home"),
    path('signup/',views.signup, name = "signup"),
    path('logout/',views.signout, name = "logout"),
    path('login/',views.signin, name = "login"),
    path('home/',views.home, name = "home2"),
    path("chat/",views.chat, name = "chat"),
    path("contactus/",views.contact_us, name = "contactus"),
    path("search/",views.account_search_view, name = "search"),
    path('contacts/',views.contacts, name = "contacts"),
    path('add_contact/<user2>/',views.add_contact, name = "add_contact"),
    path('remove_contact/<user2>/',views.remove_contact, name = "remove_contact"),
    path('tasks/',views.tasks, name = "tasks"),
    path("tasks/newtask/",views.asktask,name = "ask_task"),
    path('tasks/create/',views.create_task, name = "create_tasks"),
    path('tasks/<int:task_id>/',views.task_detail, name = "task_detail"),
    path('tasks/<int:task_id>/complete/',views.task_complete, name = "task_complete"),
    path('tasks/<int:task_id>/delete/',views.delete_task, name = "delete_task"),
    path('tasks/completed/',views.completed_tasks, name = "completed_tasks"),
    path("wsppwebhook/",views.webhook, name = "wsppwebhook")
    
]
