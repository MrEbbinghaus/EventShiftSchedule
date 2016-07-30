from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext
from django.template import loader
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render_to_response, redirect


def login_landing(request):
    return HttpResponse(request, 'PartyShiftSchedule/login.html', {})


def login_user(request):
    logout(request)
    username = password = ''
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
    user = authenticate(username=username, password=password)

    if user is not None:
        login(request, user)
        return HttpResponseRedirect('/login_landing')

    return HttpResponse("Yeah! Success!")
