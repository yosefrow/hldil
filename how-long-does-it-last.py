#!/usr/bin/env python

""" 
Lookup expiration dates for unlabeled foods

Relies on set regex pattern to find table in html pages

Powered by 
===========
"www.eatbydate.com"
"google.com" 
"""
import re
import sys

import requests
import pandas
from googlesearch import search 

from urllib.error import HTTPError

SOURCE_SITE = "www.eatbydate.com"
TABLE_REGEX_PATTERN = '<table id="unopened">(.|\n)*?</table>'
P_REGEX_PATTERN = '<h3>.*What is the best way to store.*(\n|.)*?<h3>'

color_codes = {
    'HEADER': '\033[95m',
    'BOKBLUE': '\033[94m',
    'OKGREEN': '\033[92m',
    'WARNING': '\033[93m',
    'FAIL': '\033[91m',
    'ENDC': '\033[0m',
    'BOLD': '\033[1m',
    'UNDERLINE': '\033[4m'
}

def color_print(color_name, message):
    color = color_codes[color_name]
    end_color = color_codes['ENDC']
    print(f'{color}{message}{end_color}')

def abort(message):
    color_print('FAIL', f'\nCritical error: {message}\n')
    exit(1)
    
def warn(message):
    color_print('WARNING', f'\nWarning: {message}\n')

def success(message):
    color_print('OKGREEN', message)

def get_page_url(food, site):     
    # to search 
    query = f"site:{site} {food} \"storage\""
      
    result = None
    url = None

    try:
        for result in search(query, tld="com", num=1, stop=1, pause=2): 
            url = result
    except HTTPError as err:
        print(
            f'Google Search encountered an error\n' +
            f'Code: {err.code} - {err.reason}\n' +
            f'You can visit the url manually: {err.url}\n' 
        )
        
        if err.code == 429:
            print(
                'You are probably being rate-limited by Google.\n' +
                'Try waiting before using the program again and reduce the rate at which you make requests.'
            )
        else:
            raise
    return url

def get_page_html(url):
    response = requests.get(url)
    html = response.text
    
    # sometimes a web page can respond with 200 but actually be a 404 page in content
    if not (response.status_code == 200 and re.search('Error 404', html) == None):
        html = None
    
    return html

def get_first_match(source, pattern):
    matches = re.search(pattern, source)

    try:
        result = matches[0]
    except TypeError:
        result = None

    return result

def pretty_print_table_html(table_html):
    table = pandas.read_html(table_html)
    print(table[0])

def strip_html_tags(html_string):
    pattern = '<[^><]*?>'
    
    text_string = re.sub(pattern, '', html_string)
    return text_string

def html_string_to_text(html_string):
    import html
    html_string = html.unescape(html_string)
    text_string = strip_html_tags(html_string)

    return text_string

def main(food):  
    print(f"Looking up: '{food}' ...")

    url = get_page_url(food, SOURCE_SITE)
    if url == None:
        abort(f"no page url found for '{food}'\n")
    
    success(f"Found url: {url}")
    
    html = get_page_html(url)
    if html == None:
        abort(f"no page html found for '{food}'\n")
        
    table_html = get_first_match(html, TABLE_REGEX_PATTERN)
    if table_html == None:
        warn(f"no table found for '{food}'\n")
        p_html = get_first_match(html, P_REGEX_PATTERN)
        
        if p_html == None:
            abort(f"no expiration info found for '{food}'")
        else:
            p_text = html_string_to_text(p_html)
            print(p_text)
    else:
        pretty_print_table_html(table_html)
    
if __name__ == '__main__':
    script_path = sys.argv[0]
    
    try:
        args = sys.argv[1:]
        seperator = ' '
        food = seperator.join(args)
    except:
        abort(f"Missing argument: 'food'. e.g: {script_path} food")

    main(food)
