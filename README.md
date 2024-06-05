# Web Scrapers [Demo](https://vimeo.com/953614329?share=copy)
The three Python files in this repository are designed to work together to retrieve games currently on discount on Nintendo and Steam platforms, along with additional information from Metacritic.  
![sample_output](/screenshots/sample_output.JPG)
![sample_price](/screenshots/sample_price.JPG)
![sample_score](/screenshots/sample_score.JPG)

## Nintendo Scraper: *nintendo_scraper.py*  
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

## Steamspy converter: *steamspy_deals_csv_to_json.py*
Converts Steam's discount games, provided by Steamspy, from csv into json.

This script transforms the current offers from Steam provided by Steamspy
and saves the following information into a JSON file:
- title
- original price ($USD)
- special price ($USD)

Usage:
Begin by downloading the csv file from https://steamspy.com/deal/.
Rename the downloaded csv file as "steamspy_deals_" followed by today's date (DD-MM-YYYY).
Run this script directly to convert the csv file into json file.

Dependencies:
- sys
- pandas
- json
- datetime

Example:
$ python steamspy_deals_csv_to_json.py

## Metacritic Scraper: *metacritic_scraper.py*  
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
- Make sure the json file is named f'{platform}\_discount_catalogue_{today_date}.json'  
- Run this script directly to scrape the game's information from Metacritic.


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