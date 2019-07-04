import random

from django.http import HttpResponse
from django.shortcuts import render
from django_redis import get_redis_connection
from rest_framework.generics import GenericAPIView
# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView
from Django_shop.libs.captcha.captcha import captcha
from Django_shop.utils.yuntongxun.sms import CCP
from verifications import constants

# GET /image_codes/(?P<image_code_id>[\w-]+)/
from verifications.serializer import ImageCodeCheckSerializer
from celery_tasks.sms.views import send_sms_code


class ImageCodeView(APIView):

    def get(self,request,image_code_id):

        _, text, image = captcha.generate_captcha()
        redis_conn = get_redis_connection('verify_codes')
        redis_conn.setex('img_%s' % image_code_id,constants.IMAGE_CODE_REDIS_EXPIRES,text)

        print('生成的验证码:%s' % text)
        print('image_code_id: %s' % image_code_id)

        return HttpResponse(image,content_type='image/jpg')

class SMSCodeView(GenericAPIView):
    serializer_class = ImageCodeCheckSerializer

    def get(self,request,mobile):
        serializer = self.get_serializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        sms_code = "%06d" % random.randint(0,999999)
        redis_conn = get_redis_connection('verify_codes')
        pl = redis_conn.pipeline()
        pl.setex("sms_%s" % mobile, constants.SMS_CODE_REDIS_EXPIRES, sms_code)
        pl.setex("send_flag_%s" % mobile, constants.SEND_SMS_CODE_INTERVAL, 1)
        pl.execute()

        print('短信验证码:%s' % sms_code)

        sms_code_expires = str(constants.SMS_CODE_REDIS_EXPIRES // 60)
        # ccp = CCP()
        # ccp.send_template_sms(mobile, [sms_code, sms_code_expires], 1)

        send_sms_code.delay(mobile,sms_code,sms_code_expires,constants.SMS_CODE_TEMP_ID)

        return Response({"message": "OK"})
