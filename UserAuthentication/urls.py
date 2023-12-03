from django.urls import path, re_path

from UserAuthentication import views

urlpatterns = [
    re_path('login/', views.login),
    re_path('logout/', views.logout),
    re_path('signup/', views.signup),
    re_path('test_token/', views.test_token),
    re_path('test_token/', views.test_token),
    re_path('add-location/', views.add_location),
    re_path('remove-location/', views.remove_location),
    re_path('add-count/', views.add_count_to_location),
    re_path('remove-count/', views.remove_count_from_location)
]