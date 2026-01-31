from django.core.management.base import BaseCommand
from restaurants.models import Place, Category, City

class Command(BaseCommand):
    help = 'Clears all data from the database'

    def handle(self, *args, **kwargs):
        self.stdout.write('Clearing database...')

        deleted_places = Place.objects.all().delete()[0]
        deleted_cats = Category.objects.all().delete()[0]
        deleted_cities = City.objects.all().delete()[0]

        self.stdout.write(self.style.SUCCESS(f'Successfully deleted: {deleted_places} places, {deleted_cats} categories, {deleted_cities} cities.'))