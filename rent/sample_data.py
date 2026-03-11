"""
Sample data loader for House Lease System.
Run via: python manage.py shell < sample_data.py
"""
from users.models import CustomUser
from properties.models import Property

# Create sample owner
owner, _ = CustomUser.objects.get_or_create(
    username='ram_owner',
    defaults={
        'email': 'ram@example.com',
        'first_name': 'Ram',
        'last_name': 'Sharma',
        'role': 'owner',
        'phone': '9841000001',
        'location': 'Kathmandu',
    }
)
owner.set_password('pass1234')
owner.save()

owner2, _ = CustomUser.objects.get_or_create(
    username='sita_owner',
    defaults={
        'email': 'sita@example.com',
        'first_name': 'Sita',
        'last_name': 'Thapa',
        'role': 'owner',
        'phone': '9841000002',
        'location': 'Lalitpur',
    }
)
owner2.set_password('pass1234')
owner2.save()

# Create sample renter
renter, _ = CustomUser.objects.get_or_create(
    username='hari_renter',
    defaults={
        'email': 'hari@example.com',
        'first_name': 'Hari',
        'last_name': 'Bahadur',
        'role': 'renter',
        'phone': '9841000003',
    }
)
renter.set_password('pass1234')
renter.save()

# Sample properties in Kathmandu Valley
properties_data = [
    {
        'owner': owner,
        'title': '2BHK Apartment in Baneshwor',
        'description': 'A well-maintained 2-bedroom apartment near Baneshwor Chowk. Close to major banks, hospitals, and bus stops. 24-hour water supply, parking available.',
        'category': 'apartment',
        'price': 18000,
        'location': 'Baneshwor, Kathmandu',
        'city': 'Kathmandu',
        'latitude': 27.6915,
        'longitude': 85.3453,
        'bedrooms': 2,
        'bathrooms': 1,
        'area_sqft': 750,
        'furnishing': 'semi',
        'status': 'available',
    },
    {
        'owner': owner,
        'title': 'Studio Room in Thamel',
        'description': 'Compact studio room in the heart of Thamel. Ideal for students and working professionals. WiFi included, near restaurants and shops.',
        'category': 'studio',
        'price': 9500,
        'location': 'Thamel, Kathmandu',
        'city': 'Kathmandu',
        'latitude': 27.7172,
        'longitude': 85.3140,
        'bedrooms': 1,
        'bathrooms': 1,
        'area_sqft': 350,
        'furnishing': 'furnished',
        'status': 'available',
    },
    {
        'owner': owner2,
        'title': '3BHK House in Lalitpur',
        'description': 'Spacious 3-bedroom house in a quiet residential area of Lalitpur. Large garden, modern kitchen, solar water heater. 10 minutes from Patan Dhoka.',
        'category': 'house',
        'price': 32000,
        'location': 'Sanepa, Lalitpur',
        'city': 'Lalitpur',
        'latitude': 27.6786,
        'longitude': 85.3132,
        'bedrooms': 3,
        'bathrooms': 2,
        'area_sqft': 1400,
        'furnishing': 'unfurnished',
        'status': 'available',
    },
    {
        'owner': owner2,
        'title': 'Flat in Bhaktapur',
        'description': 'Modern flat near Bhaktapur Durbar Square. Easy access to local markets and schools. Rooftop terrace with city views.',
        'category': 'flat',
        'price': 14000,
        'location': 'Suryabinayak, Bhaktapur',
        'city': 'Bhaktapur',
        'latitude': 27.6722,
        'longitude': 85.4298,
        'bedrooms': 2,
        'bathrooms': 1,
        'area_sqft': 650,
        'furnishing': 'semi',
        'status': 'available',
    },
    {
        'owner': owner,
        'title': 'Single Room in Koteshwor',
        'description': 'Affordable single room near Koteshwor Ring Road. Attached bathroom, common kitchen. Suitable for students.',
        'category': 'room',
        'price': 6000,
        'location': 'Koteshwor, Kathmandu',
        'city': 'Kathmandu',
        'latitude': 27.6830,
        'longitude': 85.3600,
        'bedrooms': 1,
        'bathrooms': 1,
        'area_sqft': 200,
        'furnishing': 'unfurnished',
        'status': 'available',
    },
]

for data in properties_data:
    prop, created = Property.objects.get_or_create(
        title=data['title'],
        defaults=data
    )
    if created:
        print(f"Created: {prop.title}")
    else:
        print(f"Already exists: {prop.title}")

print("\nSample data loaded successfully!")
print("Sample accounts:")
print("  Owner 1:  username=ram_owner    password=pass1234")
print("  Owner 2:  username=sita_owner   password=pass1234")
print("  Renter:   username=hari_renter  password=pass1234")
print("  Admin:    username=admin        password=admin123")
