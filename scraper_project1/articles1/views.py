from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import status
from rest_framework.permissions import IsAuthenticated
from .models import Article
from .serializers import ArticleSerializer
from datetime import datetime


class ArticleList(generics.ListCreateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        date_published = self.request.query_params.get('date_published', None)
        if date_published:
            try:
                valid_date = datetime.strptime(date_published, '%Y-%m-%d').date()
                queryset = queryset.filter(date_published=valid_date)
            except ValueError:
                return Response({'error': 'Invalid date format. Use YYYY-MM-DD.'}, status=status.HTTP_400_BAD_REQUEST)
        return queryset


class ArticleDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)
