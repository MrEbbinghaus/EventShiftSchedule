from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_list_or_404, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from datetime import date

from .models import Slot, Position, Event, Time, OneTimePosition, otpSlot, Comment


def ess_landing(request):
    events = Event.objects.filter(disabled=False)
    return render(request, 'EventShiftSchedule/landing_page.html', {'events': events})


@login_required()
def shift_schedule_event(request, event_id):
    try:
        next_event = get_object_or_404(Event, id=event_id)
        positions = Position.objects.filter(event=next_event)
        times = Time.objects.filter(event=next_event).order_by('beginning')
        oneTimePositions = OneTimePosition.objects.filter(event=next_event).order_by('time')

    except ObjectDoesNotExist:
        return HttpResponse(status=400)
    try:
        comment = Comment.objects.get(user=request.user, event=next_event)
    except Comment.DoesNotExist:
        comment = None

    context = {
        'oneTimePositions': oneTimePositions,
        'positions': positions,
        'times': times,
        'user': request.user,

        # guessed value for when a table should be flipped
        'transpose': len(times) / len(positions) < 0.5 if len(positions) > 0 else False,

        'event': next_event,
        'preset_comment': comment.value if comment else "",
    }
    return render(request, 'EventShiftSchedule/shift_schedule.html', context=context)


@login_required()
def enter(request):
    if request.method == 'POST':
        post = request.POST
        checked = post['checked'] == 'true'
        try:
            position = Position.objects.get(id=post['position'])
            event = position.event
            time = Time.objects.get(id=post['time'], event=event)

            user = request.user

            slot = Slot.objects.filter(time=time, position=position, user=user)
        except (ObjectDoesNotExist, NoNextEventException):
            return HttpResponse(status=400)

        if not slot.exists() and checked:
            Slot(time=time, position=position, user=user).save()

        elif slot.exists() and not checked:
            slot[0].delete()

        print("Debug: {0} {1} {2}".format(post['checked'], post['time'], post['position']))

        return HttpResponse(status=200)

    return HttpResponse(status=405)  # 405: Method not allowed


@login_required()
def add_comment(request):
    if request.method == 'POST':
        post = request.POST
        try:
            Comment.objects.update_or_create(
                user=request.user,
                event=get_object_or_404(Event, id=post.get('event_id')),
                defaults={'value': post.get('comment-value')})

        except Http404:
            return HttpResponse(status=400)

        # redirect back
        return redirect(reverse("EventShiftSchedule:shift_schedule_event", args=[post.get('event_id')]))
    else:
        return HttpResponse(status=405)  # 405: Method not allowed

@login_required()
def enter_otp(request):
    if request.method == 'POST':
        post = request.POST
        checked = post['checked'] == 'true'
        try:
            one_time_position = OneTimePosition.objects.get(id=post['position'])
            event = one_time_position.event
            user = request.user

            slot = otpSlot.objects.filter(otPosition=one_time_position, user=user)
        except (ObjectDoesNotExist, NoNextEventException):
            return HttpResponse(status=404)

        if not slot.exists() and checked:
            otpSlot(otPosition=one_time_position, user=user).save()

        elif slot.exists() and not checked:
            slot[0].delete()

        print("Debug: {0} {1}".format(post['checked'], post['position']))

        return HttpResponse(status=200)

    return HttpResponse(status=405)  # 405: Method not allowed


def _get_next_event():
    return Event.objects.filter(date__gte=date.today())


class NoNextEventException(Exception):
    def __init__(self, message, errors):
        # Call the base class constructor with the parameters it needs
        super(NoNextEventException, self).__init__(message)

        self.errors = errors
