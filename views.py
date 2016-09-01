from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

from datetime import date
import itertools

from .models import Slot, Position, Event, Time


def pss_landing(request):
    user = request.user
    return render(request, 'PartyShiftSchedule/landing_page.html', {'username': user})


@login_required()
def shift_schedule(request):
    return redirect("event/{}".format(_get_next_event()))


@login_required()
def shift_schedule_event(request, event_id):
    try:
        next_event = Event.objects.get(id=event_id)
    except Event.DoesNotExist:
        raise Http404

    positions = Position.objects.filter(event=next_event)
    times = Time.objects.filter(event=next_event).order_by('beginning')

    context = {
        'positions': positions,
        'times': times,
        'user': request.user,
    }
    return render(request, 'PartyShiftSchedule/shift_schedule.html', context=context)


@login_required()
def enter(request):
    if request.method == 'POST':
        post = request.POST
        checked = post['checked'] == 'true'
        next_event = Event.objects.get(id=_get_next_event())
        time = Time.objects.get(id=post['time'], party=next_event)
        position = Position.objects.get(id=post['position'], party=next_event)
        user = request.user

        slot = Slot.objects.filter(time=time, position=position, user=user)

        if not slot.exists() and checked:
            Slot(time=time, position=position, user=user).save()

        elif slot.exists() and not checked:
            slot[0].delete()

        print("Debug: {0} {1} {2}".format(post['checked'], post['time'], post['position']))

        return HttpResponse(status=200)

    return HttpResponse(status=405)  # 405: Method not allowed


def pad_list(l, pad, c):
    for _ in itertools.repeat(None, c):
        l.append(pad)
    return l


def _get_next_event():
    next_events = Event.objects.filter(date__gte=date.today()).order_by('date')
    if len(next_events) == 0:
        return
    return next_events[0].id
