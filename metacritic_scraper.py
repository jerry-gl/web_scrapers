"""
Metacritic Game Info Scraper

Given the game title in JSON file, this script scrapes information about video games from Metacritic
and saves the following additional information into a CSV file:
- meta_score
- meta_reviews
- user_score
- user_reviews
- release_date
- publisher
- genre

Main Functions:
- create_metacritic_url(title): Constructs the Metacritic URL for a given game title.
- get_soup(url, headers): Fetches the HTML content from the given URL and returns a BeautifulSoup object.
- parse_game_info(game): Parses detailed game information from a BeautifulSoup tag.
- scrape_game_info(json_file): Orchestrates the scraping process, iterates through the game titles in the JSON file,
 then collects game details, and saves them to a CSV file.

Usage:
Make sure the json file is named f'{platform}_discount_catalogue_{today_date}.json'
Run this script directly to scrape the game's information from Metacritic.


Dependencies:
- BeautifulSoup (bs4)
- pandas
- requests
- datetime
- re
- json
- time

Example:
$ python metacritic_scraper.py
"""


import pandas as pd
import re
import requests
import json
import time
import sys
from bs4 import BeautifulSoup
from datetime import date, datetime


def main():
    platform = input("Please enter the platform (e.g., 'steam' or 'nintendo'): ").strip().lower()
    # DD-MM-YYYY format
    today_date = date.today().strftime("%d-%m-%Y")
    create_metacritic_url_example()
    scrape_game_info(f'{platform}_discount_catalogue_{today_date}.json', today_date, platform)


def create_metacritic_url(title):
    """
    Create a Metacritic URL from the game's title using regular expressions.

    Parameters:
    title (str): The title of the game.

    Returns:
    str: The constructed Metacritic URL for the given game title.
    """
    BASE_URL = 'https://www.metacritic.com/game/'
    # removes special symbols except '+'
    mod_title = (re.sub(r'[^\w\s+-]', '', title)
                   .strip()
                   .lower())
    # remove hyphens if there are spaces before and after the hyphen
    mod_title = re.sub(r'\s-\s', ' ', mod_title)
    # replaces the '+' symbol with the word 'plus'
    mod_title = re.sub(r'\+', 'plus', mod_title)
    # replaces one or more consecutive whitespaces with '-'
    mod_title = re.sub(r'\s+', '-', mod_title)
    # remove the word "edition" and the word preceding it.
    mod_title = re.sub(r'-\w+-edition$', '', mod_title, flags=re.IGNORECASE)
    return f'{BASE_URL}{mod_title}/'


def create_metacritic_url_example():
    example_titles = [
        'Arcade Archives NEW RALLY-X',
        'Overcooked! 2 - Gourmet Edition',
        'Cynthia: Hidden in the Moonshadow - Premium Edition',
        'Notes + Stickers Complete Edition'
    ]
    example_metacritic_urls = [create_metacritic_url(title) for title in example_titles]
    for example_title, example_metacritic_url in zip(example_titles, example_metacritic_urls):
        print(f'Converted "{example_title}" into the Metacritic URL: {example_metacritic_url}')
    print()


def get_soup(url, headers):
    """
    Request a URL and return a BeautifulSoup object.

    Parameters:
    url (str): The URL to request.
    headers (dict): The request headers to simulate a browser request.

    Returns:
    BeautifulSoup object: The parsed HTML content of the URL if the request is successful.
    None: If the request fails or an exception occurs.
    """
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return BeautifulSoup(response.text, 'lxml')
    except requests.RequestException as e:
        print(f'{e}\n')
        return None


