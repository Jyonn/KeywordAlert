from django.db import models


class Admin(models.Model):
    username = models.CharField(
        verbose_name="用户名",
        max_length=20,
        unique=True,
    )
    password = models.CharField(
        verbose_name="密码",
        max_length=32,
    )

    @classmethod
    def create(cls, username, password):
        try:
            cls(username=username, password=password).save()
        except:
            return None
