from django.contrib.auth.models import User
from django.db import models


class LdapUser(models.Model):
    """User profile.  Contains some basic configurable settings"""
    user = models.OneToOneField(User, unique=True)
    firstname = models.CharField(max_length=64, blank=True, default='')
    lastname = models.CharField(max_length=64, blank=True, default='')

    def __str__(self):
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
        return display.format(str(self.user), self.position, str(self.time))
