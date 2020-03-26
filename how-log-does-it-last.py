#!/usr/bin/env python

""" 
Lookup expiration dates for unlabeled foods

Relies on set regex pattern to find table in html pages

Powered by 
===========
"www.eatbydate.com"
"google.com" 
"""
import requests
import re
import sys

import pandas

try: 
    from googlesearch import search 
except ImportError:  
    print("No module named 'google' found") 

SOURCE_SITE = "www.eatbydate.com"
TABLE_REGEX_PATTERN = '<table id="unopened">(.|\n)*?</table>'

def get_page_url(food, site):     
    # to search 
    query = f"site:{site} how long do {food} last"
      
    result = None
    url = None

    for result in search(query, tld="com", num=1, stop=1, pause=2): 
        url = result

    return url

def get_page_html(url):
    response = requests.get(url)
    html = response.text
    
    if not (response.status_code == 200 and re.search('Error 404', html) == None):
        html = None
    
    return html

def extract_html_table(html, regex_pattern):
    table_html_matches = re.search(regex_pattern, html)

    try:
        table_html = table_html_matches[0]
    except TypeError:
        table_html = None
    pass

    return table_html

def pretty_print_table_html(table_html):
    table = pandas.read_html(table_html)
    print(table[0])

def main(food):  
    print(f"Looking up: '{food}' ...")

    url = get_page_url(food, SOURCE_SITE)
    if url == None:
        print(f"error! no result found for '{food}'")
        exit(1)
    print(f"url: {url}")
    
    html = get_page_html(url)
    if html == None:
        print(f"error! page lookup failed for '{food}'")
        exit(1)
        
    table_html = extract_html_table(html, TABLE_REGEX_PATTERN)
    if table_html == None:
        print(f"error! table not found for '{food}'")
        exit(1)

    pretty_print_table_html(table_html)

if __name__ == '__main__':
    food = sys.argv[1]
    main(food)