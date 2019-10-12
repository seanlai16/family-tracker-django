from django.contrib import admin
from .models import User, Family, GeoFence, History


# Register your models here.
admin.site.register(User)
admin.site.register(Family)
admin.site.register(GeoFence)
admin.site.register(History)
