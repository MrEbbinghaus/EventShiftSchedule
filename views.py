from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext
from django.template import loader
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render_to_response, redirect

from .models import ShiftScheduleSlot


def login_user(request):
    logout(request)
    username = password = ''
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
    user = authenticate(username=username, password=password)

    if user is not None:
        login(request, user=user)
        return render(request, 'PartyShiftSchedule/landingPage.html', {'username': username})

    return HttpResponseRedirect('/login_landing')

@login_required(login_url='/login/')
def foo(request):
    user = request.user
    return render(request, 'PartyShiftSchedule/landingPage.html', {'username': user})

def shift_schedule(request):
    query_results = ShiftScheduleSlot.objects.all()
    context = {'query_results' : query_results}
    return render(request, 'PartyShiftSchedule/shift_schedule.html', context)