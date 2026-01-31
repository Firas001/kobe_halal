import time
import requests
import re
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from restaurants.models import Place, Category, City

class Command(BaseCommand):
    help = 'Scrape data from Halal Food in Japan'

    def handle(self, *args, **kwargs):
        urls = [
            ('restaurant', 'https://www.halalfoodinjapan.com/restaurant/Hyogo/AREAL3502/'),
            ('restaurant', 'https://www.halalfoodinjapan.com/restaurant/Hyogo/AREAL3512/'),
            ('grocery', 'https://www.halalfoodinjapan.com/grocery/Hyogo/AREAL3502/'),
        ]

        base_domain = "https://www.halalfoodinjapan.com"
        kobe_city, _ = City.objects.get_or_create(name="Kobe")

        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'
        }

        for p_type, list_url in urls:
            self.stdout.write(f"Scraping list: {list_url}")
            try:
                response = requests.get(list_url, headers=headers)
                soup = BeautifulSoup(response.content, 'html.parser')
                cards = soup.select('.card-groups')

                for card in cards:
                    try:
                        link_tag = card.select_one('.tile-link')
                        if not link_tag: continue
                        detail_url = base_domain + link_tag['href'].strip()

                        cat_tag = card.select_one('.card-img-overlay-top .badge')
                        cat_name = cat_tag.text.strip() if cat_tag and cat_tag.text.strip() != "halal" else "Unknown"
                        category_obj, _ = Category.objects.get_or_create(name=cat_name)

                        self.scrape_single_page(detail_url, p_type, category_obj, kobe_city, headers)
                        time.sleep(1)

                    except Exception as e:
                        self.stdout.write(self.style.ERROR(f"Error processing card: {e}"))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error fetching list: {e}"))

    def scrape_single_page(self, url, place_type, category_obj, city_obj, headers):
        self.stdout.write(f"  > Scraping detail: {url}")
        
        try:
            response = requests.get(url, headers=headers)
            content = response.content.decode('utf-8')
            soup = BeautifulSoup(content, 'html.parser')

            name = soup.select_one('h1.text-shadow').text.strip() if soup.select_one('h1.text-shadow') else "Unknown"

            if Place.objects.filter(name=name).exists():
                self.stdout.write(self.style.WARNING(f"    Skipping {name} (Already exists)"))
                return

            coordinates = None
            match = re.search(r'new google\.maps\.LatLng\(\s*([0-9\.]+)\s*,\s*([0-9\.]+)\s*\)', content)
            if match:
                lat = match.group(1)
                lng = match.group(2)
                coordinates = f"{lat},{lng}"
                self.stdout.write(f"    Found coordinates: {coordinates}")

            description = ""
            about_header = soup.find('h3', string='About')
            if about_header and about_header.find_next_sibling('p'):
                description = about_header.find_next_sibling('p').text.strip()

            address = "Kobe, Japan"
            is_halal = False
            for row in soup.select('table.table tr'):
                th = row.find('th')
                td = row.find('td')
                if th and td:
                    if "Address" in th.text: address = td.text.strip()
                    if "Halal certification" in th.text and "Yes" in td.text: is_halal = True

            place = Place(
                name=name,
                description=description,
                address=address,
                coordinates=coordinates,
                place_type=place_type,
                category=category_obj,
                city=city_obj,
                is_halal_certified=is_halal
            )

            meta_img = soup.select_one('meta[property="og:image"]')
            if meta_img:
                try:
                    img_resp = requests.get(meta_img['content'], headers=headers, timeout=10)
                    if img_resp.status_code == 200:
                        place.image.save(f"{name.replace(' ', '_')}.jpg", ContentFile(img_resp.content), save=False)
                except: pass

            place.save()
            self.stdout.write(self.style.SUCCESS(f"    Saved: {name}"))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"    Failed: {e}"))