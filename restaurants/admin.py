from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from unfold.admin import ModelAdmin
from .models import Category, Place, City

admin.site.unregister(User)
@admin.register(User)
class UserAdmin(BaseUserAdmin, ModelAdmin):
    pass

@admin.register(City)
class CityAdmin(ModelAdmin):
    list_display = ['name']

@admin.register(Category)
class CategoryAdmin(ModelAdmin):
    list_display = ['name']

@admin.register(Place)
class PlaceAdmin(ModelAdmin):
    list_display = ['name', 'place_type', 'city', 'category', 'is_halal_certified', 'updated_at']
    list_filter = ['place_type', 'city', 'category', 'is_halal_certified']
    search_fields = ['name', 'description', 'address']
    readonly_fields = ['created_at', 'updated_at']