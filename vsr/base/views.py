from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from .models import Room, Topic, Message, Task
from django.contrib.auth import authenticate, login, logout
from .forms import RoomForm, MsgForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
# Create your views here.


def loginForm(request):
    page = 'login'
    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User Does Not Exist!')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or Password does not exist!')
    context = {'page': page}
    return render(request, 'base/login_reg.html', context)

def logoutUser(request):
    logout(request)
    return redirect('home')

def regUser(request):
    page = 'register'
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Error(s) occured during registration!')
    return render(request, 'base/register.html', {'form': form, 'page':page},)

def home(request):
    q = request.GET.get('q') if request.GET.get('q') is not None else ''
    rooms = Room.objects.filter(topic__name__icontains=q)
    tasks = Task.objects.all()
    topics = Topic.objects.all()
    context = {'rooms': rooms, 'topics': topics, 'tasks': tasks}
    return render(request, 'base/home.html', context)

@login_required(login_url='login')
def add_todo(request):
    if request.method == 'POST':
        new_task_title = request.POST.get('task')

        # Save the new task to the Task model
        Task.objects.create(title=new_task_title)

    return redirect('home')

def room(request, pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all().order_by('-created')
    if request.method == 'POST':
        message = Message.objects.create(
            user = request.user,
            room = room,
            body = request.POST.get('body'),
        )
        return redirect('room', pk=room.id)
    context = {'room':room, 'room_messages':room_messages}
    return render(request, 'base/room.html', context)

@login_required(login_url='login')
def createRoom(request):
    form = RoomForm()
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            room = form.save(commit=False)
            room.host = request.user
            room.save()
            return redirect('home')
    context= {'form': form}
    return render(request, 'base/room_form.html', context)


@login_required(login_url='login')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    if request.user != room.host:
        return HttpResponse('Access Denied')

    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form': form}
    return render(request, 'base/room_form.html', context)

@login_required(login_url='login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)
    if request.user != room.host:
        return HttpResponse('Access Denied')
    if request.method == "POST":
        room.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'object':room})

@login_required(login_url='login')
def deleteMsg(request, pk):
    message = Message.objects.get(id=pk)
    if request.user != message.user:
        return HttpResponse('Access Denied')
    if request.method == "POST":
        message.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'object':message})

@login_required(login_url='login')
def updateMsg(request, pk):
    message = Message.objects.get(id=pk)
    form = MsgForm(instance=message)
    if request.user != message.user:
        return HttpResponse('Access Denied')

    if request.method == 'POST':
        form = MsgForm(request.POST, instance=message)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form': form}
    return render(request, 'base/room_form.html', context)

@login_required(login_url='login')
def delete_todo(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.delete()
    return redirect('home')