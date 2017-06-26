from django.db import models


class News(models.Model):
    L = {
        'news_id': 30,
        'title': 511,
        'news_url': 1023,
    }
    SOURCE_UNK = -1
    SOURCE_QDAILY = 0
    SOURCE_CNBETA = 1
    SOURCE_TECHWEB = 2
    SOURCE_SSPAI = 3
    SOURCE_LEIPHONE = 4
    SOURCE_TABLE = (
        (SOURCE_UNK, 'unknown'),
        (SOURCE_QDAILY, 'qdaily'),
        (SOURCE_CNBETA, 'cnbeta'),
        (SOURCE_TECHWEB, 'techweb'),
        (SOURCE_SSPAI, 'sspai'),
        (SOURCE_LEIPHONE, 'leiphone'),
    )
    SOURCE_CHINESE = (
        (SOURCE_UNK, '未知'),
        (SOURCE_QDAILY, '好奇心'),
        (SOURCE_CNBETA, 'CNBETA'),
        (SOURCE_TECHWEB, 'TECHWEB'),
        (SOURCE_SSPAI, '少数派'),
        (SOURCE_LEIPHONE, '雷锋网'),
    )
    source = models.IntegerField(
        verbose_name='新闻源',
        choices=SOURCE_TABLE,
        default=SOURCE_UNK,
    )
    news_id = models.CharField(
        verbose_name='唯一ID',
        max_length=L['news_id'],
        default=None,
        unique=True,
    )
    title = models.CharField(
        verbose_name='新闻标题',
        max_length=L['title'],
        default=None,
    )
    news_url = models.CharField(
        verbose_name='新闻链接',
        max_length=L['news_url'],
        default=None,
    )
    create_time = models.DateTimeField(
        verbose_name='创建时间',
        auto_created=True,
        auto_now=True,
    )
    publish_time = models.DateTimeField(
        verbose_name='新闻存在时间',
    )
    content = models.TextField(
        verbose_name='正文',
        help_text='保留字段',
        default=None,
        null=True,
        blank=True,
    )

    @classmethod
    def create(cls, news, source):
        source_str = None
        for item in News.SOURCE_TABLE:
            if item[0] == source:
                source_str = item[1]
        if source_str is None:
            return
        o_news = cls(
            source=source,
            news_id=source_str+'_'+str(news['id']),
            title=news['title'],
            news_url=news['url'],
            publish_time=news['publish_time'],
        )
        try:
            o_news.save()
        except:
            pass

    def get_source(self):
        for item in News.SOURCE_CHINESE:
            if item[0] == self.source:
                return item[1]


class Keyword(models.Model):
    L = {
        'kw': 10,
    }
    kw = models.CharField(
        verbose_name='关键字',
        max_length=L['kw'],
        unique=True,
    )
    count = models.IntegerField(
        verbose_name='出现次数',
        default=1,
    )
    web_count = models.IntegerField(
        verbose_name='出现网站个数',
        default=1,
    )
    disable = models.BooleanField(
        verbose_name='是否禁用',
        default=False,
    )

    @classmethod
    def create(cls, kw, count, web_count):
        o_keyword = cls(
            kw=kw,
            count=count,
            web_count=web_count,
            disable=False,
        )
        try:
            o_keyword.save()
        except:
            pass


class Log(models.Model):
    L = {
        'kw': 10,
    }
    create_time = models.DateTimeField(
        verbose_name='创建时间',
        auto_created=True,
        auto_now=True,
    )
    kw = models.CharField(
        verbose_name='关键字',
        max_length=L['kw'],
    )
    count = models.IntegerField(
        verbose_name='出现次数',
        default=1,
    )
    web_count = models.IntegerField(
        verbose_name='出现网站个数',
        default=1,
    )
    great = models.IntegerField(
        verbose_name='与期待值的倍数',
        default=1,
    )

    @classmethod
    def create(cls, kw, count, web_count, great):
        o_log = cls(kw=kw, count=count, web_count=web_count, great=great)
        # try:
        o_log.save()
        # except:
        #     pass

    def get_tag(self):
        if self.great == 1:
            return 'item-normal'
        elif self.great == 2:
            return 'item-success'
        else:
            return 'item-hot'
