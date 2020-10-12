from rest_framework import viewsets
from rest_framework import generics, viewsets, status
from rest_framework.response import Response
from rest_framework import permissions, authentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import action
from .models import UserProfile
from .serializers import UserRegSerializer, UserChangePasswordSerializer


# Create your views here.

class UserRegViewset(generics.CreateAPIView):
    serializer_class = UserRegSerializer
    queryset = UserProfile.objects.all()

class UserChangePasswordViewset(viewsets.GenericViewSet):
    serializer_class = UserChangePasswordSerializer
    
    def get_queryset(self):
        return UserProfile.objects.filter(username=self.request.user)
    
    def post(self, request, pk=None):
        user = self.get_object()
        if user.check_password(request.data['old_password']):

            user.set_password(request.data['new_password'])
            user.save()
            return Response({'status': 'success'}, status=status.HTTP_200_OK)
            
        return Response({'old_password':'原密码不正确'},status=status.HTTP_400_BAD_REQUEST)


    