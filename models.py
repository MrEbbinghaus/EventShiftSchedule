from django.db import models
from django.contrib.auth.models import User

class LdapUser(models.Model):
    """User profile.  Contains some basic configurable settings"""
    user = models.OneToOneField(User, unique=True)
    firstname = models.CharField(max_length=64, blank=True, default='')
    lastname = models.CharField(max_length=64, blank=True, default='')

    def __str__(self):
        fullname = "%s %s"
        return fullname % self.firstname, self.lastname

class ShiftScheduleSlot(models.Model):
    time = models.TimeField(unique=False)
    position = models.TextField(unique=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        information = "%s: %s, %s Uhr"
        return information % (str(self.user), self.position, str(self.time))