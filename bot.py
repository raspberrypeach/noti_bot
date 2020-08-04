#http://ice.yu.ac.kr/user/indexSub.action?codyMenuSeq=2297360&siteId=ice&menuType=T&uId=6&sortChar=A&linkUrl=6_1.html&mainFrame=right
#http://ice.yu.ac.kr/user/boardList.action?command=view&page=1&boardId=2559927&boardSeq=24078418

from urllib.request import urlopen
import bs4
url = urlopen("http://ice.yu.ac.kr/user/indexSub.action?codyMenuSeq=2297360&siteId=ice&menuType=T&uId=6&sortChar=A&linkUrl=6_1.html&mainFrame=right")
bsobj = bs4.BeautifulSoup(url, "url.parser")

print(bsobj.head.title)