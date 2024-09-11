import requests
from bs4 import BeautifulSoup
from datetime import datetime
from .models import NewsArticle
import json
    
class Crawler():  
    
    def crawling_for_just_in(url):
        offset = 0
        size = 250
        total = 250

        # Headers to mimic a real browser request (use your own from the network tab if needed)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
        }
        
        # URL for the AJAX request
        root = "https://www.abc.net.au/"
        url  = 'https://www.abc.net.au/news-web/api/loader/channelrefetch?name=PaginationArticlesFuture&documentId=10719976&prepareParams=%7B%22imagePosition%22%3A%7B%22mobile%22%3A%22right%22%2C%22tablet%22%3A%22right%22%2C%22desktop%22%3A%22right%22%7D%7D&future=true&offset={offset}&size={size}&total={total}'.format(offset = offset, size=size, total=total)
        
        # Make the request
        response = requests.get(url, headers=headers)
        
        # Check the response
        if response.status_code == 200:
            data = response.json()  # Assuming the response is JSON

            # Parse the data
            # Assuming 'data' contains the relevant information you're looking for
            for article in data['collection']:
                try:
                    # Extract the article URL 
                    url = root + article['link']
                    # Extract the article title 
                    title = article['title']
                    # Extract the article last update time 
                    parsed_datetime = datetime.strptime(article['dates']['lastUpdated'], '%Y-%m-%dT%H:%M:%S%z')
                    # Extract the article topic
                    article_topic = article['tags'][0]['title']
                    # Extract the article synopsis 
                    synopsis = article['synopsis']['descriptor']['children'][0]['children'][0]['content']
                
                except Exception as e :
                    print(f"Exception '{e}' " )  
              
                article, created = NewsArticle.objects.get_or_create(
                url = url,
                defaults = {
                    'title': title,
                    'topic' : article_topic,
                    'synopsis' : synopsis,
                    'published_at': parsed_datetime
                    }
                )
                
                if created:
                    print(f"Article '{title}' saved to the database.")
                    
                else:
                     # Check if the article's data has changed
                    if (article.title != title or 
                        article.synopsis != synopsis or 
                        article.published_at != parsed_datetime):
                        
                        # Update the article fields
                        article.title = title
                        article.topic = article_topic
                        article.synopsis = synopsis
                        article.published_at = parsed_datetime
                        article.save()                        
                        
                        print(f"Article '{title}' updated in the database.")
                    else:
                        print(f"Article '{title}' already exists and is up to date.")
                            
        else:
            print(f"Failed to retrieve content: {response.status_code}")
           