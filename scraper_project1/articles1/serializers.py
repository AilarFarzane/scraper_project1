from rest_framework import serializers
from .models import Article

class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = '__all__'

    def validate_title(self, value):
        if len(value) > 255:
            raise serializers.ValidationError("Title is too long.")
        return value