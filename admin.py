from django.contrib import admin

from .models import Slot, Position, Party, Time

admin.site.register(Slot)
admin.site.register(Position)
admin.site.register(Party)
admin.site.register(Time)