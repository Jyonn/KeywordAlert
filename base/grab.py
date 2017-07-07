import hashlib
import json
import re
from urllib import request
from datetime import timedelta
import zlib
import datetime
from bs4 import BeautifulSoup
from News.models import News

def abstract_grab(url, phone_agent=False):
    """
    抽象抓取
    :param url: 网页链接
    :param phone_agent: 是否模拟手机
    :return: 网页内容
    """
    req = request.Request(url)

    req.add_header("Accept", "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8")
    req.add_header("Accept-Encoding", "gzip")
    req.add_header("Accept-Language", "zh-CN,zh;q=0.8")
    req.add_header("Cache-Control", "max-age=0")
    req.add_header("Connection", "keep-alive")
    if phone_agent:
        # 模拟手机User-Agent
        req.add_header("User-Agent",
                       "Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) "
                       "AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1")
    else:
        req.add_header("User-Agent",
                       "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) "
                       "Chrome/56.0.2924.87 Safari/537.36")

    res = request.urlopen(req)
    gzipped = res.headers.get('Content-Encoding')  # 判断是否压缩
    compressed_data = res.read()
    res.close()
    if gzipped:
        content = zlib.decompress(compressed_data, 16+zlib.MAX_WBITS)  # 解压
    else:
        content = compressed_data
    content = content.decode("utf-8")

    return content


def qdaily_grab():
    """
    好奇心日报抓取
    :return: 统一格式的新闻列表
    """
    url = 'http://m.qdaily.com/mobile/homes/articlemore/'+str(int(datetime.datetime.now().timestamp()))+'.json'
    try:
        content = json.loads(abstract_grab(url))
    except:
        return None
    if not content['status']:
        return None

    news_list = []
    for item in content['data']['feeds']:
        news_id = item['post']['id']
        publish_time = item['post']['publish_time']
        publish_time = datetime.datetime.strptime(publish_time, '%Y-%m-%d %H:%M:%S +0800')
        news_list.append(dict(
            id=news_id,
            title=item['post']['title'],
            url='http://m.qdaily.com/mobile/articles/'+str(news_id)+'.html',
            publish_time=publish_time,
        ))

    return news_list, News.SOURCE_QDAILY


def cnbeta_grab():
    """
    CNBETA新闻抓取
    :return: 统一格式的新闻列表
    """
    host = 'http://m.cnbeta.com'
    url = host + '/wap/index.htm?page=1'
    try:
        content = abstract_grab(url)
    except:
        return None
    news_regex = r'<div class="list"><a href="(.*?)">(.*?)</a>'
    news_contents = re.findall(news_regex, content, flags=0)

    news_list = []
    for item in news_contents:
        url = host + item[0]
        news_id = item[0][10:-4]
        try:
            content = abstract_grab(url)
        except:
            continue
        time_regex = '发布日期:(.*?)</span>'
        publish_time = re.search(time_regex, content, flags=0).group(1)
        publish_time = datetime.datetime.strptime(publish_time, '%Y-%m-%d %H:%M:%S')
        news_list.append(dict(
            id=news_id,
            title=item[1],
            url=url,
            publish_time=publish_time,
        ))

    return news_list, News.SOURCE_CNBETA


def techweb_grab():
    """
    TECHWEB新闻抓取
    :return: 统一格式的新闻列表
    """
    url = 'http://m.techweb.com.cn'
    try:
        content = abstract_grab(url)
    except:
        return None
    content_regex = '<ul id="allnews">(.*?)</ul>'
    content = re.search(content_regex, content, flags=re.S).group(1)
    news_regex = '<a href="(.*?)".*?<h2>(.*?)</h2>'
    news_contents = re.findall(news_regex, content, flags=re.S)

    news_list = []
    for item in news_contents:
        url = item[0]
        news_id = url[url.rfind('/')+1:url.rfind('.')]
        try:
            content = abstract_grab(url)
        except:
            continue
        time_regex = '<span id="pubtime_baidu">(.*?)</span>'
        publish_time = re.search(time_regex, content, flags=0).group(1)
        publish_time = datetime.datetime.strptime(publish_time, '%Y-%m-%d %H:%M:%S')
        news_list.append(dict(
            id=news_id,
            title=item[1],
            url=url,
            publish_time=publish_time,
        ))
    return news_list, News.SOURCE_TECHWEB


def sspai_grab():
    """
    少数派新闻抓取
    :return: 统一格式的新闻列表
    """
    url = 'https://sspai.com/api/v1/articles?offset=0&limit=20&type=recommend_to_home&sort=recommend_to_home_at'
    try:
        content = json.loads(abstract_grab(url))
    except:
        return None

    news_list = []
    for item in content['list']:
        news_id = item['id']
        publish_time = item['created_at']
        publish_time = datetime.datetime.fromtimestamp(publish_time)

        news_list.append(dict(
            id=news_id,
            title=item['title'],
            url='https://sspai.com/post/'+str(news_id),
            publish_time=publish_time,
        ))
    return news_list, News.SOURCE_SSPAI


