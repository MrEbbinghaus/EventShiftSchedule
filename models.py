from django.contrib.auth.models import User
from django.db import models
from datetime import timedelta


class Event(models.Model):
    date = models.DateField(blank=False)
    name = models.CharField(blank=True, max_length=64)
    location = models.TextField(blank=True)
    disabled = models.BooleanField(blank=False, default=False)
    person_in_charge = models.ForeignKey(User, blank=True, null=True)

    class Meta:
        get_latest_by = 'date'

    def __str__(self):
        return "{0}{1} am {2}".format("[DISABLED] " if self.disabled else "", self.name, self.date) if self.name \
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
        display = "{0} - {1} am {2}" + (" {0}".format(self.alt_name) if self.alt_name else "")
        ending = self.beginning + timedelta(hours=self.duration)

        return display.format(self.beginning.time().strftime("%H:%M"),
                              ending.time().strftime("%H:%M"),
                              self.beginning.date())


class Slot(models.Model):
    time = models.ForeignKey(Time, on_delete=models.CASCADE)
    position = models.ForeignKey(Position, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('time', 'user')

    def __str__(self):
        display = "{0}: {1}, {2} Uhr"
        return display.format(to_full_name(self.user), self.position, str(self.time))


class Comment(models.Model):
    value = models.TextField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'event')

    def __str__(self):
        display = "{0} about: {1}"
        return display.format(to_full_name(self.user), self.event)


# für Auf- und Abbauschichten
class OneTimePosition(models.Model):
    name = models.CharField(max_length=32)
    time = models.DateTimeField()
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('time', 'event')

    def __str__(self):
        display = '{0}: {1}'
        return display.format(self.time.time().strftime('%a %H:%M'), self.name)


class otpSlot(models.Model):
    otPosition = models.ForeignKey(OneTimePosition, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'otPosition')

    def __str__(self):
        display = '{0}: {1}'
        return display.format(to_full_name(self.user), str(self.otPosition))


def to_full_name(user):
    if (user.first_name is not '') or (user.last_name is not ''):
        return " ".join([user.first_name, user.last_name])
    return user
