from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from django.contrib.auth import get_user_model

from datetime import datetime
from datetime import timedelta


from .models import VerifyCode


USER = get_user_model()

class SmsSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, email):
        if USER.objects.filter(email=email).count():
            raise serializers.ValidationError("用户已经存在")
        one_mintes_ago = datetime.now() - timedelta(hours=0, minutes=1, seconds=0)
        if VerifyCode.objects.filter(add_time__gt=one_mintes_ago, email=email).count():
            raise serializers.ValidationError("距离上一次发送未超过60s")

        return email

class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = USER
        fields = ('id', 'nick_name', 'username', 'avatar','mobile')

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(style={'input_type': 'password'}, label="原密码", write_only=True)
    new_password = serializers.CharField(style={'input_type': 'password'}, label="新密码", write_only=True)
    again_password = serializers.CharField(style={'input_type': 'password'}, label="再次新密码", write_only=True)


class UserRegSerializer(serializers.ModelSerializer):
    code = serializers.CharField(required=True, write_only='True', max_length=4, min_length=4, label='验证码', error_messages={
                                    "blank": "请输入验证码",
                                    "required": "请输入验证码",
                                    "max_length": "验证码格式错误",
                                    "min_length": "验证码格式错误"
                                })
    username = serializers.EmailField(label="邮箱", required=True, allow_blank=False,
                                    validators=[UniqueValidator(queryset=USER.objects.all(), message="邮箱已经存在")])
    password = serializers.CharField(style={'input_type': 'password'}, label="密码", write_only=True)

    def validate_code(self, code):

        verify_records = VerifyCode.objects.filter(email=self.initial_data["username"]).order_by("-add_time")
        if verify_records:
            last_record = verify_records[0]

            five_mintes_ago = datetime.now() - timedelta(hours=0, minutes=5, seconds=0)
            if five_mintes_ago > last_record.add_time:
                raise serializers.ValidationError("验证码过期")

            if last_record.code != code:
                raise serializers.ValidationError("验证码错误")

        else:
            raise serializers.ValidationError("验证码错误")

    def create(self, validated_data):
        user=USER(**validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user

    def validate(self, attrs):
        attrs["email"] = attrs["username"]
        del attrs["code"]
        return attrs
    class Meta:
        model = USER
        fields = ('id','nick_name', "username", "code", 'avatar', "password")
    