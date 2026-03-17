from django import forms
from .models import Property


class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = [
            'title', 'description', 'category', 'price',
            'location', 'city', 'latitude', 'longitude',
            'bedrooms', 'bathrooms', 'area_sqft',
            'furnishing', 'status', 'image'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if name == 'image':
                field.widget.attrs['class'] = 'form-control'
            else:
                field.widget.attrs['class'] = 'form-control'
        self.fields['latitude'].required = False
        self.fields['longitude'].required = False
        self.fields['area_sqft'].required = False


class PropertySearchForm(forms.Form):
    query = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'placeholder': 'Search by location or title...', 'class': 'form-control'
    }))
    category = forms.ChoiceField(required=False, choices=[('', 'All Types')] + Property.CATEGORY_CHOICES,
                                  widget=forms.Select(attrs={'class': 'form-select'}))
    min_price = forms.DecimalField(required=False, widget=forms.NumberInput(attrs={
        'placeholder': 'Min Price (NPR)', 'class': 'form-control'
    }))
    max_price = forms.DecimalField(required=False, widget=forms.NumberInput(attrs={
        'placeholder': 'Max Price (NPR)', 'class': 'form-control'
    }))
    furnishing = forms.ChoiceField(required=False,
                                    choices=[('', 'Any Furnishing')] + Property.FURNISHING_CHOICES,
                                    widget=forms.Select(attrs={'class': 'form-select'}))
    bedrooms = forms.IntegerField(required=False, widget=forms.NumberInput(attrs={
        'placeholder': 'Min Bedrooms', 'class': 'form-control', 'min': '1'
    }))
