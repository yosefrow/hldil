#!/usr/bin/env python
""" 
Lookup expiration dates for common unlabeled foods
"""
import requests
import re
import sys

import pandas

def main(produce):  
    print(f"Looking up: {produce}")
    
    try: 
        from googlesearch import search 
    except ImportError:  
        print("No module named 'google' found") 
      
    # to search 
    site = "www.eatbydate.com"
    query = f"site:{site} how long do {produce} last"
      
    result = None
    url = None

    for result in search(query, tld="com", num=1, stop=1, pause=2): 
        url = result

    if url == None:
        print(f"error! no result found for: {produce}")
        exit(1)
    
    response = requests.get(url)
    text = response.text
    
    if not (response.status_code == 200 and re.search('Error 404', text) == None):
        print ('error! page lookup failed!')
        exit(1)
    
    print(url)
    
    table_html_pattern = '<table id="unopened">(.|\n)*?</table>' #'<table id="unopened">'
    table_html_matches = re.search(table_html_pattern, text)

    try:
        table_html_string = table_html_matches[0]
    except TypeError:
        print("warn: no matches found")
        exit(1)
    pass

    #print(table_html_string)

    table = pandas.read_html(table_html_string)
    print(table)

if __name__ == '__main__':
    produce = sys.argv[1]
    main(produce)
    