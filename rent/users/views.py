from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegisterForm, LoginForm, ProfileUpdateForm
from bookings.models import Booking
from properties.models import Property


def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Welcome, {user.first_name or user.username}! Your account has been created.')
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'users/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Welcome back, {user.first_name or user.username}!')
            return redirect(request.GET.get('next', 'home'))
    else:
        form = LoginForm()
    return render(request, 'users/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('home')


@login_required
def profile_view(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
    else:
        form = ProfileUpdateForm(instance=request.user)

    bookings = []
    properties = []
    if request.user.is_renter():
        bookings = Booking.objects.filter(renter=request.user).select_related('property').order_by('-created_at')
    elif request.user.is_owner():
        properties = Property.objects.filter(owner=request.user).order_by('-created_at')

    return render(request, 'users/profile.html', {
        'form': form,
        'bookings': bookings,
        'properties': properties,
    })


@login_required
def dashboard_view(request):
    if not request.user.is_staff:
        messages.error(request, 'Access denied.')
        return redirect('home')
    from users.models import CustomUser
    users = CustomUser.objects.all().order_by('-created_at')
    properties = Property.objects.all().order_by('-created_at')
    bookings = Booking.objects.all().select_related('renter', 'property').order_by('-created_at')
    return render(request, 'users/admin_dashboard.html', {
        'users': users,
        'properties': properties,
        'bookings': bookings,
        'total_users': users.count(),
        'total_properties': properties.count(),
        'total_bookings': bookings.count(),
        'pending_bookings': bookings.filter(status='pending').count(),
    })
