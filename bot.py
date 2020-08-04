import feedparser

url = "http://ice.yu.ac.kr/rssList.jsp?siteId=ice&boardId=2559927"
feed = feedparser.parse(url)
print(len(feed['entries']))
print(feed['entries'][0]['published'])