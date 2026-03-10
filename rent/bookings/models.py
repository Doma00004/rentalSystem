from django.db import models
from django.conf import settings
from properties.models import Property


class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('cancelled', 'Cancelled'),
    ]

    renter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bookings')
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='bookings')
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='pending')
    move_in_date = models.DateField()
    duration_months = models.PositiveIntegerField(default=1, help_text='Lease duration in months')
    message = models.TextField(blank=True, help_text='Message to the owner')
    owner_response = models.TextField(blank=True, help_text='Owner reply')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ['renter', 'property']

    def __str__(self):
        return f"{self.renter.username} → {self.property.title} [{self.status}]"

    def total_rent(self):
        return self.property.price * self.duration_months
