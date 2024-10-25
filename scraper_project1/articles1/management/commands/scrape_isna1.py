import requests
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand
from django.apps import apps
from datetime import datetime
from persiantools.jdatetime import JalaliDate
import logging

logger = logging.getLogger(__name__)

Article = apps.get_model('articles1', 'Article')

class Command(BaseCommand):
    help = 'Scrapes articles from ISNA Culture and Art section'

    def handle(self, *args, **kwargs):
        url = 'https://www.isna.ir/service/Culture-Art'
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise an exception for HTTP errors
        except requests.RequestException as e:
            logger.error(f"Failed to retrieve content from {url}: {e}")
            return
        soup = BeautifulSoup(response.content, 'html.parser')

        new_articles_count = 0
        skipped_articles_count = 0

        section_box6 = soup.find('section', id='box6')

        if not section_box6:
            self.stdout.write(self.style.ERROR('No articles section found.'))
            return

        articles = section_box6.find_all('div', class_='desc')

        with open('text.html', 'w', encoding='utf-8') as text_file:
            text_file.write(str(articles))
        print(f"Found {len(articles)} articles.")

        for article in articles:
            title_element = article.find('h3')
            date_element = article.find('time')
            content_element = article.find('p')
            url_element = article.find('a')  # Assuming the URL is in an <a> tag

            if title_element is None:
                print("No title found for this article.")
                continue

            title = title_element.text.strip()
            article_url = url_element['href'] if url_element and 'href' in url_element.attrs else None
            if not article_url:
                print("No URL found for this article.")
                continue

            if date_element is not None:
                date_str = date_element.find('span').text.strip() if date_element.find('span') else 'Unknown Date'
                if date_str != 'Unknown Date':
                    try:
                        # Convert from Jalali to Gregorian
                        date_published = JalaliDate.fromisoformat(date_str).to_gregorian()
                        # Format as ISO (YYYY-MM-DD)
                        date_published = date_published.strftime('%Y-%m-%d')
                    except ValueError:
                        date_published = None
                        print(f"Date parsing failed for: {date_str}")
                else:
                    date_published = None
                    print("No date found for this article.")

            content = content_element.text.strip() if content_element else 'No content available.'

            # Check for duplicates using the title
            if not Article.objects.filter(title=title).exists():
                Article.objects.create(title=title, date_published=date_published, content=content, url=article_url)
                print(f"Saved article: {title}")
                new_articles_count += 1
            else:
                print(f"Skipping duplicate article: {title}")
                skipped_articles_count += 1

        self.stdout.write(self.style.SUCCESS(f'Scraped {new_articles_count} new articles.'))
        self.stdout.write(self.style.WARNING(f'Skipped {skipped_articles_count} duplicate articles.'))
