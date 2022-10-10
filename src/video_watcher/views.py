from django.http import StreamingHttpResponse
from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Serial
from .serializers import SerialSerializer, SerialDetailSerializer, SerialReviewSerializer, SerialRatingSerializer
from .filters import SerialFilter
from ..utils.calculate_rating import calculate_rating
from ..utils.open_file import open_file


class SerialAPIView(generics.ListAPIView):
    """Displaying the list of series"""
    queryset = Serial.objects.all()
    serializer_class = SerialSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
    filterset_class = SerialFilter
    search_fields = ('title', 'genres__name',)


class SerialDetailAPIView(APIView):
    """Serials info detail"""

    def get(self, request, pk):
        serial = Serial.objects.get(id=pk)
        serial.rating_sum = calculate_rating(pk)
        serializer = SerialDetailSerializer(serial)
        return Response(serializer.data)


class SerialReviewAPIView(APIView):
    """Reviews user"""
    permission_classes = [IsAuthenticatedOrReadOnly]

    def post(self, request):
        review = SerialReviewSerializer(data=request.data)
        if review.is_valid():
            review.save()
            return Response(status=201)
        else:
            return Response(status=400)


class SerialRatingAPIView(APIView):
    """Rating user"""
    permission_classes = [IsAuthenticatedOrReadOnly]

    def post(self, request):
        rating = SerialRatingSerializer(data=request.data)
        if rating.is_valid():
            rating.save()
            return Response(status=201)
        else:
            return Response(status=400)


class VideoWatcher(APIView):
    """Video watcher"""

    def get(self, request, pk: int):
        file, status, content_length, content_range = open_file(request, pk)
        response = StreamingHttpResponse(file, status=status, content_type='video/mp4')

        response['Accept-Ranges'] = 'bytes'
        response['Content-Length'] = str(content_length)
        response['Cache-Control'] = 'no-cache'
        response['Content-Range'] = content_range
        return response
