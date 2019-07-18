from django.conf.urls import url

from orders import views

urlpatterns = [
    url('^orders/settlement/$', views.OrderSettlementView.as_view()),
    url('^orders/$', views.SaveOrderView.as_view()),
]