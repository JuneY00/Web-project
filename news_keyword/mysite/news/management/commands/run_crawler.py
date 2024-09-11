from django.core.management.base import BaseCommand
from news.crawler import Crawler

class Command(BaseCommand):
    help = 'Run news crawler'
    
    def handle(self, *args, **kwargs):
        crawler = Crawler()
        crawler.crawling_for_just_in()