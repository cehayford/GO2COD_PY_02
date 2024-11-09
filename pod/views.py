import requests
from bs4 import BeautifulSoup
from django.shortcuts import render, redirect
from django.contrib import messages
from logging import getLogger
from .models import Scrappeddata as scrapy

logger = getLogger(__name__)

def scrape(request):
    """
    View function to handle web scraping requests and display recent scrapes.
    """
    if request.method == 'POST':
        url = request.POST.get('url')
        if not url:
            messages.error(request, 'Please provide a URL')
            return redirect('scrape')
            
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            response = requests.get(url, headers=headers, timeout=15)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            title = soup.title.string if soup.title else 'No title found'
            content = []
            headlines = soup.find_all('h2', class_='content-title')
            span_content = soup.find_all('span', class_='content-span')
            paragraphs = soup.find_all('p', class_="content_paragraph")
            for items in zip(headlines, span_content, paragraphs):
                headline, span, para = items
                content_item = {
                    'headline': headline.get_text(strip=True) if headline else '',
                    'span': span.get_text(strip=True) if span else '',
                    'paragraph': para.get_text(strip=True) if para else ''
                }
                content.append(content_item)
            content_str = '\n'.join(
                f"Headline: {item['headline']}\n"
                f"Span: {item['span']}\n"
                f"Paragraph: {item['paragraph']}\n"
                for item in content
            )
            scrapped_data = scrapy.objects.create(url=url, content=content_str, title=title)
            
            messages.success(request, 'Website scraped successfully!')
            return redirect('scraping_results', pk=scrapped_data.pk)
            
        except requests.ConnectionError:
            logger.error(f"Connection error while scraping {url}")
            messages.error(request, 'Could not connect to the website. Please check the URL and try again.')
        
        except requests.Timeout:
            logger.error(f"Timeout while scraping {url}")
            messages.error(request, 'The request timed out. Please try again.')
        
        except requests.RequestException as e:
            logger.error(f"Request error while scraping {url}: {str(e)}")
            messages.error(request, 'Error accessing the website. Please check the URL and try again.')
        
        except Exception as e:
            logger.error(f"Unexpected error while scraping {url}: {str(e)}")
            messages.error(request, 'An unexpected error occurred. Please try again later.')
    
    # Get recent scrapes for display
    recent_scrapes = scrapy.objects.all()
    return render(request, 'pod/entrypage.html', {'recent_scrapes': recent_scrapes})

def results(request, pk):
    try:
        scrapped_data = scrapy.objects.get(pk=pk)
        print(scrapped_data.content + "temi")
        return render(request, 'pod/results.html', {'data': scrapped_data})
    except scrapy.DoesNotExist:
        messages.error(request, 'Requested scrape data not found.')
        return redirect('scrape')