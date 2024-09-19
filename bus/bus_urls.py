from django.urls import path
from django.conf import settings


from bus import views
urlpatterns = [
    path('add/', views.add_bus),
    path('view/', views.view_buses),
    path('see_bookings/', views.see_bookings),
    path('delete/<busid>', views.delete_bus),
    path('update/<busid>', views.update_bus), 
]


