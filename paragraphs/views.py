import re
from collections import Counter
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Paragraph, WordParagraphMapping
from .serializers import ParagraphInputSerializer, ParagraphSerializer, WordSearchSerializer

class ProcessParagraphsView(generics.CreateAPIView):
    serializer_class = ParagraphInputSerializer
    permission_classes = [IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        text = serializer.validated_data['text']
        
        # Split text into paragraphs (two newlines)
        paragraphs = re.split(r'\n\s*\n', text)
        
        processed_paragraphs = []
        
        for paragraph_content in paragraphs:
            if not paragraph_content.strip():
                continue
                
            # Create paragraph record
            paragraph = Paragraph.objects.create(
                content=paragraph_content,
                user=request.user
            )
            
            # Process words in paragraph
            words = paragraph_content.split()
            # Convert to lowercase and remove punctuation
            words = [re.sub(r'[^\w\s]', '', word.lower()) for word in words]
            # Remove empty strings
            words = [word for word in words if word]
            
            # Count word frequencies
            word_counts = Counter(words)
            
            # Create word-paragraph mappings
            for word, count in word_counts.items():
                WordParagraphMapping.objects.create(
                    word=word,
                    paragraph=paragraph,
                    count=count
                )
            
            processed_paragraphs.append(paragraph)
        
        return Response({
            "message": f"Processed {len(processed_paragraphs)} paragraphs",
            "paragraphs": ParagraphSerializer(processed_paragraphs, many=True).data
        }, status=status.HTTP_201_CREATED)

class SearchWordView(generics.GenericAPIView):
    serializer_class = WordSearchSerializer
    permission_classes = [IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        word = serializer.validated_data['word'].lower()
        
        # Find paragraphs containing the word
        mappings = WordParagraphMapping.objects.filter(
            word=word, 
            paragraph__user=request.user
        ).select_related('paragraph').order_by('-count')[:10]
        
        paragraphs = [mapping.paragraph for mapping in mappings]
        
        return Response({
            "word": word,
            "paragraphs": ParagraphSerializer(paragraphs, many=True).data
        })