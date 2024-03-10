from django.shortcuts import render,redirect
from django.http import HttpResponse 
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from .models import Room,Topic,Message, User
from .form import RoomForm,UserForm,MyUserCreationForm
# Create your views here.
# rooms = [
#     {'id':1,'name':'surya'},
#     {'id':2,'name':'Ajay'},
#     {'id':3,'name':'hari'}
# ]
# couples = [
#     {'id':1, 'name':'Surya Bhuvana'},
#     {'id':2, 'name':'vimal elakkiya'},
#     {'id':3, 'name':'Vairakkannu Muthulaksmi'},
# ]

def loginPage(request):
    page = 'login'
    if request.method == 'POST':
        email = request.POST.get('email').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
        except:
            messages.error(request, 'User does not exist')

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('Home')
        else:
            messages.error(request, 'Email or password does not exist')

    context={'page':page}    
    return render(request, 'base/login_register.html',context)

def logoutUser(request):
    logout(request)
    return redirect('Home')

def registerPage(request):
    form = MyUserCreationForm()

    if request.method == "POST":
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('Home')

    return render(request, 'base/login_register.html',{'form':form})

def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(
        Q(topic__name__icontains = q) |
        Q(name__icontains = q) |
        Q(description__icontains = q) 
                                )
    topics = Topic.objects.all()[0:4]
    rooms_count = rooms.count()
    room_message = Message.objects.filter(Q(room__topic__name__icontains=q))
    context = {'rooms':rooms,'topics':topics,'rooms_count':rooms_count,'room_message':room_message}

    return render(request, 'base/home.html',context)

def room(request,pk):
    room = Room.objects.get(id=pk)
    room_message = room.message_set.all()
    participants = room.participants.all()
    if request.method == 'POST':
        message = Message.objects.create(
            user = request.user,
            room = room,
            body = request.POST.get('body')
        )
        room.participants.add(request.user)
    if request.user == 'POST':
        message.delete()
        room.participants.remove()
        return redirect('room',pk=room.id)

    context = {'room':room,'room_message':room_message,'participants':participants}

    return render(request, 'base/room.html',context)

def UserProfile(request,pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    room_message = user.message_set.all()
    topics = Topic.objects.all()
    context = {'user':user,'rooms':rooms,'room_message':room_message,'topics':topics}
    return render(request, 'base/profile.html',context)

@login_required(login_url='/login')
def Room_create(request):
    form = RoomForm()
    topics = Topic.objects.all()
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic,created = Topic.objects.get_or_create(name=topic_name)
        Room.objects.create(
            user=request.user,
            topic = topic,
            name = request.POST.get('name'),
            description= request.POST.get('description')
        )
        return redirect('Home')
        
    context = {'form':form,'topics':topics}

    return render(request, 'base/room_form.html',context)

@login_required(login_url='/login')
def Update_room(request,pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    topics = Topic.objects.all()

    if request.user != room.user:
        return HttpResponse('Your not allowed here')
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic,created = Topic.objects.get_or_create(name=topic_name)
        room.name = request.POST.get('name')
        room.topic = request.POST.get('topic')
        room.description= request.POST.get('description')
        room.save()
        return redirect('Home')
    context = {'form':form,'topics':topics,'room':room}
    return render(request, 'base/room_form.html',context)

@login_required(login_url='/login')
def DeleteRoom(request,pk):
    room = Room.objects.get(id=pk)
    if request.method == "POST":
        room.delete()
        return redirect('Home')
    return render(request, 'base/delete.html', {'obj':room})
        
@login_required(login_url='/login')
def Deletemessage(request,pk):
    message = Message.objects.get(id=pk)
    if request.user != message.user:
        return HttpResponse("You are not allowed Here!")
    
    if request.method == "POST":
        message.delete()
        
        
        return redirect('Home')
    return render(request, 'base/delete.html', {'obj':message})

@login_required(login_url='login')
def UpdateUser(request):
    user = request.user
    form = UserForm(instance=user)
    if request.method == 'POST':
        form = UserForm(request.POST,request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile',pk=user.id)
    context  = {'form':form}
    return render(request,'base/Update_user.html',context)

def TopicPage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    topics = Topic.objects.filter(name__icontains=q)
    

    return render(request, 'base/topics.html',{'topics':topics})

def ActivityPage(request):
    room_message = Message.objects.all()
    return render(request, 'base/activity.html',{'room_message':room_message})