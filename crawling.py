import feedparser
import requests
url = 'http://ice.yu.ac.kr/rssList.jsp?siteId=ice&boardId=2559927'

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750",
            'Content-Type': 'application/json', "Cookie": ""}
response = requests.get(url, headers=headers)
print(response.content)
with open('rssList.xml', 'wb') as file:
    file.write(response.content)


feed = feedparser.parse('rssList.xml')
url2 = 'http://ice.yu.ac.kr/rssList.jsp?siteId=ice&boardId=2559904'
#feed = feedparser.parse(url)

print(feed['entries'][0]['published'])
print(feed['entries'][0]['title'])
print(feed['entries'][0]['link'])
