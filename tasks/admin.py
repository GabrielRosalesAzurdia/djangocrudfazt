from django.contrib import admin
from .models import Task

# Hace visible el cambio de created como un read only
class TaskAdmin(admin.ModelAdmin):
    readonly_fields = ("created",)

admin.site.register(Task,TaskAdmin)