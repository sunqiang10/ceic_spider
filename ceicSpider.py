import requests
from pyquery import PyQuery as pq 
from urllib.parse import urlencode
import time
class Ceic(object):
	host = 'news.ceic.ac.cn'
	tt = int(time.time())
	base_url = 'http://news.ceic.ac.cn/index.html?time=' + str(tt)
	user_agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3741.400 QQBrowser/10.5.3863.400'
	headers = {
	    'Host': host,
	    'Referer': 'http://news.ceic.ac.cn/index.html?time=' + str(tt),
	    'User-Agent': user_agent
	}

	def getSinglePage():
		url = base_url
		try:
			response = requests.get(url,headers=headers)
			response.encoding = "utf-8"
			html = response.text		
			data = pq(html)

			# 获取结果集 HTML格式
			items = data('table tr').items()     
			for item in items:
				txt = item('td').items()
				data={
					'lv':item('td').eq(0).text(),
					'dt':item('td').eq(1).text(),
					'lat':item('td').eq(2).text(),
					'lon':item('td').eq(3).text(),
					'depth':item('td').eq(4).text(),
					'addr':item('td').eq(5).text()
	            }
				yield data
		except requests.ConnectionError as e :
			print('抓取错误',e.args)

if __name__=='__main__':
	results = getSinglePage()
	for result in results:
		#中国地震台网正式测定：02月18日17时07分在山东济南市长清区（北纬36.47度，东经116.64度）发生4.1级地震，震源深度10千米。（ <a href=\'/n/中国地震台网\'>@中国地震台网</a> ）
		print(result)