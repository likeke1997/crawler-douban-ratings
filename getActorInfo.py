# -*- coding: utf-8 -*-

import bs4, pyexcel_xls, random, re, requests, time
from tqdm import tqdm
from collections import OrderedDict

data_save = OrderedDict()
actor_name = []
actor_id = []
actor_movie_count = []

headers = { # 请求头
	'Host': 'movie.douban.com', 
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0',
	'Accept': '*/*',
	'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
	'Accept-Encoding': 'gzip, deflate, br',
	'Referer': 'https://movie.douban.com/',
	'DNT': '1',
	'Connection': 'close'}

def get_actor_name():
	data_source = pyexcel_xls.get_data('dataSource.xls')['actorList']
	for row in tqdm(range(1, len(data_source))):
		actor_name.append(data_source[row][0])
	print(actor_name)

def get_actor_id():
	url = 'https://movie.douban.com/j/subject_suggest'
	for name in tqdm(actor_name):
		sleep_momment()
		params = {'q': name}
		r = requests.get(url, params=params, headers=headers, timeout=2)
		for j in r.json():
			if j['type'] == 'celebrity':
				actor_id.append(j['id'])
				break
	print(actor_id)

def save_actor_id():
	datas = []
	datas.append(['index', 'name', 'id'])
	for i in range(len(actor_name)):
		datas.append([str(i+1), actor_name[i], actor_id[i]])
	data_save.update({'actorId': datas})	

def get_actor_movie_count():
	for id_ in actor_id:
		sleep_momment()
		url = 'https://movie.douban.com/celebrity/' + id_ + '/movies'
		params = {'sortby': 'time', 'start': '0', 'format': 'text', 'role': 'A1'}
		r = requests.get(url, params=params, headers=headers, timeout=2)
		soup = bs4.BeautifulSoup(r.text, features='lxml')
		tag_count = soup.find('h1')
		text_count = re.search(r'(作品)\s*\（(\S*)\）', tag_count.text).group(2)
		actor_movie_count.append(int(text_count))
	print(actor_movie_count)

def save_actor_movie_count():
	datas = []
	datas.append(['index', 'name', 'id', 'movieCount'])
	for i in range(len(actor_name)):
		datas.append([str(i+1), actor_name[i], actor_id[i], actor_movie_count[i]])
	data_save.update({'actorMovieCount': datas})	

def get_actor_movie_info():
	index = 0
	for id_ in actor_id:
		if (index>=0):
			print(index, '\t', id_, '\t', actor_name[index])
			sleep_momment(2, 3)
			url = 'https://movie.douban.com/celebrity/' + id_ + '/movies'
			pages = actor_movie_count[index] // 25 + 1
			movie_href = []
			for page in range(pages):
				sleep_momment(2, 3)
				params = {'sortby': 'time', 'start': str(page*25), 'format': 'text', 'role': 'A1'}
				r = requests.get(url, params=params, headers=headers, timeout=5)
				r.encoding = 'UTF-8'
				soup = bs4.BeautifulSoup(r.text, features='lxml')
				tag_movie = soup.find_all(headers='m_name')
				for tag in tag_movie:
					text_href = tag.a['href']
					id_href = re.search(r'(subject/)(\d*)/', text_href).group(2)
					movie_href.append('https://movie.douban.com/subject/'+id_href)
			movie_data = []
			movie_data.append(['title', 'genres', 'year', 'rating'])
			for href in tqdm(movie_href):
				sleep_momment()
				url = href
				r = requests.get(url, params=params, headers=headers)
				soup = bs4.BeautifulSoup(r.text, features='lxml')
				tag_title = soup.find(property='v:itemreviewed')
				tag_genres = soup.find_all(property='v:genre')
				tag_year = soup.find(class_='year')
				tag_rating = soup.find(property='v:average')
				try:
					text_title = tag_title.text
					text_genres = []
					for genres in tag_genres:
						text_genres.append(genres.text)
					text_year = tag_year.text
					text_rating = tag_rating.text
				except:
					text_title = '/'
					text_genres = ['/']
					text_year = '/'
					text_rating = '/'
					print('\n', id_, href, '爬取失败!')
				movie_data.append([text_title, ','.join(text_genres), text_year, text_rating])
			movie_save = OrderedDict()
			movie_save.update({'actorMovies': movie_data})
			pyexcel_xls.save_data('datas/'+id_+' '+actor_name[actor_id.index(id_)]+'.xls', movie_save)				
		index += 1

def save_all_data():
	pyexcel_xls.save_data('dataSummary.xls', data_save)	

def sleep_momment(time_a=0.1, time_b=0.2):
	time.sleep(random.uniform(time_a, time_b))

if __name__ == '__main__':
	get_actor_name()
	get_actor_id()
	save_actor_id()
	get_actor_movie_count()
	save_actor_movie_count()
	get_actor_movie_info()