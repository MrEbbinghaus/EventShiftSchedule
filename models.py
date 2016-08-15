from django.contrib.auth.models import User
from django.db import models

<<<<<<< HEAD
=======
class Party(models.Model):
    date = models.DateField(blank=False)
    name = models.TextField(blank=True)
    location = models.TextField(blank=True)
    person_in_charge = models.ForeignKey(User, blank=True)

    def __str__(self):
        return "{0} am {1}".format(self.name, self.date) if self.name \
            else self.date


class Position(models.Model):
    name = models.CharField(max_length=32)
    pref_users = models.PositiveIntegerField(default=3)
    party = models.ForeignKey(Party, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('name', 'party')

    def __str__(self):
        return "{0}({1})".format(self.name, self.pref_users)


class Slot(models.Model):
    time = models.TimeField()
    position = models.ForeignKey(Position, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    party = models.ForeignKey(Party, on_delete=models.CASCADE)
>>>>>>> master

    class Meta:
        unique_together = ('time', 'position', 'user', 'party')

    def __str__(self):
<<<<<<< HEAD
        fullname = "{} {}"
        return fullname.format(self.firstname, self.lastname)


class Time(models.Model):
    time = models.TimeField(unique=True)

    def __str__(self):
        return str(self.time)


class Position(models.Model):
    name = models.CharField(max_length=32, blank=False, unique=True)
    pref_users = models.IntegerField(default=3)

    def __str__(self):
        return "{}({})".format(self.name, self.pref_users)


class ShiftScheduleSlot(models.Model):
    time = models.ForeignKey(Time, unique=False)
    position = models.ForeignKey(Position, unique=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        display = "{}: {}, {} Uhr"
=======
        display = "{0}: {1}, {2} Uhr"
>>>>>>> master
        return display.format(str(self.user), self.position, str(self.time))
