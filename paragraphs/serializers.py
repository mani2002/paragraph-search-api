from rest_framework import serializers
from .models import Paragraph, WordParagraphMapping

class ParagraphInputSerializer(serializers.Serializer):
    text = serializers.CharField(write_only=True)
    
class ParagraphSerializer(serializers.ModelSerializer):
    class Meta:
        model = Paragraph
        fields = ('id', 'content', 'created_at')
        read_only_fields = ('id', 'created_at')

class WordSearchSerializer(serializers.Serializer):
    word = serializers.CharField()