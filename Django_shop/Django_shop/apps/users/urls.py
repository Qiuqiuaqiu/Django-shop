from django.conf.urls import url
from rest_framework_jwt.views import obtain_jwt_token

from users import views

urlpatterns = [
    url(r'^usernames/(?P<username>\w{5,20})/count/$', views.UsernameCountView.as_view()), #判断用户名是否存在
    url(r'^mobiles/(?P<mobile>1[3-9]\d{9})/count/$', views.MobileCountView.as_view()), #判断手机号是否存在
    url(r'^users/$', views.UserView.as_view()), #注册接口
    url(r'^authorizations/$', obtain_jwt_token), #登录接口
]