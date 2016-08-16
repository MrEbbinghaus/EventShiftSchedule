from django.test import TestCase
from PartyShiftSchedule.views import pad_list


class PadListTest(TestCase):

    def test_non_empty_list_positive_pad(self):
        self.assertEqual(
            pad_list([None], '/', 3),
            [None, '/', '/', '/']
        )

    def test_empty_list_positive_pad(self):
        self.assertEqual(
            pad_list([], '/', 3),
            ['/', '/', '/']
        )

    def test_empty_list_zero_pad(self):
        self.assertEqual(
            pad_list([], None, 0),
            []
        )

    def test_empty_list_negativ_pad(self):
        self.assertEqual(
            pad_list([], None, -1),
            []
        )

    def test_empty_list_None_pad(self):
        self.assertEqual(
            pad_list([], None, 3),
            [None, None, None]
        )
