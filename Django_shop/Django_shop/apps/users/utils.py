import re

from django.contrib.auth.backends import ModelBackend

from users.models import User


def jwt_response_payload_handler(token,user=None,request=None):

    return {
        'token': token,
        'user_id': user.id,
        'username': user.username
    }


#能够通过用户名或者手机号进行登录逻辑实现
def get_user_by_account(account):
    try:
        if re.match(r'1[3-9]\d{9}',account):
            user = User.objects.get(mobile=account)
        else:
            user = User.objects.get(username=account)
    except User.DoesNotExist:
        return None
    else:
        return user

class UsernameMobileAuthBackend(ModelBackend):

    def authenticate(self, request, username=None, password=None, **kwargs):
        user = get_user_by_account(username)

        if user is not None and user.check_password(password):
            return user