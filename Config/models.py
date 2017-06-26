from django.db import models


class AbstractDict(models.Model):
    L = {
        'key': 511,
        'value': 1023,
    }
    key = models.CharField(
        verbose_name='键',
        max_length=L['key'],
    )
    value = models.CharField(
        verbose_name='值',
        max_length=L['value'],
    )

    class Meta:
        abstract = True


class Config(AbstractDict):
    @classmethod
    def create(cls, key, value):
        try:
            o_config = Config.objects.get(key=key)
            o_config.value = value
        except:
            o_config = cls(key=key, value=value)
        o_config.save()
        return o_config
