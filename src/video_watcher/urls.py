from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from rest_framework import routers

from . import views
from .views import UserViewSet

router = routers.SimpleRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
    path("", views.SerialAPIView.as_view(), name='list'),
    path('auth/', include(router.urls)),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/virify/', TokenVerifyView.as_view(), name='token_verify'),
    path("<int:pk>/", views.SerialDetailAPIView.as_view(), name='detail'),
    path("review/", views.SerialReviewAPIView.as_view(), name='review'),
    path("rating/", views.SerialRatingAPIView.as_view(), name='rating'),
]