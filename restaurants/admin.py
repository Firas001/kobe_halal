from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from unfold.admin import ModelAdmin
from .models import Category, Restaurant

admin.site.unregister(User)
@admin.register(User)
class UserAdmin(BaseUserAdmin, ModelAdmin):
    pass

# تسجيل التصنيفات
@admin.register(Category)
class CategoryAdmin(ModelAdmin):
    list_display = ['name']

@admin.register(Restaurant)
class RestaurantAdmin(ModelAdmin):
    list_display = ['name', 'category', 'is_fully_halal', 'created_at']
    list_filter = ['category', 'is_fully_halal']
    search_fields = ['name', 'description']