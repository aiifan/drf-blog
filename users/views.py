from random import choice
from django.core.mail import send_mail
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from rest_framework import permissions
from rest_framework.authentication import SessionAuthentication

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import action

from .serializers import SmsSerializer, UserDetailSerializer, UserRegSerializer, ChangePasswordSerializer
from .models import VerifyCode
from .permissions import IsOwnerOrReadOnly
# Create your views here.
User = get_user_model()

# class CustomBackend(ModelBackend):
#     """
#     自定义用户验证
#     """
#     def authenticate(self, request, username=None, password=None, **kwargs):
#         try:
#             user = User.objects.get(Q(username=username)|Q(email=username))
#             if user.check_password(password):
#                 return user
#         except Exception as e:
#             return None



class SmsCodeViewset(generics.CreateAPIView):
    """
    发送验证码
    """
    serializer_class = SmsSerializer

    def generate_code(self):
        """
        生成四位数字的验证码
        :return:
        """
        seeds = "1234567890"
        random_str = []
        for i in range(4):
            random_str.append(choice(seeds))

        return "".join(random_str)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        code = self.generate_code()
        send_mail('注册验证码', '{}'.format(code), from_email=None, recipient_list=[email], fail_silently=False)
        code_record = VerifyCode(code=code, email=email)
        code_record.save()
        return Response({'msg':'ok', 'code':code}, status=status.HTTP_201_CREATED)

# from rest_framework.views import APIView


# class UserRegView(APIView):

#     def get(self,request):
#         users=User.objects.all()
#         serializer=UserRegSerializer(users,many=True)
#         return Response(serializer.data)

#     def post(self, request):
#         s = UserRegSerializer(data=request.data)
#         if s.is_valid():
#             s.save()
#             return Response(data=s.data, status=status.HTTP_201_CREATED)
#         return Response(s.error_messages, status=status.HTTP_400_BAD_REQUEST)



class UserVireset(mixins.CreateModelMixin,mixins.RetrieveModelMixin,mixins.UpdateModelMixin,mixins.ListModelMixin,viewsets.GenericViewSet):
    """
    list:
    查看用户
    create:
    注册用户
    retrieve:
    查看用户详情
    update:
    更新用户信息
    partial_update:
    局部更新用户信息
    change_password:
    修改密码
    """

    # serializer_class = UserRegSerializer

    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.action == "change_password":
            return ChangePasswordSerializer
        elif self.action == 'retrieve':
            return UserDetailSerializer
        elif self.action == 'partial_update':
            return UserDetailSerializer
        elif self.action == 'update':
            return UserDetailSerializer
        return UserRegSerializer
        
    
    # def get_queryset(self):
    #     return User.objects.filter(username=self.request.user)

    authentication_classes = (SessionAuthentication, JWTAuthentication)

    def get_permissions(self):
        if self.action == "retrieve":
            return [IsOwnerOrReadOnly()]
        elif self.action == "change_password":
            return [IsOwnerOrReadOnly()]
        elif self.action == "update":
            return [IsOwnerOrReadOnly()]
        elif self.action == 'partial_update':
            return [IsOwnerOrReadOnly()]
        return []
    
    @action(detail=True, methods=['post'], serializer_class=ChangePasswordSerializer, permission_classes=(IsOwnerOrReadOnly,))
    def change_password(self, request, pk=None):
        user = self.get_object() # 返回应用于详细试图的对象示例，默认是使用lookup_field参数过滤基本查询及
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            if user.check_password(request.data['old_password']):
                if request.data['new_password'] == request.data['again_password']:
                    user.set_password(request.data['new_password'])
                    user.save()
                    return Response({'msg':'密码修改成功'}, status=status.HTTP_200_OK)
                else:
                    return Response({'msg':'两次输入密码不一致'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'msg':'原密码不正确'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'msg':'原密码不正确'}, status=status.HTTP_400_BAD_REQUEST)