def parse_game_info(game):
    """
    Scrapes and parses the game's details into a dictionary.

    Parameters:
    game (BeautifulSoup): The parsed HTML content of the game's Metacritic page.

    Returns:
    dict: A dictionary containing the game's detailed information:
        - meta_score (str or None)
        - meta_reviews (str or None)
        - user_score (str or None)
        - user_reviews (str or None)
        - release_date (date or None)
        - publisher (str or None)
        - genre (str or None)
    """
    try:
        meta_score = game.find('div', class_='c-productScoreInfo u-clearfix g-inner-spacing-bottom-medium') \
                         .find('div', class_='c-siteReviewScore_background c-siteReviewScore_background-critic_medium')\
                         .find('span') \
                         .text
        if meta_score.lower() == 'tbd':
            meta_score = None
    except AttributeError:
        meta_score = None

    try:
        meta_reviews_text = game.find('div', class_='c-productScoreInfo u-clearfix g-inner-spacing-bottom-medium') \
                                .find('span', class_='c-productScoreInfo_reviewsTotal u-block') \
                                .find('span') \
                                .text
        meta_reviews = re.search(r'\d{1,3}(?:,\d{3})*', meta_reviews_text).group().replace(',', '')
    except AttributeError:
        meta_reviews = None

    try:
        user_score = game.find('div', class_='c-siteReviewScore_background c-siteReviewScore_background-user') \
                         .find('span') \
                         .text
        if user_score.lower() == 'tbd':
            user_score = None
    except AttributeError:
        user_score = None

    try:
        user_reviews_text = game.find('div', class_='c-productScoreInfo u-clearfix') \
                                .find('span', class_='c-productScoreInfo_reviewsTotal u-block') \
                                .find('span') \
                                .text
        user_reviews = re.search(r'\d{1,3}(?:,\d{3})*', user_reviews_text).group().replace(',', '')
    except AttributeError:
        user_reviews = None

    try:
        release_date_string = game.find('div', class_='c-gameDetails_ReleaseDate u-flexbox u-flexbox-row') \
                                  .find('span', class_="g-outer-spacing-left-medium-fluid g-color-gray70 u-block") \
                                  .text
        release_date = datetime.strptime(release_date_string, '%b %d, %Y').strftime('%d-%m-%Y')
    except AttributeError:
        release_date = None

    try:
        publisher = game.find('div', class_='c-gameDetails_Distributor u-flexbox u-flexbox-row') \
                        .find('span', class_='g-outer-spacing-left-medium-fluid g-color-gray70 u-block') \
                        .text
    except AttributeError:
        publisher = None

    try:
        genre = game.find('li', class_='c-genreList_item') \
                    .find('span', class_='c-globalButton_label') \
                    .text \
                    .strip()
    except AttributeError:
        genre = None

    return {
        'meta_score': meta_score,
        'meta_reviews': meta_reviews,
        'user_score': user_score,
        'user_reviews': user_reviews,
        'release_date': release_date,
        'publisher': publisher,
        'genre': genre,
    }


def scrape_game_info(json_file, today_date, platform):
    """
    Core function that orchestrates the scraping process,
    iterates through the game titles in the JSON file, collects game details, and saves them to a CSV file.

    Parameters:
    json_file (str): The path to the JSON file containing the game catalogue.

    Returns:
    None: This function does not return a value. Instead, it performs side effects such as printing information
    to the console and writing results to a CSV file.
    """
    start_time = time.time()
    total_game_info_scraped = 0
    request_headers = {
        'User-Agent': ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                       "AppleWebKit/537.36 (KHTML, like Gecko) "
                       "Chrome/113.0.0.0 Safari/537.36")
    }

    try:
        with open(json_file, 'r') as json_file:
            catalogue = json.load(json_file)
    except FileNotFoundError:
        print(f"Error: The file '{json_file}' was not found.")
        sys.exit(1)

    for game in catalogue:
        title = game['title']
        url = create_metacritic_url(title)
        soup = get_soup(url, request_headers)

        if soup:
            game_info = parse_game_info(soup)
            total_game_info_scraped += 1

            print(f'#{total_game_info_scraped}')
            print(f'"{title}"')
            print(f"Meta Score: {game_info['meta_score']}")
            print(f"Meta Reviews: {game_info['meta_reviews']}")
            print(f"User Score: {game_info['user_score']}")
            print(f"User Reviews: {game_info['user_reviews']}")
            print(f"Release Date: {game_info['release_date']}")
            print(f"Publisher: {game_info['publisher']}")
            print(f"Genre: {game_info['genre']}\n")

            game.update({
                'meta_score': game_info['meta_score'],
                'meta_reviews': game_info['meta_reviews'],
                'user_score': game_info['user_score'],
                'user_reviews': game_info['user_reviews'],
                'release_date': game_info['release_date'],
                'publisher': game_info['publisher'],
                'genre': game_info['genre']
            })

        else:
            game.update({
                'meta_score': 'N/A',
                'meta_reviews': 'N/A',
                'user_score': 'N/A',
                'user_reviews': 'N/A',
                'release_date': 'N/A',
                'publisher': 'N/A',
                'genre': 'N/A'
            })

    end_time = time.time()
    runtime_minutes = (end_time - start_time) / 60
    scrape_success_rate = total_game_info_scraped / len(catalogue)

    print(f'Statistics')
    print(f'Total game information retrieved: {total_game_info_scraped}')
    print(f'Scrape success rate: {scrape_success_rate * 100:.2f}%')
    print(f'Runtime: {runtime_minutes:.2f} minute\n')

    catalogue_df = pd.DataFrame(catalogue)
    catalogue_df.to_csv(f'{platform}_discount_catalogue_with_info_{today_date}.csv', index=False)


if __name__ == '__main__':
    main()
