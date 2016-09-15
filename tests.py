from hypothesis.extra.django import models, TestCase as hyp_TestCase
from django.test import TestCase, Client

from .views import _get_next_event
from PartyShiftSchedule import views
from InphimaHelperCoordinator import settings
from hypothesis import given, assume
from hypothesis.strategies import lists, randoms, integers, booleans, text
from django.contrib.auth.backends import ModelBackend
from django.core.urlresolvers import reverse


class PadListTest(hyp_TestCase):

    @given(l=lists(randoms()), pad=randoms(), c=integers(min_value=-1000, max_value=1000))
    def test_pad_list(self, l, pad, c):
        padded_list = views.pad_list(l, pad, c)
        assert isinstance(padded_list, list)
        assert padded_list[:len(l)] == l


class EnterSignupTest(hyp_TestCase):
    from datetime import date
    from .models import Event
    from django.contrib.auth.models import User

    def setUp(self):
        self.client = Client()

        self.user = self.User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        # self.event = self.Event.objects.create(date="2099-12-31", person_in_charge=self.user)

    @given(checked=booleans(), time=integers(min_value=0, max_value=2**31-1), position=integers(min_value=0, max_value=2**31-1))
    def post_enter(self, status_code, checked, time, position):
        user = self.User.objects.get(username='john')
        c = Client()
        c.force_login(user, backend=settings.AUTHENTICATION_BACKENDS[0])
        response = c.post(reverse('PartyShiftSchedule:enter'), {
            "checked": checked,
            "time": time,
            "position": position}
                          )
        assert response.status_code != status_code

    def test_enter_no_500(self):
        self.post_enter(status_code=500)
