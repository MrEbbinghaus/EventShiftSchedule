from hypothesis.extra.django import models, TestCase as hyp_TestCase
from django.test import TestCase, Client

from PartyShiftSchedule import views
from InphimaHelperCoordinator import settings
from hypothesis import given, assume
from hypothesis.strategies import lists, randoms, integers, booleans, text
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse


class PadListTest(hyp_TestCase):

    @given(l=lists(randoms()), pad=randoms(), c=integers(min_value=-1000, max_value=1000))
    def test_pad_list(self, l, pad, c):
        padded_list = views.pad_list(l, pad, c)
        assert isinstance(padded_list, list)
        assert padded_list[:len(l)] == l


class NoEventTest(hyp_TestCase):
    from datetime import date
    from .models import Event

    def setUp(self):
        self.user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        self.client = Client()
        self.client.force_login(self.user, backend=settings.AUTHENTICATION_BACKENDS[0])

    def tearDown(self):
        self.user.delete()

    @given(checked=booleans(),
           time=integers(min_value=0, max_value=2**31-1),
           position=integers(min_value=0, max_value=2**31-1))
    def post_enter(self, status_code, checked, time, position):
        response = self.client.post(reverse('PartyShiftSchedule:enter'), {
            "checked": checked,
            "time": time,
            "position": position}
                          )
        assert response.status_code != status_code

    def test_enter_no_500(self):
        self.post_enter(status_code=500)

    def test_shift_schedule_no_500(self):
        response = self.client.get(reverse('PartyShiftSchedule:shift_schedule'))
        assert response.status_code != 500

