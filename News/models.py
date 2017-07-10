from django.db import models


class News(models.Model):
    """
    新闻类
    """
    L = {
        'news_id': 50,
        'title': 511,
        'news_url': 1023,
    }
    SOURCE_UNK = -1  # 预留未知新闻源
    SOURCE_QDAILY = 0
    SOURCE_CNBETA = 1
    SOURCE_TECHWEB = 2
    SOURCE_SSPAI = 3
    SOURCE_LEIPHONE = 4
    SOURCE_DGTLE = 5
    SOURCE_ITHOME = 6
    SOURCE_KR36 = 7
    SOURCE_9TO5MAC = 8
    SOURCE_9TO5GOOGLE = 9
    SOURCE_SOLIDOT = 10
    SOURCE_ENGADGETCN = 11
    SOURCE_ENGADGETEN = 12

    # 新闻源表
    SOURCE_TABLE = (
        (SOURCE_UNK, 'unknown'),
        (SOURCE_QDAILY, 'qdaily'),
        (SOURCE_CNBETA, 'cnbeta'),
        (SOURCE_TECHWEB, 'techweb'),
        (SOURCE_SSPAI, 'sspai'),
        (SOURCE_LEIPHONE, 'leiphone'),
        (SOURCE_DGTLE, 'dltle'),
        (SOURCE_ITHOME, 'ithome'),
        (SOURCE_KR36, '36kr'),
        (SOURCE_9TO5MAC, '9to5mac'),
        (SOURCE_9TO5GOOGLE, '9to5google'),
        (SOURCE_SOLIDOT, 'solidot'),
        (SOURCE_ENGADGETCN, 'engadgetcn'),
        (SOURCE_ENGADGETEN, 'engadgeten')

    )
    # 新闻源中文注释
    SOURCE_CHINESE = (
        (SOURCE_UNK, '未知'),
        (SOURCE_QDAILY, '好奇心'),
        (SOURCE_CNBETA, 'CNBETA'),
        (SOURCE_TECHWEB, 'TECHWEB'),
        (SOURCE_SSPAI, '少数派'),
        (SOURCE_LEIPHONE, '雷锋网'),
        (SOURCE_DGTLE, '数字尾巴'),
        (SOURCE_ITHOME, 'IT之家'),
        (SOURCE_KR36, '36氪'),
        (SOURCE_9TO5MAC, '9TO5MAC'),
        (SOURCE_9TO5GOOGLE, '9TO5GOOGLE'),
        (SOURCE_SOLIDOT, '奇客'),
        (SOURCE_ENGADGETCN, '瘾科技CN'),
        (SOURCE_ENGADGETEN, '瘾科技EN')
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
        """
        创建新闻
        :param news: dict类型新闻体
        :param source: 新闻来源
        :return:
        """
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
        """
        获取中文新闻源注释
        """
        for item in News.SOURCE_CHINESE:
            if item[0] == self.source:
                return item[1]

    def get_web_url(self):
        """
        获取桌面版新闻链接
        """
        if self.source == News.SOURCE_QDAILY:
            return self.news_url.replace('m.qdaily', 'www.qdaily')
        elif self.source == News.SOURCE_CNBETA:
            return self.news_url.replace('m.cnbeta.com/wap/view', 'www.cnbeta.com/articles/comic')
        elif self.source == News.SOURCE_TECHWEB:
            return self.news_url.replace('m.techweb', 'www.techweb')
        elif self.source == News.SOURCE_SSPAI:
            return self.news_url
        elif self.source == News.SOURCE_LEIPHONE:
            return self.news_url.replace('m.leiphone', 'www.leiphone')
        else:
            return self.news_url


class KeywordGroup(models.Model):
    """
    关键字组类
    """
    L = {
        'group_name': 20,
    }
    group_name = models.CharField(
        verbose_name='组名',
        max_length=L['group_name'],
        unique=True,
        db_index=True,
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
    def create(cls, group_name, count, web_count):
        """
        创建关键字
        :param group_name: 组名
        :param count: 总个数
        :param web_count: 网站数
        """
        o = cls(
            group_name=group_name,
            count=count,
            web_count=web_count,
        )
        try:
            o.save()
            return o
        except:
            try:
                return KeywordGroup.objects.get(group_name=group_name)
            except:
                return None


class Keyword(models.Model):
    """
    关键字类
    """
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
    group_id = models.IntegerField(
        verbose_name='GROUP ID',
        default=None,
    )

    @classmethod
    def create(cls, kw, count, web_count):
        """
        创建关键字
        :param kw: 关键字
        :param count: 总个数
        :param web_count: 网站数
        """
        o_group = KeywordGroup.create(kw, count, web_count)
        if o_group is None:
            return None
        o_keyword = cls(
            kw=kw,
            count=count,
            web_count=web_count,
            disable=False,
            group_id=o_group.pk,
        )
        try:
            o_keyword.save()
        except:
            pass


class Log(models.Model):
    """
    log类
    """
    L = {
        'kw': 20,
    }
    create_time = models.DateTimeField(
        verbose_name='创建时间',
        auto_created=True,
        auto_now=True,
    )
    kw = models.CharField(
        verbose_name='关键字组名',
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
        """
        创建log
        :param kw: 关键词
        :param count: 真实总个数
        :param web_count: 真实网站个数
        :param great: 与期待值的倍数
        :return:
        """
        o_log = cls(kw=kw, count=count, web_count=web_count, great=great)
        o_log.save()

    def get_tag(self):
        """
        根据great倍数，获取相应颜色tag
        """
        if self.great == 1:
            return 'item-normal'
        elif self.great == 2:
            return 'item-success'
        else:
            return 'item-hot'
