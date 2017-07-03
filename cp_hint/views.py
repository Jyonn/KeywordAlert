import datetime

from Config.models import Config
from News.models import News, Keyword, Log
from admin.models import Admin
from base.decorator import require_post, require_json, require_params
from base.grab import qdaily_grab, cnbeta_grab, techweb_grab, leiphone_grab, sspai_grab, dgtle_grab
from base.response import response
from cp_hint.settings import QDAILY_SIGNAL, QDAILY_INTERVAL, CNBETA_SIGNAL, CNBETA_INTERVAL, TECHWEB_SIGNAL, \
    TECHWEB_INTERVAL, \
    SSPAI_SIGNAL, SSPAI_INTERVAL, LEIPHONE_SIGNAL, LEIPHONE_INTERVAL, DGTLE_SIGNAL, DGTLE_INTERVAL


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
    Config.create(DGTLE_SIGNAL, '0')  # 数字尾巴上次抓取时间
    Config.create(DGTLE_INTERVAL, '20')  # 数字尾巴抓取时间间隔

    Config.create('lasting', '10')  # 默认新闻频率统计范围
    Config.create('interval', '10')  # 默认统计数据时间间隔
    Config.create('analyse-signal', '0')  # 默认统计数据时间
    Admin.create('cp', 'Chaping321')
    return response()


def news_dealer(request):
    """
    网站统一抓取 10s访问一次
    """
    funcs = [qdaily_grab, cnbeta_grab, techweb_grab, sspai_grab, leiphone_grab, dgtle_grab]
    for func in funcs:
        ret = func()  # 执行抓取
        if ret is None:
            continue
        news_list, signal, source = ret
        for news in news_list:  # 存储到数据库
            News.create(news, source)
        Config.create(signal, str(int(datetime.datetime.now().timestamp())))  # 更新上次抓取时间
    return response()


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
    # print(len(newses), begin_time)
    for o_keyword in keywords:
        kw = o_keyword.kw.upper()
        count = 0
        web_list = []
        for news in newses:
            if news.title.upper().find(kw) != -1:
                count += 1
                if news.source not in web_list:
                    web_list.append(news.source)
        # print(kw, count, len(web_list))
        if count >= o_keyword.count and len(web_list) >= o_keyword.web_count:
            Log.create(kw, count, len(web_list), count*len(web_list)//(o_keyword.count*o_keyword.web_count))

    o_last.value = str(int(crt_time.timestamp()))
    o_last.save()
    return response()


def delete_old(request):
    crt_time = datetime.datetime.now()
    old_time = crt_time - datetime.timedelta(days=1)
    newses = News.objects.filter(create_time__lt=old_time)
    for news in newses:
        news.delete()
    logs = News.objects.filter(create_time__lt=old_time)
    for log in logs:
        log.delete()
    return response()


@require_post
@require_json
@require_params(['last_log_id', 'last_news_id'])
def refresh_hot(request):
    last_log_id = int(request.POST['last_log_id'])
    last_news_id = int(request.POST['last_news_id'])
    if last_log_id == -1:
        logs = Log.objects.all().order_by('-pk')[:20]
    else:
        logs = Log.objects.filter(pk__gt=last_log_id)
    log_list = []
    latest_log_id = last_log_id
    for log in logs:
        log_list.append(dict(
            kw=log.kw,
            count=log.count,
            web_count=log.web_count,
            great=log.great,
            tag=log.get_tag(),
        ))
        if latest_log_id < log.pk:
            latest_log_id = log.pk

    if last_news_id == -1:
        newses = News.objects.all().order_by('-pk')
    else:
        newses = News.objects.filter(pk__gt=last_news_id)
    news_list = []
    latest_news_id = last_news_id
    kws = Keyword.objects.all()
    for news in newses:
        title = news.title.upper()
        for kw in kws:
            if title.find(kw.kw.upper()) != -1:
                title = title.replace(kw.kw.upper(), '<p class="highlight">'+kw.kw.upper()+'</p>')
        news_list.append(dict(
            # publish_time=news.publish_time,
            title=title,
            url=news.get_web_url(),
            source=news.get_source(),
        ))
        if latest_news_id < news.pk:
            latest_news_id = news.pk
    return response(body=dict(
        logs=log_list,
        last_log_id=latest_log_id,
        newses=news_list,
        last_news_id=latest_news_id,
    ))
