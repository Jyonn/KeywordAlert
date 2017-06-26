import datetime
import time

from Config.models import Config
from News.models import News, Keyword, Log
from admin.models import Admin
from base.decorator import require_post, require_json, require_params
from base.grab import qdaily_grab, cnbeta_grab, techweb_grab, leiphone_grab, sspai_grab
from base.response import response
from cp_hint.settings import QDAILY_SIGNAL, QDAILY_INTERVAL, CNBETA_SIGNAL, CNBETA_INTERVAL, TECHWEB_SIGNAL, \
    TECHWEB_INTERVAL, \
    SSPAI_SIGNAL, SSPAI_INTERVAL, LEIPHONE_SIGNAL, LEIPHONE_INTERVAL


def init(request):
    """
    初始化网站数据
    """
    Config.create(QDAILY_SIGNAL, '0')  # 好奇心日报上次抓取时间
    Config.create(QDAILY_INTERVAL, '20')  # 好奇心日报抓取时间间隔
    Config.create(CNBETA_SIGNAL, '0')  # CNBETA上次抓取时间
    Config.create(CNBETA_INTERVAL, '20')  # CNBETA抓取时间间隔
    Config.create(TECHWEB_SIGNAL, '0')  # TECHWEB上次抓取时间
    Config.create(TECHWEB_INTERVAL, '20')  # TECHWEB抓取时间间隔
    Config.create(SSPAI_SIGNAL, '0')  # 少数派上次抓取时间
    Config.create(SSPAI_INTERVAL, '20')  # 少数派抓取时间间隔
    Config.create(LEIPHONE_SIGNAL, '0')  # 雷锋网上次抓取时间
    Config.create(LEIPHONE_INTERVAL, '20')  # 雷锋网抓取时间间隔
    Config.create('lasting', '10')  # 默认新闻频率统计范围
    Config.create('interval', '10')  # 默认统计数据时间间隔
    Config.create('analyse-signal', '0')  # 默认统计数据时间
    Admin.create('cp', 'Chaping321')
    return response()


def news_dealer(request):
    """
    网站统一抓取 10s访问一次
    """
    funcs = [qdaily_grab, cnbeta_grab, techweb_grab, sspai_grab, leiphone_grab]
    for func in funcs:
        ret = func()  # 执行抓取
        if ret is None:
            continue
        news_list, signal, source = ret
        for news in news_list:  # 存储到数据库
            News.create(news, source)
        Config.create(signal, str(int(datetime.datetime.now().timestamp())))  # 更新上次抓取时间


def analyse(request):
    interval = int(Config.objects.get(key='interval').value)
    o_last = Config.objects.get(key='analyse-signal')
    last_time = int(o_last.value)
    crt_time = datetime.datetime.now()
    if int(crt_time.timestamp()) - last_time < int(interval) * 60:
        return response()

    keywords = Keyword.objects.filter(disable=False)
    lasting = int(Config.objects.get(key='lasting').value)
    lasting = datetime.timedelta(minutes=lasting)
    begin_time = crt_time - lasting
    newses = News.objects.filter(publish_time__gte=begin_time)
    print(len(newses), begin_time)
    for o_keyword in keywords:
        kw = o_keyword.kw
        count = 0
        web_list = []
        for news in newses:
            if news.title.find(kw) != -1:
                count += 1
                if news.source not in web_list:
                    web_list.append(news.source)
        print(kw, count, len(web_list))
        if count > o_keyword.count and len(web_list) > o_keyword.web_count:
            Log.create(kw, count, len(web_list))

    o_last.value = str(int(crt_time.timestamp()))
    o_last.save()


@require_post
@require_json
@require_params(['last_id'])
def refresh_hot(request):
    last_id = int(request.POST['last_id'])
    if last_id == -1:
        return response(body=dict(logs=[], last_id=Log.objects.all().order_by('-pk')[0].pk))
    logs = Log.objects.filter(pk__gt=last_id)
    log_list = []
    latest = last_id
    # latest = 0
    for log in logs:
        log_list.append(dict(
            kw=log.kw,
            count=log.count,
            web_count=log.web_count,
        ))
        if latest < log.pk:
            latest = log.pk
    return response(body=dict(logs=log_list, last_id=latest))
