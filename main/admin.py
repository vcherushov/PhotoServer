from django.contrib import admin
from .models import *


class TrackCarAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}


admin.site.register(TrackCar, TrackCarAdmin)


