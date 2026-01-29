from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"

class Restaurant(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='restaurants')
    description = models.TextField()
    address = models.CharField(max_length=300)
    is_fully_halal = models.BooleanField(default=True) 
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name