from decimal import Decimal
from django.shortcuts import render

# Create your views here.
from django_redis import get_redis_connection
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from goods.models import SKU
from orders.serializers import OrderSettlementSerializer, SaveOrderSerializer


class OrderSettlementView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self,request):

        user = request.user

        redis_conn = get_redis_connection('cart')
        redis_cart = redis_conn.hgetall('cart_%s' % user.id)
        print('redis_cart:%s' % redis_cart)
        redis_selected = redis_conn.smembers('cart_selected_%s' % user.id)
        print('redis_selected: %s' % redis_selected)

        cart = {}
        for sku_id in redis_selected:
            cart[int(sku_id)] = int(redis_cart[sku_id])

        print('cart: %s' % cart)

        skus = SKU.objects.filter(id__in=cart.keys())
        print('skus:%s' % skus)
        for sku in skus:
            sku.count = cart[sku.id]
        freight = Decimal('10.00')

        serializer = OrderSettlementSerializer({'freight':freight, 'skus':skus})

        return Response(serializer.data)

class SaveOrderView(CreateAPIView):
    """
    保存订单
    """
    permission_classes = [IsAuthenticated]
    serializer_class = SaveOrderSerializer