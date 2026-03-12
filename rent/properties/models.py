from django.db import models
from django.conf import settings


class Property(models.Model):
    CATEGORY_CHOICES = [
        ('apartment', 'Apartment'),
        ('house', 'House'),
        ('room', 'Room'),
        ('flat', 'Flat'),
        ('studio', 'Studio'),
        ('villa', 'Villa'),
    ]
    FURNISHING_CHOICES = [
        ('furnished', 'Fully Furnished'),
        ('semi', 'Semi Furnished'),
        ('unfurnished', 'Unfurnished'),
    ]
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('booked', 'Booked'),
        ('unavailable', 'Unavailable'),
    ]

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='properties')
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2, help_text='Monthly rent in NPR')
    location = models.CharField(max_length=200)
    city = models.CharField(max_length=100, default='Kathmandu')
    latitude = models.FloatField(null=True, blank=True, help_text='GPS Latitude')
    longitude = models.FloatField(null=True, blank=True, help_text='GPS Longitude')
    bedrooms = models.PositiveIntegerField(default=1)
    bathrooms = models.PositiveIntegerField(default=1)
    area_sqft = models.PositiveIntegerField(null=True, blank=True, help_text='Area in sq.ft')
    furnishing = models.CharField(max_length=15, choices=FURNISHING_CHOICES, default='unfurnished')
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='available')
    image = models.ImageField(upload_to='property_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Properties'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} - {self.location}"

    def is_available(self):
        return self.status == 'available'


class PropertyImage(models.Model):
    """Extra images for a property."""
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='extra_images')
    image = models.ImageField(upload_to='property_images/')
    caption = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"Image for {self.property.title}"
