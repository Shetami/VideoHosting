from django.urls import path

from . import views


urlpatterns = [
    path("", views.SerialAPIView.as_view(), name='list'),
    path("<int:pk>/", views.SerialDetailAPIView.as_view(), name='detail')
]