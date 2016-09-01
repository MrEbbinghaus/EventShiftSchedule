from django.contrib.auth.models import User
from django.db import models
from datetime import timedelta


class Event(models.Model):
    date = models.DateField(blank=False)
    name = models.CharField(blank=True, max_length=64)
    location = models.TextField(blank=True)
    person_in_charge = models.ForeignKey(User, blank=True)

    def __str__(self):
        return "{0} am {1}".format(self.name, self.date) if self.name \
            else str(self.date)


class Position(models.Model):
    name = models.CharField(max_length=32)
    pref_users = models.PositiveIntegerField(default=3)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('name', 'event')

    def __str__(self):
        return "{0}({1})".format(self.name, self.pref_users)


class Time(models.Model):
    beginning = models.DateTimeField()
    duration = models.FloatField(default=2, blank=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    alt_name = models.CharField(blank=True, max_length=32)

    class Meta:
        unique_together = ('beginning', 'duration', 'event')

    def __str__(self):
        display = "{0} - {1}"
        ending = self.beginning + timedelta(hours=self.duration)

        return display.format(self.beginning.time().strftime("%H:%M"), ending.time().strftime("%H:%M"))


class Slot(models.Model):
    time = models.ForeignKey(Time, on_delete=models.CASCADE)
    position = models.ForeignKey(Position, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('time', 'user')

    def __str__(self):
        display = "{0}: {1}, {2} Uhr"
        return display.format(str(self.user), self.position, str(self.time))
