from rest_framework import serializers


from .models import UserProfile


class UserChangePasswordSerializer(serializers.Serializer):
    """
    修改密码序列化类
    """
    old_password = serializers.CharField(label='原密码', required=True, style={'input_type':'password'})
    new_password = serializers.CharField(label='新密码', required=True, style={'input_type':'password'})
    again_password = serializers.CharField(label='新密码', required=True, style={'input_type':'password'})


class UserRegSerializer(serializers.ModelSerializer):
    
    password = serializers.CharField(style={'input_type':'password'}, label='密码', write_only=True)

    class Meta:
        model = UserProfile
        fields = ('id','username','password', 'nickname', 'head')
