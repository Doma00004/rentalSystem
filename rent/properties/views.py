import math
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Property
from .forms import PropertyForm, PropertySearchForm


# ─────────────────────────────────────────────
# Haversine + KNN (from proposal Section 4.3.3)
# ─────────────────────────────────────────────

def haversine_distance(lat1, lon1, lat2, lon2):
    """
    Calculate the great-circle distance between two points on Earth (in km).
    Uses the Haversine formula as described in the project proposal.
    """
    R = 6371  # Earth radius in km
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    d_phi = math.radians(lat2 - lat1)
    d_lambda = math.radians(lon2 - lon1)
    a = math.sin(d_phi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(d_lambda / 2) ** 2
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))


def knn_recommend(user_lat, user_lon, k=5, exclude_id=None):
    """
    KNN algorithm: find k nearest available properties to user's location.
    Returns list of (property, distance_km) sorted by distance.
    """
    properties = Property.objects.filter(
        status='available',
        latitude__isnull=False,
        longitude__isnull=False
    )
    if exclude_id:
        properties = properties.exclude(id=exclude_id)

    distances = []
    for prop in properties:
        dist = haversine_distance(user_lat, user_lon, prop.latitude, prop.longitude)
        distances.append((prop, round(dist, 2)))

    distances.sort(key=lambda x: x[1])
    return distances[:k]


# ─────────────────────────────────────────────
# Views
# ─────────────────────────────────────────────

def home(request):
    featured = Property.objects.filter(status='available').order_by('-created_at')[:6]
    total_properties = Property.objects.filter(status='available').count()
    return render(request, 'base/home.html', {
        'featured': featured,
        'total_properties': total_properties,
        'categories': Property.CATEGORY_CHOICES,
    })


def property_list(request):
    form = PropertySearchForm(request.GET or None)
    properties = Property.objects.filter(status='available')

    if form.is_valid():
        q = form.cleaned_data.get('query')
        category = form.cleaned_data.get('category')
        min_price = form.cleaned_data.get('min_price')
        max_price = form.cleaned_data.get('max_price')
        furnishing = form.cleaned_data.get('furnishing')
        bedrooms = form.cleaned_data.get('bedrooms')

        if q:
            properties = properties.filter(
                Q(title__icontains=q) | Q(location__icontains=q) | Q(city__icontains=q)
            )
        if category:
            properties = properties.filter(category=category)
        if min_price:
            properties = properties.filter(price__gte=min_price)
        if max_price:
            properties = properties.filter(price__lte=max_price)
        if furnishing:
            properties = properties.filter(furnishing=furnishing)
        if bedrooms:
            properties = properties.filter(bedrooms__gte=bedrooms)

    return render(request, 'properties/list.html', {
        'properties': properties,
        'form': form,
        'total': properties.count(),
    })


def property_detail(request, pk):
    prop = get_object_or_404(Property, pk=pk)

    # KNN recommendations based on property location
    nearby = []
    if prop.latitude and prop.longitude:
        nearby = knn_recommend(prop.latitude, prop.longitude, k=4, exclude_id=prop.id)

    # Check if user already has a booking
    existing_booking = None
    if request.user.is_authenticated:
        from bookings.models import Booking
        existing_booking = Booking.objects.filter(renter=request.user, property=prop).first()

    return render(request, 'properties/detail.html', {
        'property': prop,
        'nearby': nearby,
        'existing_booking': existing_booking,
    })


@login_required
def property_create(request):
    if not request.user.is_owner() and not request.user.is_staff:
        messages.error(request, 'Only property owners can add listings.')
        return redirect('property_list')

    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES)
        if form.is_valid():
            prop = form.save(commit=False)
            prop.owner = request.user
            prop.save()
            messages.success(request, 'Property listed successfully!')
            return redirect('property_detail', pk=prop.pk)
    else:
        form = PropertyForm()
    return render(request, 'properties/form.html', {'form': form, 'action': 'Add'})


@login_required
def property_edit(request, pk):
    prop = get_object_or_404(Property, pk=pk)
    if prop.owner != request.user and not request.user.is_staff:
        messages.error(request, 'You can only edit your own properties.')
        return redirect('property_detail', pk=pk)

    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES, instance=prop)
        if form.is_valid():
            form.save()
            messages.success(request, 'Property updated successfully!')
            return redirect('property_detail', pk=prop.pk)
    else:
        form = PropertyForm(instance=prop)
    return render(request, 'properties/form.html', {'form': form, 'action': 'Edit', 'property': prop})


@login_required
def property_delete(request, pk):
    prop = get_object_or_404(Property, pk=pk)
    if prop.owner != request.user and not request.user.is_staff:
        messages.error(request, 'You can only delete your own properties.')
        return redirect('property_detail', pk=pk)

    if request.method == 'POST':
        prop.delete()
        messages.success(request, 'Property deleted.')
        return redirect('property_list')
    return render(request, 'properties/confirm_delete.html', {'property': prop})


@login_required
def my_properties(request):
    if not request.user.is_owner() and not request.user.is_staff:
        messages.error(request, 'Only owners can view this page.')
        return redirect('home')
    properties = Property.objects.filter(owner=request.user).order_by('-created_at')
    return render(request, 'properties/my_properties.html', {'properties': properties})


def property_map(request):
    """
    Interactive map view: shows all available properties,
    lets renter set their location, draws a radius boundary, and
    calculates distances using the Haversine formula.
    """
    properties = Property.objects.filter(
        status='available',
        latitude__isnull=False,
        longitude__isnull=False
    ).select_related('owner').order_by('-created_at')
    return render(request, 'properties/map.html', {'properties': properties})
