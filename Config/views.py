from django.shortcuts import render

from Config.models import Config
from News.models import Keyword
from base.common import get_user_from_session


def admin_page(request):
    admin = get_user_from_session(request)
    login = 'inline' if admin is None else 'none'
    logout = 'none' if admin is None else 'inline'
    login = 'display: ' + login
    logout = 'display: ' + logout

    keywords = Keyword.objects.all()
    key_list = []
    for kw in keywords:
        key_list.append(dict(
            id=kw.pk,
            kw=kw.kw,
            count=kw.count,
            web_count=kw.web_count,
        ))

    lasting = Config.objects.get(key='lasting').value
    interval = Config.objects.get(key='interval').value

    return render(request, 'admin.html', dict(
        lasting=lasting,
        interval=interval,
        login=login,
        logout=logout,
        keywords=key_list,
        is_login=admin is not None,
    ))


def index_page(request):
    return render(request, 'index.html')