def leiphone_grab():
    """
    雷锋网新闻抓取
    :return: 统一格式的新闻列表
    """
    url = 'https://m.leiphone.com/page/1'
    try:
        content = abstract_grab(url, phone_agent=True)
    except:
        return None

    host = 'https://m.leiphone.com/news/'
    news_regex = '<a href="'+host+'(.*?)">.*?<div class="tit">(.*?)</div>.*?</li>'
    news_contents = re.findall(news_regex, content, flags=re.S)

    news_list = []
    for item in news_contents:
        url = host + item[0]
        news_id = item[0][7:-5]
        try:
            content = abstract_grab(url)
        except:
            continue
        time_regex = '<meta property="article:published_time" content="(.*?)\+08:00"/>'
        try:
            publish_time = re.search(time_regex, content, flags=0).group(1)
            publish_time = datetime.datetime.strptime(publish_time, '%Y-%m-%dT%H:%M:%S')
        except:
            publish_time = datetime.datetime.now()
        news_list.append(dict(
            id=news_id,
            title=item[1],
            url=url,
            publish_time=publish_time,
        ))
    return news_list, News.SOURCE_LEIPHONE


def dgtle_grab():
    """
    数字尾巴新闻抓取
    :return: 统一格式的新闻列表
    """
    url = 'http://www.dgtle.com/'
    try:
        content = abstract_grab(url, phone_agent=True)
    except:
        return None
    soup = BeautifulSoup(content, 'html.parser')
    newses = soup.find(class_='cr180article_list')
    news_list = []
    publish_time = datetime.datetime.now()
    for news in newses('dl'):
        href = news.find(class_='zjj_title')
        title = href('a')[0].get_text()
        news_id = href('a')[0].get('href')
        news_url = url + news_id
        news_id = news_id[news_id.find('-')+1:news_id.rfind('-')]
        news_list.append(dict(
            id=news_id,
            title=title,
            url=news_url,
            publish_time=publish_time,
        ))
    return news_list, News.SOURCE_DGTLE


def ithome_grab():
    try:
        content = abstract_grab('https://www.ithome.com')
    except:
        return None
    soup = BeautifulSoup(content, 'html.parser')
    newses = soup.find(class_='new-list-1')
    news_list = []
    for news in newses.findAll(class_='title'):
        news = news.find('a')
        news_url = news.get('href')
        title = news.get_text()
        news_id = news_url[news_url.rfind('/') + 1:news_url.rfind('.')]
        try:
            content = abstract_grab(news_url)
        except:
            continue
        time_regex = '<span id="pubtime_baidu">(.*?)</span>'
        publish_time = re.search(time_regex, content, flags=0).group(1)
        publish_time = datetime.datetime.strptime(publish_time, '%Y-%m-%d %H:%M:%S')
        news_list.append(dict(
            id=news_id,
            title=title,
            url=news_url,
            publish_time=publish_time,
        ))
    return news_list, News.SOURCE_ITHOME


def kr_grab():
    try:
        content = abstract_grab('http://36kr.com/')
    except:
        return None
    content_regex = 'var props=(.*?),locationnal'
    content = re.search(content_regex, content, flags=0).group(1)
    newses = json.loads(content)['feedPostsLatest|post']
    news_list = []
    for news in newses:
        news_list.append(dict(
            id=news['id'],
            title=news['title'],
            url='http://36kr.com/p/'+str(news['id'])+'.html',
            publish_time=datetime.datetime.strptime(news['published_at'], '%Y-%m-%d %H:%M:%S')
        ))
    return news_list, News.SOURCE_KR36


def ninetofivemac_grab():
    items = []
    try:
        html = abstract_grab('https://9to5mac.com/')
    except:
        return None
    soup = BeautifulSoup(html, 'lxml')
    news_list = soup.find_all('article')

    for news in news_list:
        item = {}
        try:
            item['title'] = news.find('a').text.strip()

            date = news.find('p', attrs={'class': 'time-twitter'}).text.replace('.','').strip().split(' ')
            date[2] = re.sub("\D", "", date[2])
            date = date[1] + '-' + date[2] + '-' + date[3] + '-' + date[4] + '-' + date[5] + '-' + '01'
            CTS = datetime.datetime.strptime(date, '%b-%d-%Y-%I:%M-%p-%S')
            PTS = CTS + timedelta(hours=15)
            item['publish_time'] = PTS

            item['url'] = news.find('a')['href'].strip()
            item['id'] = hashlib.md5(item['title'].encode('utf-8')).hexdigest()[8:-8]
            items.append(item)

        except:
            pass

    return items, News.SOURCE_9TO5MAC

