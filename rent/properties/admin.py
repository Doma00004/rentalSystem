from django.contrib import admin
from .models import Property, PropertyImage


class PropertyImageInline(admin.TabularInline):
    model = PropertyImage
    extra = 2


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ['title', 'owner', 'category', 'price', 'location', 'status', 'created_at']
    list_filter = ['category', 'status', 'furnishing', 'city']
    search_fields = ['title', 'location', 'owner__username']
    inlines = [PropertyImageInline]
    readonly_fields = ['created_at', 'updated_at']
