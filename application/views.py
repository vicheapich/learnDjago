from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import Room, Topic
from .forms import RoomForm


# Create your views here.

# rooms = [
#     {"id":1, "name":"DJango"},
#     {"id":2, "name":"FastAPI"},
#     {"id":3, "name":"Frappe"}
# ]

def loginPage(request):

    if request.user.is_authenticated:
        return redirect('homepage')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "User do not exit")
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('homepage')
        else:
            messages.error(request, "username or password incorect")
    context = {}
    return render(request, 'base/login_register.html', context)

def logoutPage(request):
    logout(request)
    return redirect('homepage')

def homepage(request):
    qp = request.GET.get('qp') if request.GET.get('qp') != None else ''

    rooms = Room.objects.filter( 
        Q(topic__name__contains=qp) | 
        Q(name__icontains=qp) | 
        Q(description__icontains=qp)
    )

    topics = Topic.objects.all()
    room_count = rooms.count()
    context = {'rooms':rooms, 'topics':topics , 'room_count':room_count}
    return render(request, 'base/home.html', context)

def room(request, pk):
    rooms = Room.objects.get(id=pk)
    context = {'room':rooms}
    return render(request, 'base/room.html', context)

@login_required(login_url='login-page')
def createroom(request):
    form = RoomForm()
    if request.method == "POST":
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('homepage')
    context = {'form':form}
    return render(request, 'base/room_form.html', context)

@login_required(login_url='login-page')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    if request.user != room.host:
        return HttpResponse('You are not allow here!!')

    if request.method == "POST":
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('homepage')
    context = {'form':form}
    return render(request, 'base/room_form.html', context)

@login_required(login_url='login-page')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)
    if request.user != room.host:
        return HttpResponse('You are not allow here!!')
    if request.method == "POST":
        room.delete()
        return redirect('homepage')
    return render(request, 'base/delete.html', {'obj':room})