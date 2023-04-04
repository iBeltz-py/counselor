from django.contrib import admin
from .models import Task
from .models import Messages
from .models import CounselorData
from .models import FriendList, FriendRequest
from .models import ContactUs
# Register your models here.


class TaskAdmin(admin.ModelAdmin):
    readonly_fields = ("created", )
    
class ContactUsAdmin(admin.ModelAdmin):
    readonly_fields = ("created","user", )
    
class MessagesAdmin(admin.ModelAdmin):
    readonly_fields = ("created", )
class CounselorDataAdmin(admin.ModelAdmin):
    readonly_fields = ("created", )

class FriendListAdmin(admin.ModelAdmin):
       list_filter = ["user"]
       list_display=["user"]
       search_fields= ["user"]
       readonly_fields = ["user"]
       
       class Meta:
           model = FriendList

class FriendRequestAdmin(admin.ModelAdmin):
    list_filter = ["sender", "receiver"]
    list_display = ["sender", "receiver"]
    search_fields = ["sender__username", "receiver__email","receiver__email", "receiver__username"]
    class Meta:
        model = FriendRequest



admin.site.register(Task,TaskAdmin)
admin.site.register(Messages,MessagesAdmin)
admin.site.register(CounselorData,CounselorDataAdmin)
admin.site.register(FriendList,FriendListAdmin)
admin.site.register(FriendRequest,FriendRequestAdmin)
admin.site.register(ContactUs,ContactUsAdmin)




