from django.contrib import admin

from .models import Slot, Position, Event, Time, OneTimePosition, otpSlot

admin.site.register(Slot)
admin.site.register(Position)
admin.site.register(Event)
admin.site.register(Time)
admin.site.register(OneTimePosition)
admin.site.register(otpSlot)