# produce=carrots; url_prefix=www.eatbydate.com/vegetables/fresh-vegetables; curl -s "${url_prefix}/how-long-do-${produce}-last-shelf-life//" | grep '<table id="unopened">.*</table>'
print('hello friends')

import requests
import re

produce = "carrots"
produce = produce.replace(' ', '-').lower()

print(produce)

url_prefix = "https://www.eatbydate.com/vegetables/fresh-vegetables"
urls = [
    f"{url_prefix}/how-long-do-{produce}-last-shelf-life/",
    f"{url_prefix}/{produce}-shelf-life-expiration-date/"
]

for url in urls:
    response = requests.get(url)
    content = str(response.content)

    if response.status_code == 200:
        if re.search('Error 404', content) == None:
            break

print(url)

pattern = '<table id="unopened">.*?</table>'
extract = re.search(pattern, content)

try:
    print(extract[0])
except TypeError:
    print("warn: no matches found")
    pass
