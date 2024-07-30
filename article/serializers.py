from rest_framework import serializers
from .models import ArticleModel

class ArticleSerializer(serializers.ModelSerializer):
    author = serializers.CharField(read_only = True)

    class Meta:
        model= ArticleModel
        fields = ['id' , 'title' , 'description' , 'author']