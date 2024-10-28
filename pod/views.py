import requests
from bs4 import BeautifulSoup
from django.shortcuts import render
from django.http import JsonResponse

def scrape(request):
    data = None
    error = None

    if request.method == 'POST':
        url = request.POST.get('url')
        response = requests.get(url)

        # Check if the request was successful
        if response.status_code != 200:
            error = 'Failed to retrieve the page.'
        else:
            # Parse the HTML content
            soup = BeautifulSoup(response.text, 'html.parser')

            # Extract specific data
            headlines = soup.find_all('h2', class_='product-title')  # Adjust based on the website structure
            prices = soup.find_all('span', class_='product-price')   # Adjust based on the website structure

            # Prepare the extracted data
            data = []
            for headline, price in zip(headlines, prices):
                data.append({
                    'headline': headline.get_text(strip=True),
                    'price': price.get_text(strip=True),
                })

    return render(request, 'pod/entrypage.html', {'data': data, 'error': error})