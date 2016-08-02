from django.contrib import admin

from .models import ShiftScheduleSlot, Time, Position

admin.site.register(ShiftScheduleSlot)
admin.site.register(Time)
admin.site.register(Position)