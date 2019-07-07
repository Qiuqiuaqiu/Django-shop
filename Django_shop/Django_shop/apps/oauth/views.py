from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.settings import api_settings

from .exceptions import QQAuthException
from oauth.utils import OAuthQQ
from .models import OauthQQUser

#  url(r'^qq/authorization/$', views.QQAuthURLView.as_view()),
class QQAuthURLView(APIView):
    """
    获取QQ登录的url
    """
    def get(self, request):
        """
        提供用于qq登录的url
        """
        next = request.query_params.get('next')
        oauth = OAuthQQ(state=next)
        login_url = oauth.get_qq_login_url()
        return Response({'login_url': login_url})

class QQAuthUserView(APIView):
    """
    QQ登录的用户
    """
    def get(self,request):

        code = request.query_params.get('code')
        print("code:%s" % code)
        if not code:
            return Response({"message":"未获取到code"},status=status.HTTP_400_BAD_REQUEST)

        oauth = OAuthQQ()
        try:
            access_token = oauth.get_access_token(code)
            print("access_token:%s" % access_token)
            openid = oauth.get_openid(access_token)
            print("openid:%s" % openid)
        except QQAuthException:
            return Response({"message":"未获取到openid"},status=status.HTTP_503_SERVICE_UNAVAILABLE)
        try:
            qq_user = OauthQQUser.objects.get(openid=openid)
        except OauthQQUser.DoesNotExist:
            #未找到用户,保存openid
            token = oauth.generate_save_user_token(openid)
            return Response({'access_token': token})
        else:
            # 找到用户,生成token
            user = qq_user.user
            jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
            jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
            payload = jwt_payload_handler(user)
            token = jwt_encode_handler(payload)

            response = Response({
                'token': token,
                'user_id': user.id,
                'username': user.username
            })
            return response