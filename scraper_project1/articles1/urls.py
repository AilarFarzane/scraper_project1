from django.urls import path
from .views import ArticleList, ArticleDetail
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('api/articles/', ArticleList.as_view(), name='ArticleList'),
    path('api/articles/<int:pk>/', ArticleDetail.as_view(), name='ArticleDetail'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]