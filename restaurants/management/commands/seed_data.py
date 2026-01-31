import random
import requests
from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from faker import Faker
from restaurants.models import Place, Category, City

class Command(BaseCommand):
    help = 'Seed the database with random restaurants and groceries'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding data...')
        fake = Faker('en_US')

        self.stdout.write('Deleting old data...')
        Place.objects.all().delete()
        Category.objects.all().delete()
        City.objects.all().delete()

        cities_names = ['Kobe', 'Osaka', 'Kyoto', 'Tokyo']
        cities = []
        for name in cities_names:
            city = City.objects.create(name=name)
            cities.append(city)
        self.stdout.write(f'Created {len(cities)} cities.')

        categories_names = ['Japanese Ramen', 'Indian Curry', 'Turkish Kebab', 'Asian Fusion', 'Sweets & Cafe']
        categories = []
        for name in categories_names:
            cat = Category.objects.create(name=name)
            categories.append(cat)
        self.stdout.write(f'Created {len(categories)} categories.')

        places_count = 12

        for i in range(places_count):
            place_type = random.choice(['restaurant', 'restaurant', 'restaurant', 'grocery'])
            
            if place_type == 'restaurant':
                name = f"{fake.last_name()} {random.choice(['Kitchen', 'Diner', 'Bistro', 'House', 'Halal Food'])}"
            else:
                name = f"{fake.last_name()} {random.choice(['Mart', 'Grocery', 'Spices', 'Halal Market'])}"
            
            description = fake.paragraph(nb_sentences=5)
            address = fake.address().replace('\n', ', ')
            
            is_halal = random.choice([True, True, False])
            
            place = Place(
                name=name,
                description=description,
                address=address,
                google_map_link='https://maps.google.com',
                place_type=place_type,
                is_halal_certified=is_halal,
                category=random.choice(categories),
                city=random.choice(cities)
            )

            self.stdout.write(f'Downloading image for {name}...')
            try:
                response = requests.get("https://loremflickr.com/640/480/restaurant", timeout=10)
                if response.status_code == 200:
                    place.image.save(f'place_{i}.jpg', ContentFile(response.content), save=False)
            except Exception as e:
                self.stdout.write(self.style.WARNING(f'Could not download image: {e}'))

            place.save()
            self.stdout.write(self.style.SUCCESS(f'Created place: {name}'))

        self.stdout.write(self.style.SUCCESS('Successfully seeded database!'))