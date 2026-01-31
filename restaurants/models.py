from django.db import models

class City(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Cities"

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Categories"

class Place(models.Model):
    PLACE_TYPES = [
        ('restaurant', 'Restaurant'),
        ('grocery', 'Grocery Store'),
    ]

    name = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='places_images/', blank=True, null=True)

    google_map_link = models.URLField(max_length=500)
    address = models.CharField(max_length=300)
    
    place_type = models.CharField(max_length=20, choices=PLACE_TYPES, default='restaurant')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='places')
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, related_name='places')
    
    is_halal_certified = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name