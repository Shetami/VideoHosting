from django.urls import path

from . import views


urlpatterns = [
    path("", views.SerialAPIView.as_view(), name='list'),
    path("<int:pk>/", views.SerialDetailAPIView.as_view(), name='detail'),
    path("review/", views.SerialReviewAPIView.as_view(), name='review'),
    path("rating/", views.SerialRatingAPIView.as_view(), name='rating'),
    path("video/<int:pk>/", views.VideoWatcher.as_view(), name='video')
]