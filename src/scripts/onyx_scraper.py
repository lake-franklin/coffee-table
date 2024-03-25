import requests
from bs4 import BeautifulSoup
import json

# Function to scrape product names and URLs from the main webpage
url = 'https://onyxcoffeelab.com/collections/coffee/type:single-origin'
pages = ['type:single-origin', 'type:blend']
def scrape_product_info(url):
    # Send a GET request to the webpage
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content of the webpage
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find all elements containing product information
        product_info = soup.find_all('div', class_='product-preview')

        # Dictionary to store product names and URLs
        products = {}
        for item in product_info:
            product_name = item.find('h3', class_='title upper').text.strip()
            product_url = item.find('a', class_='product-preview')['href']
            products[product_name] = product_url

        return products
    else:
        print("Failed to retrieve data from the webpage.")
        return {}

# Function to scrape data from individual product pages
def scrape_product_data(base_url, product_urls):
    # Dictionary to store product data
    product_dict = {}

    # Scrape data from individual product pages
    for product_name, product_url in product_urls.items():
        full_product_url = f"{base_url}{product_url}"
        response = requests.get(full_product_url)

        # Check if the request was successful
        if response.status_code == 200:
            # Parse the HTML content of the product page
            soup = BeautifulSoup(response.content, 'html.parser')

            # Extract relevant data from the product page
            product_data = {
                'name': product_name,
                'price': soup.find('span', class_='price').text.strip(),
                # Add more fields as needed
            }

            product_dict[product_name] = product_data
        else:
            print(f"Failed to retrieve data from the product page: {full_product_url}")

    return product_dict

# Main function to orchestrate the scraping process
def get_beans(prod_type:str = 'single-origin'):
    # URL of the main webpage containing product listings
    main_page_url = url
    # Base URL of individual product pages
    base_product_urls = 'INSERT_BASE_PRODUCT_URL_HERE'

    # Scrape product names and URLs from the main webpage
    product_info = scrape_product_info(main_page_url)

    for base_url in base_product_urls:
        # Scrape data from individual product pages
        product_data = scrape_product_data(base_url, product_info)

        # Save the product data dictionary to a JSON file
        with open('product_data.json', 'w') as json_file:
            json.dump(product_data, json_file, indent=4)

    print("Product data saved to 'product_data.json'.")


