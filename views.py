from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext
from django.template import loader
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render_to_response, redirect
from itertools import combinations, chain, product

from .models import ShiftScheduleSlot, Time, Position


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
    positions = Position.objects.all()
    times = Time.objects.all().order_by('time')
    rows = list()
    table = slots_to_table()

    # TODO make it beautiful
    for time in times:
        row = [time.time]
        for position in positions:
            entrys = list()
            if frozenset({time, position}) in table.keys():
                entrys = [table[frozenset({time, position})]]
                row += entrys


            if len(entrys) < position.pref_users:
                for i in range(0,  position.pref_users - len(entrys)):
                    row.append("")


        rows.append(row)

    context = {
        'query_results': query_results,
        'positions': positions,
        'rows': rows
    }
    return render(request, 'PartyShiftSchedule/shift_schedule.html', context)


def slots_to_table():
    table = dict()
    times = Time.objects.all()
    positions = Position.objects.all()
    slots = ShiftScheduleSlot.objects.all()
    key_set = map(set, product(times, positions))

    for slot in slots:
        table[frozenset({slot.time, slot.position})] = slot.user

    for e in table:  # debug
        print(e, table[e])

    return table
