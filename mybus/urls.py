"""
URL configuration for mybus_1 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from mybus import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('admins/bus/', include('bus.bus_urls')),
    path('mybus/', views.home, name='mybus'),
    path('login/', views.user_login),
    path('register/', views.user_register),
    path('logout/', views.user_logout),
    path('admins/', views.admin_panel),
    path('find/', views.find, name='find'),
    path('buslist/', views.bus_list, name='bus_list'),
    path('seats/', views.bus_seats, name='seats'),  # URL for the bus seats selection page
    path('book/', views.book, name='book'),
    path('details/', views.booking_details),
    path('cancel/', views.cancel),
    path('pay/', views.payment, name='pay'),

    path('forgotpassword/', views.forgot_password),
    path('forgotpassword/update/<uname>', views.passotp),

    # path('bookings/', views.bookings, name="bookings" ),


    # path('buseslist/', views.list_buses),
    # path('buses/', views.buses),
]
