from admin.models import Admin


def save_session(request, key, value):
    request.session["saved_" + key] = value


def load_session(request, key, once_delete=True):
    value = request.session.get("saved_" + key)
    if value is None:
        return None
    if once_delete:
        del request.session["saved_" + key]
    return value


def login_to_session(request, admin):
    try:
        request.session.cycle_key()
    except:
        pass
    save_session(request, 'admin', admin.pk)
    return None


def get_user_from_session(request):
    reader_pk = load_session(request, 'admin', once_delete=False)
    if reader_pk is None:
        return None
    try:
        return Admin.objects.get(pk=reader_pk)
    except:
        return None


def logout_user_from_session(request):
    load_session(request, 'admin')
