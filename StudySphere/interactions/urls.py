from django.urls import path
from . import views

urlpatterns = [
    path('notifications/', views.notifications, name='notifications'),
    path('notifications/mark-read/', views.mark_all_read, name='mark_all_read'),
    path('user/<int:user_id>/follow/', views.toggle_follow, name='toggle_follow'),
]
