import pyexcel_xls, random, re, os
import numpy as np
from tqdm import tqdm
from collections import OrderedDict

data_save = []
data_save.append(['名称', '作品数量', '平均分', '最高分', '最高分作品', '最低分', '最低分作品', '评分波动', 
	'0-4', '4-6', '6-8', '8-10', '0-4占比', '4-6占比', '6-8占比', '8-10占比'])

path = "datas/"
files = []
for dirpath, dirnames, filenames in os.walk(path):
    for filepath in filenames:
        files = filenames

for file in tqdm(files):
	data = pyexcel_xls.get_data(path+file)['actorMovies']
	movie_name = []
	movie_rating = []
	for row in range(1, len(data)):
		if (len(data[row])>3):
			name = data[row][0]
			genres = data[row][1]
			rating = data[row][3]
			if ('真人秀' not in genres) and ('脱口秀' not in genres) and ('歌舞' not in genres) and ('纪录片' not in genres) and ('短片' not in genres) and (data[row][3] != '/'):
				movie_name.append(data[row][0])
				movie_rating.append(eval(data[row][3]))

	a = np.array(movie_rating)
	value_count = len(a)
	print('\n',file, value_count)
	value_mean = np.mean(a)
	value_max = np.max(a)
	name_max = movie_name[movie_rating.index(value_max)]
	value_min = np.min(a)
	name_min = movie_name[movie_rating.index(value_min)]
	value_var = np.var(a)

	dist = [0, 0, 0, 0]
	for rating in movie_rating:
		if (rating<4):
			dist[0] += 1
		elif (rating<6):
			dist[1] += 1
		elif (rating<8):
			dist[2] += 1
		else:
			dist[3] += 1

	distp = []
	for d in dist:
		distp.append(str(d/value_count*100)+'%')
	'''
	print('\n名称\t', file,
		'\n作品数量\t', value_count, 
		'\n平均分\t', value_mean, 
		'\n最高分\t', name_max, value_max, 
		'\n最低分\t', name_min, value_min, 
		'\n方差\t', value_var,
		'\n分布\t', distp)
	'''

	data_save.append([file, str(value_count), str(value_mean), str(value_max), name_max, str(value_min), name_min, str(value_var),
		str(dist[0]), str(dist[1]), str(dist[2]), str(dist[3]), str(distp[0]), str(distp[1]), str(distp[2]), str(distp[3])])

data_summary = OrderedDict()
data_summary.update({'actorRating': data_save})
pyexcel_xls.save_data('dataRating.xls', data_summary)

