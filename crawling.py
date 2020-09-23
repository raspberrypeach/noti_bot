import feedparser
import requests
import param

def crawling(type = None):
    # contents
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750",
        'Content-Type': 'application/json', "Cookie": ""}
    if type == 'jobs':
        response = requests.get(param.url2, headers=headers)
        with open('JrssList.xml', 'wb') as file:
            file.write(response.content)
    else:
        response = requests.get(param.url, headers=headers)
        with open('rssList.xml', 'wb') as file:
            file.write(response.content)

    feed = feedparser.parse('rssList.xml')
    #print(feed['entries'][0]['title'])

crawling()