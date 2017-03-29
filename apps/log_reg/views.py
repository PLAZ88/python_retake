from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from .models import User
from ..friends.models import Friend


def index(request):
    return redirect('/main')

def main(request):
    return render(request, 'log_reg/index.html')

def login(request):
    result = User.objects.login(request.POST.copy())
    if 'errors' in result:
        for error in result['errors']:
            messages.add_message(request, messages.ERROR, error)

        return redirect('/')
    request.session['user'] = result['user'].first_name
    request.session['action'] = 'login'
    request.session['user_id'] = result['user'].id
    return redirect('/friends')

def register(request):

    result = User.objects.register(request.POST.copy())
    if 'errors' in result:
        for error in result['errors']:
            messages.add_message(request, messages.ERROR, error)

        return redirect('/')
    request.session['user'] = result['user'].first_name
    request.session['action'] = 'register'
    request.session['user_id'] = result['user'].id

    return redirect('/friends')

def logout(request):
    request.session.clear()
    return redirect('/')

def friends(request):

    id = request.session['user_id']
    x = User.objects.get(id=id)

    context = {
        "my_friends": Friend.objects.filter(relationships=x),
        "users": User.objects.filter().exclude(friends__friend_id=request.session['user_id']),
    }

    return render(request, 'log_reg/dashboard.html', context)


