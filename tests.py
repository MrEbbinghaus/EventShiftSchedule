from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import Client
from hypothesis import given
from hypothesis.extra.django import TestCase as hyp_TestCase
from hypothesis.extra.django.models import models as hyp_models
from hypothesis.extra.datetime import dates
from hypothesis.strategies import lists, randoms, integers, booleans, text, just

from datetime import date

from EventShiftSchedule import views
from EventShiftSchedule.models import *
from InphimaHelperCoordinator import settings # FIXME: This doesn't work with a capsuled app!


class PadListTest(hyp_TestCase):

    @given(l=lists(randoms()), pad=randoms(), c=integers(min_value=-1000, max_value=1000))
    def test_pad_list(self, l, pad, c):
        padded_list = views.pad_list(l, pad, c)
        assert isinstance(padded_list, list)
        assert padded_list[:len(l)] == l


class NoEventTest(hyp_TestCase):

    @given(checked=booleans(),
           time=integers(min_value=0, max_value=2**31-1),
           position=integers(min_value=0, max_value=2**31-1))
    def post_enter(self, status_code, checked, time, position):
        self.user = hyp_models(User, last_login=just("2099-12-31"), date_joined=just("2099-12-31")).example()
        self.client = Client()
        self.client.force_login(self.user, backend=settings.AUTHENTICATION_BACKENDS[0])
        response = self.client.post(reverse('EventShiftSchedule:enter'), {
            "checked": checked,
            "time": time,
            "position": position
        })
        assert response.status_code != status_code
        self.user.delete()

    def test_enter_no_500(self):
        self.post_enter(status_code=500)

    def test_shift_schedule_no_500(self):
        response = self.client.get(reverse('EventShiftSchedule:shift_schedule'))
        assert response.status_code != 500


class AddCommentTest(hyp_TestCase):
    from EventShiftSchedule.views import add_comment

    def setUp(self):
        self.client = Client()

    @given(comment=text(), event_id=integers(min_value=0, max_value=2**31-1))
    def test_add_comment_500(self, comment, event_id):
        self.user = hyp_models(User, last_login=dates(), date_joined=dates(), email=just('')).example()
        self.event = hyp_models(Event, date=dates()).example()
        self.client.force_login(self.user, backend=settings.AUTHENTICATION_BACKENDS[0])

        response = self.client.post(reverse('EventShiftSchedule:comment'), {
            'value': comment,
            'event_id': event_id
        })

        assert response.status_code != 500

        self.user.delete()
