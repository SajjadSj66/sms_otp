from datetime import datetime
from django.conf import settings
from django.contrib.auth import get_user_model
from django.shortcuts import render
from kavenegar import KavenegarAPI
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle
from rest_framework.views import APIView
# from .models import OtpRequest
from .serializers import *


# Create your views here.

class OncePerMinuteThrottle(UserRateThrottle):
    rate = '1/minute'


class RequestOTP(APIView):
    throttle_classes = [OncePerMinuteThrottle]

    def post(self, request):
        serializer = RequestOtpSerializer(data=request.data)
        if serializer.is_valid():
            req_otp = OtpRequest()
            req_otp.phone = serializer.validated_data['phone']
            req_otp.channel = serializer.validated_data['channel']
            req_otp.generate_password()
            req_otp.save()

            # api = KavenegarAPI(settings.SMS_API_KEY)
            # response = api.verify_lookup({
            #     "receptor": req_otp.phone,
            #     'token': req_otp.password,
            #     'template': settings.OTP_TEMPLATE,
            # })
            # print(response)
            return Response(RequestOtpResponseSerializer(req_otp).data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyOTP(APIView):
    def post(self, request):
        serializer = VerifyOtpSerializer(data=request.data)
        if serializer.is_valid():
            query = OtpRequest.objects.filter(
                request_id=serializer.validated_data['request_id'],
                phone=serializer.validated_data['phone'],
                valid_until__gte=datetime.now()
            )
            if query.exists():
                User = get_user_model()
                userq = User.objects.filter(username=serializer.validated_data['phone'])
                if userq.exists():
                    user = userq.first()
                    token, created = Token.objects.get_or_create(user=user)
                    return Response(data=VerifyOtpResponseSerializer({'token': token, 'new_user': False}).data)
                else:
                    user = User.objects.create(username=serializer.validated_data['phone'])
                    token, created = Token.objects.get_or_create(user=user)
                    return Response(data=VerifyOtpResponseSerializer({'token': token, 'new_user': True}).data)

            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
