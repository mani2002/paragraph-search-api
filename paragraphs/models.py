import uuid
from django.db import models
from users.models import User

class Paragraph(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    content = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='paragraphs')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Paragraph {self.id}"

class WordParagraphMapping(models.Model):
    word = models.CharField(max_length=100, db_index=True)
    paragraph = models.ForeignKey(Paragraph, on_delete=models.CASCADE, related_name='word_mappings')
    count = models.IntegerField(default=1)
    
    class Meta:
        unique_together = ('word', 'paragraph')
        indexes = [
            models.Index(fields=['word']),
        ]
    
    def __str__(self):
        return f"{self.word} - {self.paragraph.id}"