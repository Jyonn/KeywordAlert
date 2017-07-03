from admin.models import Admin
from base.common import logout_user_from_session, login_to_session
from base.decorator import *


@require_post
@require_json
@require_params(['username', 'password'])
def login(request):
    """
    用户登录
    """
    username = request.POST['username']
    password = request.POST['password']
    try:
        admin = Admin.objects.get(username=username, password=password)
        login_to_session(request, admin)
        return response()
    except:
        return error_response(Error.ERROR_PASSWORD)


@require_post
def logout(request):
    logout_user_from_session(request)
    return response()
