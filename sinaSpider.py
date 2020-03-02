import requests
from pyquery import PyQuery as pq 
from urllib.parse import urlencode
#https://m.weibo.cn/search?containerid=231522type=1&q=#地震快讯#&sudaref=login.sina.com.cn&display=0&retcode=6102
#https://m.weibo.cn/api/container/getIndex?containerid=231522type=1&q=#地震快讯#&sudaref=login.sina.com.cn&display=0&retcode=6102&page_type=searchall&page=3
host = 'm.weibo.cn'
base_url = 'https://%s/api/container/getIndex?' % host
user_agent = 'User-Agent: Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1 wechatdevtools/0.7.0 MicroMessenger/6.3.9 Language/zh_CN webview/0'
headers = {
    'Host': host,
    'Referer': 'https://m.weibo.cn/search?containerid=231522type%3D1%26q%3D%23%E5%9C%B0%E9%9C%87%E5%BF%AB%E8%AE%AF%23&sudaref=login.sina.com.cn&display=0&retcode=6102',
    'User-Agent': user_agent
}

def getSinglePage():
	# 参数
	params = {
		'containerid':'231522type=1&t=10&q=#地震快讯#',
		'isnewpage':1,
		'luicode':'10000011',
		'lfid':'231522type=1&q=#地震快讯#',
		'sudaref':'login.sina.com.cn',
		'display':0,
		'retcode':6102,
		'page_type':'searchall'
	}
	# 抓取热点页震情信息
	url = base_url + urlencode(params)
	try:
		response = requests.get(url,headers=headers)	
		if response.status_code==200:
			return response.json()
	except requests.ConnectionError as e :
		print('抓取错误',e.args)
#数据解析JSON格式
def parsePage(json):
	data = json.get('data')
	cards = data.get('cards')	
	for item in cards:
		mblog = item.get('mblog')
		if mblog:
			data={
				'id':mblog.get('id'),
				'text': mblog.get('text'),
				'attitudes': mblog.get('attitudes_count'),
                'comments': mblog.get('comments_count'),
                'reposts': mblog.get('reposts_count')
            }
			yield data

if __name__=='__main__':
	json = getSinglePage()
	results = parsePage(json)
	for result in results:
		#中国地震台网正式测定：02月18日17时07分在山东济南市长清区（北纬36.47度，东经116.64度）发生4.1级地震，震源深度10千米。（ <a href=\'/n/中国地震台网\'>@中国地震台网</a> ）
		print(result)