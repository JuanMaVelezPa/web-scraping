# Developer Information
# Name: Juan Manuel Velez Parra
# Email: juanmavelezpa@gmail.com
# Date: 2025-09-18
# Description: Web scraping script to monitor product prices from multiple e-commerce websites.
# The logic is separated by client for greater control and stability.

# ==============================================================================
# 1. Web Scraping Functions per Client
# ==============================================================================
import requests
from bs4 import BeautifulSoup
import csv
import datetime
import time
import re
import json
from urllib.parse import urlparse
import concurrent.futures
import random

def scrape_duquin(url):
    try:
        headers = {'User-Agent': random.choice(USER_AGENTS)}
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        product_name_tag = soup.find('h1', class_='vtex-store-components-3-x-productNameContainer')
        name = product_name_tag.text.strip() if product_name_tag else None
        
        price_tag = soup.find('span', class_='vtex-product-price-1-x-sellingPrice')
        price = None
        if price_tag:
            price_text = price_tag.text.strip()
            clean_price = re.sub(r'[^\d.]', '', price_text)
            price = float(clean_price.replace('.', ''))
            
        return {'product_name': name, 'price': price}

    except Exception as e:
        print(f"Error during Duquin scraping: {e}")
        return None

def scrape_electromillonaria(url):
    try:
        headers = {'User-Agent': random.choice(USER_AGENTS)}
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        product_name_tag = soup.find('h1', class_='product_title')
        name = product_name_tag.text.strip() if product_name_tag else None
        
        price_tag = soup.find('p', class_='price').find('span', class_='woocommerce-Price-amount')
        price = None
        if price_tag:
            price_text = price_tag.text.strip()
            clean_price = re.sub(r'[^\d.]', '', price_text)
            price = float(clean_price.replace('.', ''))

        return {'product_name': name, 'price': price}

    except Exception as e:
        print(f"Error during Electromillonaria scraping: {e}")
        return None

def scrape_hogarymoda(url):
    try:
        headers = {'User-Agent': random.choice(USER_AGENTS)}
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')

        product_name_tag = soup.find('h1', class_='hdt-product__title')
        name = product_name_tag.text.strip() if product_name_tag else None
        
        price_container = soup.find('hdt-price')
        if price_container:
            price_tag = price_container.find('span', class_='hdt-money')
        
        price = None
        if price_tag:
            price_text = price_tag.text.strip()
            clean_price = re.sub(r'[^\d.]', '', price_text)
            price = float(clean_price.replace('.', ''))
            
        return {'product_name': name, 'price': price}

    except Exception as e:
        print(f"Error during HogarYModa scraping: {e}")
        return None

def scrape_luma(url):
    try:
        headers = {'User-Agent': random.choice(USER_AGENTS)}
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        product_name_tag = soup.find('h1', class_='product-name')
        name = product_name_tag.text.strip() if product_name_tag else None
        
        price_tag = soup.find('div', class_='product-price mar-bottom-10')
        price = None
        if price_tag:
            price_text = price_tag.text.strip()
            clean_price = re.sub(r'[^\d.]', '', price_text)
            price = float(clean_price.replace('.', ''))
            
        return {'product_name': name, 'price': price}

    except Exception as e:
        print(f"Error during Luma scraping: {e}")
        return None
    
def scrape_innovar(url):
    try:
        headers = {'User-Agent': random.choice(USER_AGENTS)}
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        product_name_tag = soup.find('div', class_='product__title')
        name = product_name_tag.text.strip() if product_name_tag else None
        
        section_name = soup.find('div', class_='no-js-hidden mainp-price')
        price_tag = section_name.find('span', class_='price-item--last')
        
        if price_tag:
            price_text = price_tag.text.strip()
            clean_price = re.sub(r'[^\d.]', '', price_text)
            price = float(clean_price.replace('.', ''))
            
        return {'product_name': name, 'price': price}

    except Exception as e:
        print(f"Error during Innovar scraping: {e}")
        return None    

def scrape_towncenter(url):
    try:
        headers = {'User-Agent': random.choice(USER_AGENTS)}
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        product_name_tag = soup.find('h1', class_='product_title')
        name = product_name_tag.text.strip() if product_name_tag else None
        
        price_tag = soup.find('p', class_='price').find('ins')
        price = None
        if price_tag:
            price_text = price_tag.text.strip()
            clean_price = re.sub(r'[^\d.]', '', price_text)
            price = float(clean_price.replace('.', ''))

        if price is None:
            price_tag = soup.find('p', class_='price').find('span', class_='woocommerce-Price-amount')
            if price_tag:
                price_text = price_tag.text.strip()
                clean_price = re.sub(r'[^\d.]', '', price_text)
                price = float(clean_price.replace('.', ''))
            

        return {'product_name': name, 'price': price}

    except Exception as e:
        print(f"Error during Towncenter scraping: {e}")
        return None
    
