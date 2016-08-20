from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext
from django.template import loader
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render_to_response, redirect

from datetime import date
from PartyShiftSchedule.templatetags.schedule_table_tags import toggle_button
import itertools

from .models import Slot, Position, Party, Time


@login_required(login_url='/login/')
def pss_landing(request):
    user = request.user
    return render(request, 'PartyShiftSchedule/landing_page.html', {'username': user})

@login_required(login_url='/login/')
def shift_schedule(request):
    next_party = get_next_party()
    positions = Position.objects.all()
    times = Time.objects.filter(party=next_party)
    rows = [get_schedule_row(time, next_party, request.user) for time in times]

    context = {
        'positions': positions,
        'rows': rows
    }
    return render(request, 'PartyShiftSchedule/shift_schedule.html', context=context)


def get_schedule_row(time, party, user):
    slots = Slot.objects.filter(time=time)
    positions = Position.objects.filter(party=party)
    row = [time]

    for position in positions:
        pos_slots = slots.filter(position=position)
        row += [pos_slot.user for pos_slot in pos_slots]

        # pad to the right with buttons up to position.pref_users
        row = pad_list(row, toggle_button(user), position.pref_users - len(pos_slots))

    return [str(e) for e in row]


@login_required(login_url='/login/')
def shift_schedule_enter(request):
    next_party = get_next_party()
    times = Time.objects.filter(party=next_party)
    positions = Position.objects.filter(party=next_party)

    context = {
        'times': times,
        'positions': positions,
    }
    return render(request, 'PartyShiftSchedule/shift_schedule_enter.html', context=context)


@login_required(login_url='/login/')
def enter(request):
    if request.method == 'POST':
        data = request.POST
        checked = True if data['checked'] == 'true' else False
        next_party = get_next_party()
        time = Time.objects.get(beginning=data['time'], party=next_party)
        position = Position.objects.get(name=data['position'], party=next_party)
        user = request.user

        slot = Slot.objects.filter(time=time, position=position, user=user, party=next_party)

        if not slot.exists() and checked:
            Slot(time=time, position=position, user=user, party=next_party).save()

        elif slot.exists() and not checked:
            slot[0].delete()

        print("Debug: {0} {1} {2}".format(data['checked'], data['time'], data['position']))

        return HttpResponse(status=200)

    return HttpResponse(status=405)  # 405: Method not allowed


def pad_list(l, pad, c):
    for _ in itertools.repeat(None, c):
        l.append(pad)
    return l


def get_next_party():
    # TODO: Get the party from somewhere else. Dropdown menu, if the tool is used for more then one upcoming party?
    next_partys = Party.objects.filter(date__gte=date.today()).order_by('date')
    if len(next_partys) == 0:
        return
    return next_partys[0]