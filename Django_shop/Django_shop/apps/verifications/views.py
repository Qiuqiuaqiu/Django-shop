from django.http import HttpResponse
from django.shortcuts import render
from django_redis import get_redis_connection
from rest_framework.generics import GenericAPIView
# Create your views here.
from rest_framework.views import APIView
from Django_shop.libs.captcha.captcha import captcha
from verifications import constants

# GET /image_codes/(?P<image_code_id>[\w-]+)/
class ImageCodeView(APIView):

    def get(self,request,image_code_id):

        _, text, image = captcha.generate_captcha()
        redis_conn = get_redis_connection('verify_codes')
        redis_conn.setex('img_%s' % image_code_id,constants.IMAGE_CODE_REDIS_EXPIRES,text)

        return HttpResponse(image,content_type='image/jpg')