import bs4, requests

# 从百度搜索风云榜获取热门演员列表

# 链接和请求头
url = 'http://top.baidu.com/buzz'
headers = {
	'Host': 'top.baidu.com',
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0',
	'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
	'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
	'Accept-Encoding': 'gzip, deflate'}

# 男演员列表
r = requests.get(url, headers=headers, params={'b': 17}, timeout=10)
r.encoding = 'gbk'
soup = bs4.BeautifulSoup(r.text, features='lxml')
actor_list = soup.find_all(class_='list-title')
for actor in actor_list:
	print(actor.text)

# 女演员列表
r = requests.get(url, headers=headers, params={'b': 18}, timeout=10)
r.encoding = 'gbk'
soup = bs4.BeautifulSoup(r.text, features='lxml')
actor_list = soup.find_all(class_='list-title')
for actor in actor_list:
	print(actor.text)


