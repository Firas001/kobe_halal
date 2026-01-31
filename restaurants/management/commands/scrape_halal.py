import time
import requests
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
                        relative_url = link_tag['href'].strip()
                        detail_url = base_domain + relative_url

                        cat_tag = card.select_one('.card-img-overlay-top .badge')
                        if not cat_tag or cat_tag.text.strip() == "halal":
                            cat_name = "Unknown"
                        else:
                            cat_name = cat_tag.text.strip()
                        
                        category_obj, _ = Category.objects.get_or_create(name=cat_name)

                        self.scrape_single_page(detail_url, p_type, category_obj, kobe_city, headers)
                        
                        time.sleep(1) 

                    except Exception as e:
                        self.stdout.write(self.style.ERROR(f"Error processing card: {e}"))

            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error fetching list {list_url}: {e}"))

    def scrape_single_page(self, url, place_type, category_obj, city_obj, headers):
        self.stdout.write(f"  > Scraping detail: {url}")
        
        try:
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.content, 'html.parser')

            name_tag = soup.select_one('h1.text-shadow')
            name = name_tag.text.strip() if name_tag else "Unknown Name"

            if Place.objects.filter(name=name).exists():
                self.stdout.write(self.style.WARNING(f"    Skipping {name} (Already exists)"))
                return

            description = ""
            about_header = soup.find('h3', string='About')
            if about_header:
                desc_p = about_header.find_next_sibling('p')
                if desc_p:
                    description = desc_p.text.strip()

            address = "Kobe, Japan"
            is_halal = False
            
            rows = soup.select('table.table tr')
            for row in rows:
                th = row.find('th')
                td = row.find('td')
                if not th or not td: continue
                
                header_text = th.text.strip()
                value_text = td.text.strip()

                if "Address" in header_text:
                    address = value_text
                
                if "Halal certification" in header_text:
                    if "Yes" in value_text:
                        is_halal = True

            google_map = f"https://www.google.com/maps/search/?api=1&query={address}"
            image_url = ""
            meta_img = soup.select_one('meta[property="og:image"]')
            if meta_img:
                image_url = meta_img['content']

            place = Place(
                name=name,
                description=description,
                address=address,
                google_map_link=google_map,
                place_type=place_type,
                category=category_obj,
                city=city_obj,
                is_halal_certified=is_halal
            )

            if image_url:
                try:
                    img_response = requests.get(image_url, headers=headers, timeout=10)
                    if img_response.status_code == 200:
                        file_name = f"{name.replace(' ', '_')}.jpg"
                        place.image.save(file_name, ContentFile(img_response.content), save=False)
                except Exception as img_err:
                    self.stdout.write(self.style.WARNING(f"    Image download failed: {img_err}"))

            place.save()
            self.stdout.write(self.style.SUCCESS(f"    Saved: {name}"))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"    Failed to scrape details: {e}"))