import feedparser
import requests
import param

def crawling():
    # contents
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750",
        'Content-Type': 'application/json', "Cookie": ""}
    response = requests.get(param.url, headers=headers)
    with open('rssList.xml', 'wb') as file:
        file.write(response.content)
    feed = feedparser.parse('rssList.xml')
    print(feed['entries'][0]['title'])

crawling()