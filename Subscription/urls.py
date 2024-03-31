from django.urls import path, re_path

from Subscription import views

urlpatterns = [
    path('firerisk/factor', views.fireRiskFactor),
    path('firerisk/tff', views.fireRisk),
    path('location', views.location),
    path('decreaseCount', views.decreaseSubscriberCount),
    path('increaseCount', views.increaseSubscriberCount),
]