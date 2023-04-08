from django.shortcuts import get_object_or_404, redirect, render

from . import forms
from django.contrib.auth.models import User
from .models import Event
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Reservation


def login_page(request):
    form = forms.LoginForm()
    message = ''
    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                message = 'Identifiants invalides.'
    return render(
        request, 'authentication/login.html', context={'form': form, 'message': message})

@login_required
def events_list(request):
    events = Event.objects.all()
    reservations = Reservation.objects.all()
    events_to_show = []
    for event in events:
        if event.available_seats > 0:
            is_already_reserved = False
            for reservation in reservations:
                if reservation.user.id == request.user.id and reservation.event.id == event.id:
                    is_already_reserved = True
            if is_already_reserved == False:
                events_to_show.append(event)
    return render(request, 'home.html', {'events' : events_to_show})

@login_required
def reservations_list(request):
    reservations = Reservation.objects.all()
    sorted_reservations = []
    for reservation in reservations:
        if reservation.user.id == request.user.id:
            sorted_reservations.append(reservation)
    return render(request, 'reservations.html', {'reservations' : sorted_reservations})

@login_required
def add_reserv(request):
    if request.method == 'POST':
        user_id = get_object_or_404(User, pk=request.user.id)
        event_id = get_object_or_404(Event, pk=request.POST.get('event_id'))
        if user_id and event_id:
            reservation = Reservation(user=user_id, event=event_id)
            reservation.save()
            event_id.available_seats = event_id.available_seats -1
            event_id.save()
    return redirect('home')

@login_required
def cancel_reserv(request):
    if request.method == 'POST':
        reservation_id = get_object_or_404(Reservation, pk=request.POST.get('reservation_id'))
        if reservation_id:
            event = reservation_id.event
            event.available_seats = event.available_seats +1
            event.save()
            reservation_id.delete()
    return redirect('reservations')
    
def logout_user(request):
    logout(request)
    return redirect('login')
