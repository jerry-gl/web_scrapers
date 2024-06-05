"""
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
"""

import sys
import pandas as pd
import json
from datetime import date


def main():
    """
    Main function to convert SteamSpy CSV data to a discount catalogue JSON file.
    """
    # DD-MM-YYYY
    today_date = date.today().strftime("%d-%m-%Y")
    # specify the file name here.
    steamspy_csv = f'steamspy_deals_{today_date}.csv'
    create_discount_catalogue(steamspy_csv, today_date)
    print("Successfully converted steamspy deals from csv to json")


def create_discount_catalogue(steamspy: str, today_date):
    """
    Create a discount catalogue JSON file from the SteamSpy CSV file.
    """
    try:
        df = pd.read_csv(steamspy)
    except FileNotFoundError:
        print(f"Error: The file '{steamspy}' was not found.")
        sys.exit(1)

    catalogue = []

    for _, row in df.iterrows():
        title = row['Game']
        prices = (row['Price'].replace('$', '')
                  .replace('(', '')
                  .replace(')', '')
                  .split())
        special_price = float(prices[0])
        original_price = float(prices[1])

        catalogue.append({
            "title": title,
            "original_price": original_price,
            "special_price": special_price
        })

    output_file = f'steam_discount_catalogue_{today_date}.json'

    with open(output_file, 'w') as json_file:
        json.dump(catalogue, json_file, indent=4)


if __name__ == "__main__":
    main()