def scrape_electrojaponesa(url):
    try:
        headers = {'User-Agent': random.choice(USER_AGENTS)}
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        product_name_tag = soup.find('h1', class_='vtex-store-components-3-x-productNameContainer')
        name = product_name_tag.text.strip() if product_name_tag else None
        
        price_tag = soup.find('span', class_='vtex-product-price-1-x-sellingPrice')
        price = None
        if price_tag:
            price_text = price_tag.text.strip()
            clean_price = re.sub(r'[^\d.]', '', price_text)
            price = float(clean_price.replace('.', ''))
            
        return {'product_name': name, 'price': price}

    except Exception as e:
        print(f"Error during Electrojaponesa scraping: {e}")
        return None

def scrape_masion(url):
    try:
        headers = {'User-Agent': random.choice(USER_AGENTS)}
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        product_name_tag = soup.find('h1', class_='h1 page-title')
        name = product_name_tag.text.strip() if product_name_tag else None
        
        price_tag = soup.find('span', itemprop='price')
        price = None
        if price_tag:
            price_text = price_tag.text.strip()
            clean_price = re.sub(r'[^\d]', '', price_text)
            price = float(clean_price)

        return {'product_name': name, 'price': price}

    except Exception as e:
        print(f"Error during Masion scraping: {e}")
        return None
    
def scrape_lagobo(url):
    try:
        headers = {'User-Agent': random.choice(USER_AGENTS)}
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        product_name_tag = soup.find('div', class_='product-data').find('div', class_='product-name').find('div', class_='productName')
        name = product_name_tag.text.strip() if product_name_tag else None

        price_container = soup.find('div', class_='product-data').find('div', class_='plugin-preco').find('strong', class_='skuPrice')
        price = None
        if price_container:
            price_text = price_container.get_text(strip=True)
            clean_price = re.sub(r'[^\d]', '', price_text)
            price = int(clean_price)

        return {'product_name': name, 'price': price}

    except Exception as e:
        print(f"Error during Oportunidades scraping: {e}")
        return None
    
# =======================================================================
# 2. Main Program Logic
# ==============================================================================

CLIENT_SCRAPERS = {
    'Duquin': scrape_duquin,
    'Electromillonaria': scrape_electromillonaria,
    'HogarYModa': scrape_hogarymoda,
    'Luma': scrape_luma,
    'Innovar': scrape_innovar,
    'Towncenter': scrape_towncenter,
    'Electrojaponesa': scrape_electrojaponesa,
    'Masion': scrape_masion,
    'Lagobo': scrape_lagobo,
}

USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/603.2.4 (KHTML, like Gecko) Version/10.1.1 Safari/603.2.4',
]

def save_data_to_csv(client, code, product_name, price):
    consolidated_file = 'consolidated_prices.csv'
    current_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

    columns = ['Client', 'Date', 'Product_Name', 'Price', 'Code']

    with open(consolidated_file, 'a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=columns)
        
        if f.tell() == 0:
            writer.writeheader()
        
        writer.writerow({
            'Client': client,
            'Date': current_date,
            'Product_Name': product_name,
            'Price': price,
            'Code': code
        })
        print(f"Data saved to consolidated file: {client}")

def main_optimized(input_file):
    import datetime
    import time

    start_time = datetime.datetime.now()
    print(f"[{start_time.strftime('%Y-%m-%d %H:%M:%S')}] --- Starting price monitoring process ---")

    try:
        with open(input_file, mode='r', encoding='utf-8') as infile:
            reader = csv.DictReader(infile)
            urls_to_scrape = list(reader)

        with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
            futures = {executor.submit(CLIENT_SCRAPERS.get(row['Client']), row['Url']): row for row in urls_to_scrape}

            for future in concurrent.futures.as_completed(futures):
                row = futures[future]
                client = row['Client']
                code = row['Code']
                url = row['Url']
                
                try:
                    data = future.result()
                    if data:
                        current_time = datetime.datetime.now().strftime('%H:%M:%S')
                        print(f"[{current_time}] Processing product for {client} at {code}...")
                        save_data_to_csv(client, code, data['product_name'], data['price'])
                    else:
                        print(f"Failed to get data for {client} at {code}.")
                except Exception as e:
                    print(f"An error occurred while scraping {client} at {code}: {e}")
                    
    except FileNotFoundError:
        print(f"Error: Input file '{input_file}' not found.")
    except Exception as e:
        print(f"An unexpected error occurred in the main logic: {e}")

    end_time = datetime.datetime.now()
    total_time = end_time - start_time
    total_minutes = total_time.total_seconds() / 60
    
    print(f"\n[{end_time.strftime('%Y-%m-%d %H:%M:%S')}] --- Process finished. ---")
    print(f"Total execution time: {total_time} (approx. {total_minutes:.2f} minutes)")

if __name__ == '__main__':
    main_optimized('productos_a_monitorear.csv')
    print("\nPrice monitoring process finished.")