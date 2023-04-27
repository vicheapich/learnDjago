from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .models import Room, Topic, Message
from .forms import RoomForm, UserForm


# Create your views here.

# rooms = [
#     {"id":1, "name":"DJango"},
#     {"id":2, "name":"FastAPI"},
#     {"id":3, "name":"Frappe"}
# ]

def loginPage(request):
    page = 'login-page'
    if request.user.is_authenticated:
        return redirect('homepage')

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        # try:
        #     user = User.objects.get(username=username)
        # except:
        #     messages.error(request, "User do not exit")
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('homepage')
        else:
            messages.error(request, "username or password incorect")
    context = {'page':page}
    return render(request, 'base/login_register.html', context)


def logoutPage(request):
    logout(request)
    return redirect('homepage')


def registerPage(request):
    form = UserCreationForm
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('homepage')
        else:
            messages.error(request, "An error occured during resgitration")

    return render(request, 'base/login_register.html',{'form':form})


def homepage(request):
    qp = request.GET.get('qp') if request.GET.get('qp') != None else ''

    rooms = Room.objects.filter( 
        Q(topic__name__contains=qp) | 
        Q(name__icontains=qp) | 
        Q(description__icontains=qp)
    )

    topics = Topic.objects.all()[0:4]
    room_count = rooms.count()
    room_message = Message.objects.filter(Q(room__topic__name__icontains=qp))

    context = {'rooms':rooms, 'topics':topics , 'room_count':room_count, 'room_message':room_message}
    return render(request, 'base/home.html', context)


def room(request, pk):
    rooms = Room.objects.get(id=pk)
    room_messages = rooms.message_set.all()
    participants = rooms.participants.all()
    if request.method == 'POST':
        message = Message.objects.create(
            user = request.user,
            room = rooms,
            body = request.POST.get('body')
        )
        rooms.participants.add(request.user)
        return redirect('room', pk = rooms.id)
    context = {'room':rooms, 'room_messages': room_messages , 'participants': participants}
    return render(request, 'base/room.html', context)

def userProfile(request, pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    room_message = user.message_set.all()
    topics = Topic.objects.all()
    context = {'user': user, 'rooms':rooms , 'room_message':room_message, 'topics':topics}
    return render(request, 'base/profile.html', context)



@login_required(login_url='login-page')
def createroom(request):
    form = RoomForm()
    topics = Topic.objects.all()
    if request.method == "POST":
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name = topic_name)
        Room.objects.create(
            host = request.user,
            topic = topic,
            name = request.POST.get('name'),
            description = request.POST.get('description')
        )
        return redirect('homepage')
    context = {'form':form, 'topics':topics}
    return render(request, 'base/room_form.html', context)


@login_required(login_url='login-page')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    topics = Topic.objects.all()
    if request.user != room.host:
        return HttpResponse('You are not allow here!!')

    if request.method == "POST":
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name = topic_name)
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()
        return redirect('homepage')
    context = {'form':form, 'topics':topics, 'room':room}
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


@login_required(login_url='login-page')
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)
    if request.user != message.user:
        return HttpResponse('You are not allow here!!')
    if request.method == "POST":
        message.delete()
        return redirect('homepage')
    return render(request, 'base/delete.html', {'obj':message})


@login_required(login_url='login')
def updateUser(request):
    user = request.user
    form = UserForm(instance=user)
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile-page', pk=user.id)

    return render(request, 'base/update-user.html', {'form': form})

def topicsPage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    topics = Topic.objects.filter(name__icontains=q)
    return render(request, 'base/topics.html', {'topics': topics})

def activityPage(request):
    room_messages = Message.objects.all()
    return render(request, 'base/activity.html', {'room_messages': room_messages})


@login_required(login_url='login')
def deleteTopic(request, pk):
    topic = Topic.objects.get(id = pk)
    if request.user != topic.host:
        return HttpResponse('You are not allow here!!')
    if request.method == "POST":
        topic.delete()
        return redirect('homepage')
    return render(request, 'base/delete.html', {'obj':topic})