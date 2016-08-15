from django.contrib import admin

from .models import Slot, Position, Party

admin.site.register(Slot)
admin.site.register(Position)
admin.site.register(Party)