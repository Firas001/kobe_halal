import os
import shutil
from django.conf import settings
from django.core.management.base import BaseCommand
from restaurants.models import Place, Category, City

class Command(BaseCommand):
    help = 'Clears all data from the database and deletes media files'

    def handle(self, *args, **kwargs):
        self.stdout.write('Starting cleanup process...')

        self.stdout.write('1. Clearing database records...')
        
        places_count = Place.objects.count()
        Place.objects.all().delete()
        Category.objects.all().delete()
        City.objects.all().delete()
        
        self.stdout.write(f'   - Deleted {places_count} places.')

        self.stdout.write('2. Cleaning up media files...')
        images_dir = os.path.join(settings.MEDIA_ROOT, 'places_images')

        if os.path.exists(images_dir):
            try:
                shutil.rmtree(images_dir)
                self.stdout.write(self.style.WARNING(f'   - Deleted folder: {images_dir}'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'   - Error deleting files: {e}'))
        else:
            self.stdout.write('   - No media folder found to delete.')

        self.stdout.write(self.style.SUCCESS('Successfully cleared all data and media files! 🧹'))