from django.contrib import admin
from .models import Task
from .models import Messages
from .models import CounselorData
from .models import Friends
# Register your models here.


class TaskAdmin(admin.ModelAdmin):
    readonly_fields = ("created", )
    
class ContactUsAdmin(admin.ModelAdmin):
    readonly_fields = ("created","user", )
    
class MessagesAdmin(admin.ModelAdmin):
    readonly_fields = ("created", )
class CounselorDataAdmin(admin.ModelAdmin):
    readonly_fields = ("created", )

class ContactsAdmin(admin.ModelAdmin):
    readonly_fields = ("created", )

class FriendsAdmin(admin.ModelAdmin):
    readonly_fields=("created", )

admin.site.register(Task,TaskAdmin)
admin.site.register(Messages,MessagesAdmin)
admin.site.register(CounselorData,CounselorDataAdmin)
admin.site.register(Friends,FriendsAdmin)




