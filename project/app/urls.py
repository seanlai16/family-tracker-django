from django.urls import path
from . import views

urlpatterns = [
    path('registerFamily', views.register_family),
    path('login', views.login),
    path('addUpdateUser', views.update_user),
    path('getUserList', views.get_user_list),
    path('getGeofenceList', views.get_geofence_list),
    path('getHistoryList', views.get_history_list),
    path('getLastKnownList', views.get_last_known_list),
    path('addUpdateGeofence', views.update_geofence),
    path('uploadLocation', views.upload_location),
    path('uploadGeofence', views.upload_geofence)
]