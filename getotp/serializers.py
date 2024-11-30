from rest_framework import serializers

from .models import *


class RequestOtpSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=12, allow_null=False)
    channel = serializers.ChoiceField(allow_null=False, choices=['android', 'ios', 'web'])


class RequestOtpResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = OtpRequest
        fields = ['request_id']


class VerifyOtpSerializer(serializers.Serializer):
    request_id = serializers.CharField(max_length=64, allow_null=False)
    phone = serializers.CharField(max_length=12, allow_null=False)
    password = serializers.CharField(allow_null=False)


class VerifyOtpResponseSerializer(serializers.Serializer):
    token = serializers.CharField()
    new_user = serializers.BooleanField()
