from django.urls import path
from . import views

urlpatterns = [
    path('registerFamily', views.register_family),
    path('login', views.login),
    path('updateUser', views.update_user),
    path('getUserList', views.get_user_list),
    path('getGeofenceList', views.get_geofence_list),
    path('getHistoryList', views.get_history_list),
    path('updateGeofence', views.update_geofence),
    path('uploadLocation', views.upload_location),
    path('uploadGeofence', views.upload_geofence)
]