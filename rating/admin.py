from django.contrib import admin
from .models import user_profile, app, tasks
from django.contrib.admin.options import ModelAdmin

class taskadmin(ModelAdmin):
    model=tasks
    list_display = ['id','user','app','status']

class appadmin(ModelAdmin):
    model=tasks
    list_display = ['id','app_name']

class userprofileadmin(ModelAdmin):
    model=tasks
    list_display = ['id','user']


admin.site.register(user_profile,userprofileadmin)
admin.site.register(app,appadmin)
admin.site.register(tasks,taskadmin)