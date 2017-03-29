from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from ..log_reg.models import User
from .models import Friend

def process(request):
    Friend.objects.process(request.session['user_id'])
    return redirect('/friends')

def feature(request, id):
    context = {
        "users": User.objects.filter(id=id),
    }
    return render(request, 'friends/feature.html', context)

def remove(request, id):
    user = User.objects.get(id=request.session['user_id'])
    friend = Friend.objects.get(id=id)
    friend.relationships.remove(user)
    return redirect ('/friends')
