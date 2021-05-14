from django.contrib import admin

# Register your models here.
from .models import StorageData, User, Folder, File, ActionLog

# Register your models here.
admin.site.register([User, StorageData, Folder, File, ActionLog])