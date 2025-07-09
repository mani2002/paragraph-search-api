from django.urls import path
from .views import ProcessParagraphsView, SearchWordView

urlpatterns = [
    path('process/', ProcessParagraphsView.as_view(), name='process-paragraphs'),
    path('search/', SearchWordView.as_view(), name='search-word'),
]