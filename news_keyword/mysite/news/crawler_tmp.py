import requests
from bs4 import BeautifulSoup
from datetime import datetime
from .models import NewsArticle
import json
    
class Crawler():  

    def crawling_for_just_in(self):
        # initialize the list of discovered urls
        # with the first page to visit
        root = "https://www.abc.net.au/"
        urls = ["https://www.abc.net.au/news/justin"]
        
        # header 
        headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86'}

        # until all pages have been visited
        while len(urls) != 0:
            # get the page to visit from the list
            current_url = urls.pop()
        
            # crawling logic
            response = requests.get(current_url, headers=headers)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, "html.parser")
                lates_news = soup.select('#anchor-10719976 > div > div > div > ul > li')
            else : 
                print(response.status_code)
                return None
        
            for news in lates_news:
                # Select the article div container
                article_div = news.select_one("article > div")
                
                # Extract the article URL (href attribute from the <a> tag)
                url = root + article_div.select_one("h3 > a")["href"]
                
                # Extract the article title (from the <a> tag inside the <h3>)
                title = article_div.select_one("h3 > a").get_text(strip=True)

                # Extract the article synopsis (from the <p> tag)
                synopsis = article_div.select_one("div.DetailCard_synopsis__qszdA p").get_text(strip=True)

                # Find the <p> tag
                p_tag = news.find('p', class_="Typography_base__sj2RP")

                # Extract the text from the <p> tag, excluding the <span> (Screen reader only content)
                text = p_tag.get_text(strip=True)

                # Clean up if needed (remove 'Topic:' from the final text)
                article_topic = text.replace('Topic:', '').strip()
                
                # Find the time tag with the datetime attribute
                time_tag = news.find('time', {'datetime': True})
               
                # Extract the datetime string
                datetime_str = time_tag['datetime']
               
                # Convert to a Python datetime object
                parsed_datetime = datetime.strptime(datetime_str, '%Y-%m-%dT%H:%M:%S.%fZ')

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
                    print(f"Article '{title}' already exists in the database.")


            return {'URL': url, 'Title': title, 'Topic': article_topic, 'Synopsis': synopsis, 'Datetime':parsed_datetime}
