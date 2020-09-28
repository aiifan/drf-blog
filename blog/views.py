from rest_framework import viewsets
from rest_framework import mixins
from rest_framework import filters
from rest_framework.pagination import  PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import rest_framework as rest_filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication



from .serializers import ArticleListSerializer, ArticleSerializer
from .models import Article, Category
# Create your views here.

class ArticlePagination(PageNumberPagination):
    '''
    文章分页
    '''
    page_size = 12
    page_size_query_param = 'page_size'
    max_page_size = 100

class ArticeFilter(rest_filters.FilterSet):
    '''
    过滤
    '''
    pass


class ArticleListViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    '''
    查看所有文章
    '''
    queryset = Article.objects.all()
    serializer_class = ArticleListSerializer
    
    pagination_class = ArticlePagination #分页

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filter_fields = ('category', 'tags', 'user') #过滤
    ordering_fields = ('views', 'created_time', 'modified_time') #排序
    search_fields = ('title', 'excerpt', 'body', 'user') #搜索

class ArticleCreateViewSet(viewsets.ModelViewSet, viewsets.GenericViewSet):
    '''
    list:
    查看个人文章列表
    create:
    创建文章
    retrieve:
    文章详情
    update:
    更新文章
    partial_update:
    局部更新文章
    destroy:
    删除文章
    '''
    # queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    authentication_classes = (SessionAuthentication,JWTAuthentication)
    permission_classes = (IsAuthenticated,)
    def get_queryset(self):
        return Article.objects.filter(user=self.request.user)
    

    