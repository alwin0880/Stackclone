from django.contrib import admin

# Register your models here.
from api.models import MyUser

admin.site.register(MyUser)