from urllib.parse import urlencode, parse_qs
from urllib.request import urlopen
from django.conf import settings
from rest_framework.response import Response
import logging
from .exceptions import QQAuthException

logger = logging.getLogger('django')

class OAuthQQ(object):

    def __init__(self, client_id=None, client_secret=None, redirect_uri=None, state=None):
        self.client_id = client_id or settings.QQ_CLIENT_ID
        self.client_secret = client_secret or settings.QQ_CLIENT_SECRET
        self.redirect_uri = redirect_uri or settings.QQ_REDIRECT_URI
        self.state = state or settings.QQ_STATE  # 用于保存登录成功后的跳转页面路径

    def get_qq_login_url(self):

        params = {
            'response_type': 'code',
            'client_id': self.client_id,
            'redirect_uri': self.redirect_uri,
            'state': self.state,
            'scope': 'get_user_info',
        }

        url = 'https://graph.qq.com/oauth2.0/authorize?' + urlencode(params)

        return url

    def get_access_token(self,code):

        params = {
            'grant_type': 'authorization_code',
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'code': code,
            'redirect_uri': self.redirect_uri
        }

        url = 'https://graph.qq.com/oauth2.0/token?' + urlencode(params)
        try:
            response = urlopen(url)
            response_data = response.read().decode()
            data = parse_qs(response_data)
        except Exception as e:
            logger.error("获取access_token错误:%s" % e)
            raise QQAuthException
        else:
            access_token = data.get('access_token', None)

        return access_token