from django.conf.urls import url

from users import views

urlpatterns = [
    url(r'^username/(?P<username>\w{5,20})/count/$', views.UsernameCountView.as_view()),
    url(r'^mobile/(?P<mobile>\1[3-9]\d{9})/count/$', views.MobileCountView.as_view()),
]