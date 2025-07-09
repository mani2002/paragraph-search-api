from django.contrib import admin
from .models import Paragraph, WordParagraphMapping

@admin.register(Paragraph)
class ParagraphAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at')
    search_fields = ('content',)
    list_filter = ('user',)

@admin.register(WordParagraphMapping)
class WordParagraphMappingAdmin(admin.ModelAdmin):
    list_display = ('word', 'paragraph', 'count')
    search_fields = ('word',)
    list_filter = ('word',)