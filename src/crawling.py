
import feedparser
import wget

feed = feedparser.parse(url)
url2 = 'http://ice.yu.ac.kr/rssList.jsp?siteId=ice&boardId=2559904'
feed = feedparser.parse(url)
#feed = feedparser.parse('./rssList.xml')
#wget.download(url2)

print(feed['entries'][0]['published'])
print(feed['entries'][0]['title'])
print(feed['entries'][0]['link'])
