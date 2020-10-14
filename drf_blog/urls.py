"""drf_blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path

from django.views.static import serve
from django.conf import settings

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


from rest_framework import routers

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


from blog.views import ArticleListViewSet, ArticleCreateViewSet
from users.views import SmsCodeViewset, UserVireset

router = routers.DefaultRouter()
router.register('all_article', ArticleListViewSet, basename='all_article')
router.register('article', ArticleCreateViewSet, basename='article')

router.register('user',UserVireset, basename='user')




schema_view = get_schema_view(
    openapi.Info(
        title="DRF-Blog API",
        default_version='v1',
        description="Test description",
        # terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="459153431@qq.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)
swagger_urlpatterns = [
    # path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    # path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

]

log_url = [
    path('code/', SmsCodeViewset.as_view(), name='code'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    #path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

]

urlpatterns = [
    
    path('api-auth/', include('rest_framework.urls')),
    
    path('admin/', admin.site.urls),

    path('ueditor/', include('DjangoUeditor.urls')),

    path('api/v1/', include(router.urls)),
    path('api/v1/', include(log_url)),

    re_path('media/(?P<path>.*)', serve, {'document_root': settings.MEDIA_ROOT}),
]
urlpatterns += swagger_urlpatterns
