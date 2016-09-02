from hypothesis.extra.django import models, TestCase as hyp_TestCase
from django.test import TestCase
from PartyShiftSchedule.views import pad_list
from hypothesis import given
from hypothesis.strategies import lists, randoms, integers


class PadListTest(hyp_TestCase):

    @given(l=lists(randoms()), pad=randoms(), c=integers(min_value=-10000, max_value=10000))
    def test_pad_list(self, l, pad, c):
        padded_list = pad_list(l, pad, c)
        assert isinstance(padded_list, list)
        assert padded_list[:len(l)] == l