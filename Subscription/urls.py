from django.urls import path, re_path

from Subscription import views

urlpatterns = [
    re_path('add-location/', views.add_location),
    re_path('get/locations/', views.get_locations),
    re_path('delete/location/', views.delete_location),
]