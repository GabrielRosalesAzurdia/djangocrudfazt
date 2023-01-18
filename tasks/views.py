from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import CreateTaskForm
from . models import Task
from django.utils import timezone
from django.contrib.auth.decorators import login_required

def home(request):
    return render(request,"home.html")

def signup(request):
    if request.method == 'GET':
        return render(request,"auth/signup.html",{'form':UserCreationForm,'error':''})
    if request.method == 'POST':
        if request.POST["password1"] == request.POST["password2"]:
            try:
                user = User.objects.create_user(username=request.POST["username"],password=request.POST["password1"])
                user.save()
                # Sirve para crear la cookie de seción
                login(request,user)
                return redirect("tasks")
            except IntegrityError:
                return render(request,"auth/signup.html",{'form':UserCreationForm, 'error':'User already exists'})
        else:
            return render(request,"auth/signup.html",{'form':UserCreationForm, 'error':'Passwords are not the same'})
    return HttpResponse("Sorry lad no such method is handled ; )")

@login_required
def signout(request):
    logout(request)
    return redirect('home')

def signin(request):
    if request.method == "GET":
        return render(request, "auth/signin.html",{"form":AuthenticationForm})
    if request.method == "POST":
        user = authenticate(request, username=request.POST["username"], password=request.POST["password"])
        if user is None:
            return render(request, "auth/signin.html",{"form":AuthenticationForm, "error":"Username or password are invalid"})
        login(request, user)
        return redirect("tasks")
    return HttpResponse("Sorry lad no such method is handled ; )")

@login_required
def tasks(request):
    tasks = Task.objects.filter(user=request.user,datecompleted__isnull=True)
    return render(request,"tasks/tasks.html",{"tasks":tasks})

@login_required
def tasks_completed(request):
    tasks = Task.objects.filter(user=request.user,datecompleted__isnull=False)
    return render(request,"tasks/tasks.html",{"tasks":tasks})

@login_required
def create_task(request):
    if request.method == "GET":
        return render(request,"tasks/create_task.html",{"form":CreateTaskForm})
    if request.method == "POST":
        try:
            form = CreateTaskForm(request.POST)
            # Gets the raw data from the form 
            new_task = form.save(commit=False)
            new_task.user = request.user
            new_task.save()
            return redirect("tasks")
        except ValueError:
            return render(request,"tasks/create_task.html",{"form":CreateTaskForm,"error":"Please provide a valid data"})
    return HttpResponse("Sorry lad no such method is handled ; )")

@login_required
def task_detail(request,task_id):
    if request.method == "GET":
        # se usa el usuario para que no alteren o vean las de otros usuarios
        task = get_object_or_404(Task, pk=task_id,user=request.user)
        form = CreateTaskForm(instance=task)
        return render(request, "tasks/task_detail.html",{"task":task,"form":form})
    if request.method == "POST":
        try:
            # Este actualiza con los nuevos datos
            task = get_object_or_404(Task,pk=task_id,user=request.user)
            form = CreateTaskForm(request.POST, instance=task)
            form.save()
            return redirect("tasks")
        except ValueError:
            return render(request, "tasks/task_detail.html",{"task":task,"form":form,"error":"Error updating task"}) 
    return HttpResponse("Sorry lad no such method is handled ; )")

@login_required
def task_complete(request,task_id):
    if request.method == "POST":
        print("entro")
        task = get_object_or_404(Task, pk=task_id, user=request.user)
        task.datecompleted = timezone.now()
        task.save()
        return redirect("tasks")
    return HttpResponse("Sorry lad no such method is handled ; )")

@login_required
def task_delete(request,task_id):
    if request.method == "POST":
        task = get_object_or_404(Task, pk=task_id, user=request.user)
        task.delete()
        return redirect("tasks")
    return HttpResponse("Sorry lad no such method is handled ; )")