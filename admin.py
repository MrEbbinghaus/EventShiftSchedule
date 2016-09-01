from django.contrib import admin

from .models import Slot, Position, Event, Time

admin.site.register(Slot)
admin.site.register(Position)
admin.site.register(Event)
admin.site.register(Time)