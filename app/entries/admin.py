from django.contrib import admin

from .models import Entry, EntryRow

# Register your models here.

admin.site.register(Entry)
admin.site.register(EntryRow)
