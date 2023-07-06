import requests
from bs4 import BeautifulSoup
import csv
import time


def scrape_product_listing_page(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    products = soup.find_all('div', {'data-component-type': 's-search-result'})

    for product in products:
        product_link = product.find('a', {'class': 'a-link-normal s-no-outline'})
        if product_link:
            product_url = 'https://www.amazon.in' + product_link['href']
            
            product_name_elem = product.find('span', {'class': 'a-size-base-plus a-color-base a-text-normal'})
            if product_name_elem:
                product_name = product_name_elem.text.strip()
            else:
                product_name = 'Loading Failed'
            
            product_price_elem = product.find('span', {'class': 'a-offscreen'})
            if product_price_elem:
                product_price = product_price_elem.text.strip()
            else:
                product_price = 'N/A'
            
            rating_elem = product.find('span', {'class': 'a-icon-alt'})
            if rating_elem:
                rating = rating_elem.text.split(' ')[0]
            else:
                rating = 'N/A'
            
            num_reviews_elem = product.find('span', {'class': 'a-size-base'})
            if num_reviews_elem:
                num_reviews = num_reviews_elem.text.strip().replace(',', '')
            else:
                num_reviews = 'N/A'

            writer.writerow([product_url, product_name, product_price, rating, num_reviews])



csv_file = open('amazon_products.csv', 'w', newline='', encoding='utf-8')
writer = csv.writer(csv_file)
headers = ['Product URL', 'Product Name', 'Product Price', 'Rating', 'Number of Reviews']
writer.writerow(headers)

base_url = 'https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_'
num_pages = 20

for page in range(1, num_pages + 1):
    url = base_url + str(page)
    scrape_product_listing_page(url)
    time.sleep(2)  # Delay between requests to avoid overwhelming the server

csv_file.close()

csv_file = open('amazon_products.csv', 'r', newline='', encoding='utf-8')
reader = csv.reader(csv_file)
next(reader)  # Skip header row

csv_file_new = open('amazon_product_details.csv', 'w', newline='', encoding='utf-8')
writer_new = csv.writer(csv_file_new)
headers_new = ['Product URL', 'Description', 'ASIN', 'Product Description', 'Manufacturer']
writer_new.writerow(headers_new)

count = 0
for row in reader:
    product_url = row[0]
    scrape_product_listing_page(product_url)
    count += 1
    if count % 10 == 0:
        print(f'Scraped {count} product URLs. Waiting for 2 seconds...')
        time.sleep(2)

csv_file.close()
csv_file_new.close()