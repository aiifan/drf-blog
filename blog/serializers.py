from rest_framework import serializers


from .models import Article



class ArticleListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Article
        fields = '__all__'

class ArticleSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    # title = serializers.CharField(required=False)

    def validate_title(self, title):
        print(title)
        if not title:
            raise serializers.ValidationError('title是必填项')
        return title

    class Meta:
        model = Article
        fields = '__all__'