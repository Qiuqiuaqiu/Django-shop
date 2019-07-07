import json
from urllib.parse import urlencode, parse_qs
from urllib.request import urlopen
from django.conf import settings
from rest_framework import response
from rest_framework.response import Response
from oauth import constants
import logging
from .exceptions import QQAuthException
from itsdangerous import TimedJSONWebSignatureSerializer as TJWSSerializer

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

        return access_token[0]
    def get_openid(self,access_token):
        """
       获取用户的openid
       :param access_token: qq提供的access_token
       :return: open_id
       """
        url = 'https://graph.qq.com/oauth2.0/me?access_token=' + access_token
        resp = urlopen(url)
        resp_data = resp.read().decode()
        try:
            data = json.loads(resp_data[10:-4])
        except Exception as e:
            data = parse_qs(resp_data)
            logger.error('code=%s msg=%s' % (data.get('code'), data.get('msg')))
            raise QQAuthException
        else:
            openid = data.get('openid', None)
        # 返回的数据 callback( {"client_id":"YOUR_APPID","openid":"YOUR_OPENID"} )\n;
        return openid

    @staticmethod
    def generate_save_user_token(openid):
        """
               生成保存用户数据的token
               :param openid: 用户的openid
               :return: token
               """
        serializer = TJWSSerializer(settings.SECRET_KEY, expires_in=constants.SAVE_QQ_USER_TOKEN_EXPIRES)
        data = {'openid': openid}
        token = serializer.dumps(data)
        return token.decode()