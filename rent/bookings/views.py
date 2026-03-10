from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from properties.models import Property
from .models import Booking
from .forms import BookingForm, BookingResponseForm


@login_required
def create_booking(request, property_id):
    prop = get_object_or_404(Property, pk=property_id)

    if not request.user.is_renter():
        messages.error(request, 'Only renters can make bookings.')
        return redirect('property_detail', pk=property_id)

    if prop.owner == request.user:
        messages.error(request, 'You cannot book your own property.')
        return redirect('property_detail', pk=property_id)

    if not prop.is_available():
        messages.error(request, 'This property is not available for booking.')
        return redirect('property_detail', pk=property_id)

    existing = Booking.objects.filter(renter=request.user, property=prop).first()
    if existing:
        messages.warning(request, 'You already have a booking for this property.')
        return redirect('booking_detail', pk=existing.pk)

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.renter = request.user
            booking.property = prop
            booking.save()
            messages.success(request, 'Booking request submitted! The owner will review it soon.')
            return redirect('booking_detail', pk=booking.pk)
    else:
        form = BookingForm()

    return render(request, 'bookings/create.html', {'form': form, 'property': prop})


@login_required
def booking_detail(request, pk):
    booking = get_object_or_404(Booking, pk=pk)

    if booking.renter != request.user and booking.property.owner != request.user and not request.user.is_staff:
        messages.error(request, 'Access denied.')
        return redirect('home')

    response_form = None
    if booking.property.owner == request.user or request.user.is_staff:
        if request.method == 'POST':
            response_form = BookingResponseForm(request.POST, instance=booking)
            if response_form.is_valid():
                response_form.save()
                messages.success(request, 'Booking status updated.')
                return redirect('booking_detail', pk=pk)
        else:
            response_form = BookingResponseForm(instance=booking)

    return render(request, 'bookings/detail.html', {
        'booking': booking,
        'response_form': response_form,
    })


@login_required
def cancel_booking(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    if booking.renter != request.user:
        messages.error(request, 'Access denied.')
        return redirect('home')
    if request.method == 'POST':
        booking.status = 'cancelled'
        booking.save()
        messages.info(request, 'Booking cancelled.')
        return redirect('profile')
    return render(request, 'bookings/cancel.html', {'booking': booking})


@login_required
def my_bookings(request):
    if request.user.is_renter():
        bookings = Booking.objects.filter(renter=request.user).select_related('property', 'property__owner')
    elif request.user.is_owner():
        bookings = Booking.objects.filter(property__owner=request.user).select_related('renter', 'property')
    else:
        bookings = Booking.objects.all().select_related('renter', 'property')
    return render(request, 'bookings/list.html', {'bookings': bookings})
