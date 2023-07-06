import csv
import requests
from bs4 import BeautifulSoup


# Function to scrape product listing pages
def scrape_product_listings(url):
    # Send a GET request to the URL
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    products = [ ]

    # Find all the product listing items on the page
    listings = soup.find_all('div', {'data-component-type': 's-search-result'})

    # Iterate over each product listing item and extract the required information
    for listing in listings:
        product = {}

        # Extract product URL
        url_element = listing.find('a', class_='a-link-normal')
        if url_element:
            product [ 'URL' ] = 'https://www.amazon.in' + url_element [ 'href' ]

        # Extract product name
        name_element = listing.find('span', class_='a-size-medium')
        if name_element:
            product [ 'Name' ] = name_element.text

        # Extract product price
        price_element = listing.find('span', class_='a-offscreen')
        if price_element:
            product [ 'Price' ] = price_element.text

        # Extract rating
        rating_element = listing.find('span', class_='a-icon-alt')
        if rating_element:
            product [ 'Rating' ] = rating_element.text

        # Extract number of reviews
        reviews_element = listing.find('span', class_='a-size-base')
        if reviews_element:
            product [ 'Number of Reviews' ] = reviews_element.text

        products.append(product)

    return products


# Function to scrape product details from individual URLs
def scrape_product_details(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    product_details = {}

    # Extract description, ASIN, product description, and manufacturer from the product page
    description_element = soup.find('div', id='productDescription')
    if description_element:
        product_details [ 'Description' ] = description_element.text.strip( )

    asin_element = soup.find('th', string='ASIN')
    if asin_element:
        product_details [ 'ASIN' ] = asin_element.find_next('td').text.strip( )

    product_description_element = soup.find('div', id='productDescription_feature_div')
    if product_description_element:
        product_details [ 'Product Description' ] = product_description_element.text.strip( )

    manufacturer_element = soup.find('th', string='Manufacturer')
    if manufacturer_element:
        product_details [ 'Manufacturer' ] = manufacturer_element.find_next('td').text.strip( )

    return product_details


# Main code

# Scrape product listing pages
products = [ ]
for page_number in range(1, 21):
    url = f'https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_{page_number}'
    products += scrape_product_listings(url)

# Scrape product details for each product URL
for product in products:
    if 'URL' in product:
        product_url = product [ 'URL' ]
        product_details = scrape_product_details(product_url)
        product.update(product_details)

# Export data to CSV
csv_file = 'scraped_data.csv'
headers = [ 'URL', 'Name', 'Price', 'Rating', 'Number of Reviews', 'Description', 'ASIN', 'Product Description',
            'Manufacturer' ]

with open(csv_file, 'w', encoding='utf-8', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=headers)
    writer.writeheader( )

    for product in products:
        writer.writerow(product)

print(f"Data exported to {csv_file} successfully.")

