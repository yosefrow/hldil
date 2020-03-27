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

SOURCE_SITE = "www.eatbydate.com"
TABLE_REGEX_PATTERN = '<table id="unopened">(.|\n)*?</table>'
#P_REGEX_PATTERN = '^<h3>.*What is the best way to store.*</h3>$[\n|.]*?<h3>'
P_REGEX_PATTERN = '<h3>.*What is the best way to store.*(\n|.)*?<h3>'

def get_page_url(food, site):     
    # to search 
    query = f"site:{site} {food} \"storage\""
      
    result = None
    url = None

    for result in search(query, tld="com", num=1, stop=1, pause=2): 
        url = result

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
    pass

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
        print(f"\nerror! no result found for '{food}'\n")
        exit(1)
    print(f"url: {url}")
    
    html = get_page_html(url)
    if html == None:
        print(f"\nerror! page lookup failed for '{food}'\n")
        exit(1)
        
    table_html = get_first_match(html, TABLE_REGEX_PATTERN)
    if table_html == None:
        print(f"\nwarning! table not found for '{food}'\n")
        p_html = get_first_match(html, P_REGEX_PATTERN)
        
        if p_html == None:
            print(f"\nerror! expiry info not found for '{food}'\n")
            exit(1)
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
        
        print(food)
    except:
        print(f"error! You must provide a food to lookup as an argument. e.g: {script_path} my-favorite-food")
        exit(1)
    pass

    main(food)