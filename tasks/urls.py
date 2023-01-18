from django.contrib import admin
from django.urls import path
from .views import home,signup, tasks, signout, signin,create_task,task_detail, task_complete, task_delete, tasks_completed

urlpatterns = [
    path('', home,name="home"),
    path('signup/',signup,name="signup"),
    path("tasks/",tasks, name="tasks"),
    path("tasks_completed/",tasks_completed, name="tasks_completed"),
    path("signout/",signout,name="signout"),
    path("signin/", signin, name="signin"),
    path("task/create/",create_task,name="create_task"),
    path("task/<int:task_id>",task_detail,name="task_detail"),
    path("task/<int:task_id>/complete",task_complete,name="task_complete"),
    path("task/<int:task_id>/delete",task_delete,name="task_delete"),
]