def ninetofivegoogle_grab():
    items = []
    try:
        html = abstract_grab('https://9to5google.com/')
    except:
        return None
    soup = BeautifulSoup(html, 'lxml')
    news_list = soup.find_all('article')

    for news in news_list:
        item = {}
        try:
            item['title'] = news.find('a').text.strip()

            date = news.find('p', attrs={'class': 'time-twitter'}).text.replace('.','').strip().split(' ')
            date[2] = re.sub("\D", "", date[2])
            date = date[1] + '-' + date[2] + '-' + date[3] + '-' + date[4] + '-' + date[5] + '-' + '01'
            CTS = datetime.datetime.strptime(date, '%b-%d-%Y-%I:%M-%p-%S')
            PTS = CTS + timedelta(hours=15)
            item['publish_time'] = PTS

            item['url'] = news.find('a')['href'].strip()
            item['id'] = hashlib.md5(item['title'].encode('utf-8')).hexdigest()[8:-8]
            items.append(item)

        except:
            pass

    return items, News.SOURCE_9TO5GOOGLE

def solidot_grab():
    items = []
    try:
        html = abstract_grab('http://www.solidot.org/')
    except:
        return None
    soup = BeautifulSoup(html, 'lxml')
    news_list = soup.find_all('div', attrs={'class': 'block_m'})

    for news in news_list:
        item = {}
        item['title'] = news.find_all('a')[0].text + ':' + news.find_all('a')[1].text
        item['url'] = 'http://www.solidot.org' + news.find_all('a')[1].get('href')
        time = news.find('div', attrs={'class': 'talk_time'}).\
            text.strip().split('pigsrollaroundinthem(39396)\r\n                \n\r\n            发表于')[1].split(' ')[:2]
        time = re.sub("\D", "", time[0]) + re.sub("\D", "", time[1]) + '01'
        item['publish_time'] = datetime.datetime.strptime(time, '%Y%m%d%H%M%S')
        item['id'] = time = re.sub("\D", "", item['url'])
        items.append(item)

    return items, News.SOURCE_SOLIDOT

def engadgetcn_grab():
    items = []
    try:
        html = abstract_grab('http://cn.engadget.com/')
    except:
        return None
    soup = BeautifulSoup(html, 'lxml')
    news_list = soup.find_all('article', attrs={'class': 'o-hit'})

    for news in news_list:
        try:
            item = {}
            item['title'] = news.find('span').text.strip()
            item['url'] = 'http://cn.engadget.com' + news.find('a', attrs={'class': 'o-hit__link'}).get('href')
            time = news.find('span', {'class': ' hide@tp mDC'}).text.strip()
            if re.match('\d+ 小时前', time):
                time = int(re.sub("\D", "", time))
                item['publish_time'] = datetime.datetime.now() - timedelta(hours=time)
            elif re.match('\d+ 分钟前', time):
                time = int(re.sub("\D", "", time))
                item['publish_time'] = datetime.datetime.now() - timedelta(minutes=time)
            else:
                item['publish_time'] = datetime.datetime.now() - timedelta(days=1)
            item['id'] = hashlib.md5(item['title'].encode('utf-8')).hexdigest()[8:-8]

            items.append(item)
        except:
            pass
    return items, News.SOURCE_ENGADGETCN

def engadgeten_grab():
    items = []
    try:
        html = abstract_grab('http://www.engadget.com/')
    except:
        return None
    soup = BeautifulSoup(html, 'lxml')
    news_list = soup.find_all('article', attrs={'class': 'o-hit'})

    for news in news_list:
        try:
            item = {}
            item['title'] = news.find('span').text.strip()
            item['url'] = 'http://www.engadget.com' + news.find('a', attrs={'class': 'o-hit__link'}).get('href')
            time = news.find('span', attrs={'class': ' hide@tp'}).text.strip()
            if re.match('\d+h ago', time):
                time = int(re.sub("\D", "", time))
                item['publish_time'] = datetime.datetime.now() - timedelta(hours=time)
            elif re.match('\d+m ago', time):
                time = int(re.sub("\D", "", time))
                item['publish_time'] = datetime.datetime.now() - timedelta(minutes=time)
            else:
                item['publish_time'] = datetime.datetime.now() - timedelta(days=1)
            item['id'] = hashlib.md5(item['title'].encode('utf-8')).hexdigest()[8:-8]

            items.append(item)
        except:
            pass

    return items, News.SOURCE_ENGADGETEN