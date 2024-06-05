"""
Australia Nintendo eShop Discount Scraper

This script scrapes the current offers from the Nintendo eShop and saves the following information into a JSON file:
- title
- original price ($AUD)
- special price ($AUD)

Main Functions:
- fetch_html(url): Fetches the HTML content from the given URL.
- parse_game_details(game): Parses the game details (title, original price, special price) from a BeautifulSoup tag.
- scrape_nintendo_offers(): Orchestrates the scraping process, iterates through all offer pages, collects game details,
and saves them to a JSON file.

Usage:
Run this script directly to scrape the Nintendo eShop offers and save as json file.

Dependencies:
- requests
- json
- time
- BeautifulSoup (bs4)
- datetime

Example:
$ python nintendo_scraper.py
"""

import requests
import json
import time
from bs4 import BeautifulSoup
from datetime import date


def main():
    # DD-MM-YYYY
    today_date = date.today().strftime("%d-%m-%Y")
    scrape_nintendo_offers(today_date)


def get_soup(url):
    """
    Fetches HTML content from the given URL into a BeautifulSoup object.

    Parameters:
    url (str): The URL to fetch HTML content from.

    Returns:
    str: The HTML content of the page if the request is successful.
    None: If there is an error during the request.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
        print(f'Connection successful\n')
        return BeautifulSoup(response.text, 'lxml')
    except requests.RequestException as e:
        print(f'Error fetching URL {url}: {e}')
        return None


def parse_game_details(game):
    """
    Parses the game details.

    Parameters:
    game: The BeautifulSoup tag containing the game details.

    Returns:
    dict: A dictionary with the title, original price, and special price of the game.
    """
    try:
        title_element = game.find('strong', class_='product name product-item-name')
        title = title_element.text.strip()
    except AttributeError:
        title = 'N/A'

    try:
        original_price_element = game.find('span', class_='old-price')
        original_price_text = original_price_element.text.replace(' ', '').replace('RegularPrice', '').strip()
        original_price = float(original_price_text[1:])
    except AttributeError:
        original_price = 'N/A'

    try:
        special_price_element = game.find('span', class_='special-price')
        special_price_text = special_price_element.text.replace(' ', '').replace('SpecialPrice', '').strip()
        special_price = float(special_price_text[1:])
    except AttributeError:
        special_price = 'N/A'

    return {
        'title': title,
        'original_price': original_price,
        'special_price': special_price
    }


def scrape_nintendo_offers(today_date):
    """
    The core function that scrapes Nintendo eShop current offers and saves them to a JSON file.

    This function iterates through all the pages of the Nintendo eShop's current offers section,
    collects the details of each game on offer, and saves the data to a JSON file.
    """
    BASE_URL = 'https://store.nintendo.com.au/au/nintendo-eshop/current-offers?p='
    catalogue = []
    page = 1
    total_games = 0
    failed_game_scrapes = 0
    total_pages = 0
    start_time = time.time()

    while True:
        soup = get_soup(f'{BASE_URL}{page}')
        if not soup:
            break

        games = soup.find_all('li', class_='item product product-item')

        if not games:
            break

        total_pages += 1

        for game in games:
            game_details = parse_game_details(game)
            if not game_details \
                    or game_details['title'] == 'N/A' \
                    or game_details['original_price'] == 'N/A' \
                    or game_details['special_price'] == 'N/A':
                failed_game_scrapes += 1
                total_games += 1
                continue
            catalogue.append(game_details)

            total_games += 1

            print(f'#{total_games}')
            print(f"{game_details['title']}")
            print(f"Original Price: ${game_details['original_price']:.2f}")
            print(f"Special Price: ${game_details['special_price']:.2f}\n")

        page += 1

    end_time = time.time()
    runtime_minutes = (end_time - start_time) / 60
    scrape_success_rate = (total_games - failed_game_scrapes) / total_games

    print(f'Statistics')
    print(f'Total pages: {total_pages}')
    print(f'Total games: {total_games}')
    print(f'Unsuccessful game scrapes: {failed_game_scrapes}')
    print(f'Scrape Success Rate: {scrape_success_rate * 100:.2f}%')
    print(f'Runtime: {runtime_minutes:.2f} minute\n')

    # Save catalogue as JSON
    with open(f'nintendo_discount_catalogue_{today_date}.json', 'w') as json_file:
        json.dump(catalogue, json_file, indent=4)


if __name__ == "__main__":
    main()
