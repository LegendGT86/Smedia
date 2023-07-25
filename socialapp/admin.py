from django.contrib import admin
from django.contrib.auth.models import Group, User

# unRegister your models here.
admin.site.unregister(Group)

#extend user model
class UserAdmin(admin.ModelAdmin):
    model = User
    # Just display username field on admin
    fields = ["username"]

    #Unregister innitial user
admin.site.unregister(User)
    #Reregister user
admin.site.register(User, UserAdmin)
                         