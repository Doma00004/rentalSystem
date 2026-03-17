from django import forms
from .models import Booking


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['move_in_date', 'duration_months', 'message']
        widgets = {
            'move_in_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'duration_months': forms.NumberInput(attrs={'class': 'form-control', 'min': '1', 'max': '24'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 3,
                                              'placeholder': 'Any message to the owner...'}),
        }


class BookingResponseForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['status', 'owner_response']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-select'}),
            'owner_response': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
