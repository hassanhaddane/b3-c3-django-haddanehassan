from django.urls import path

from . import views


urlpatterns = [
    path('', views.login_page, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('home', views.events_list, name='home'),
    path('reservations', views.reservations_list, name='reservations'),
    path('add_reserv/', views.add_reserv, name='add_reserv'),
    path('cancel_reserv/', views.cancel_reserv, name='cancel_reserv'),
]