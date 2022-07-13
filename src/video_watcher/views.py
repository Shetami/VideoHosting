from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Serial, Rating
from .serializers import SerialSerializer, SerialDetailSerializer, SerialReviewSerializer, SerialRatingSerializer
from .filters import SerialFilter


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
        rating = Rating.objects.filter(serial=pk)
        rating_count = Rating.objects.filter(serial=pk).count()
        sum_r = 0
        for i in rating:
            sum_r += i.rate
        sum_r = sum_r/rating_count
        serial.rating_sum = sum_r
        serializer = SerialDetailSerializer(serial)
        return Response(serializer.data)


class SerialReviewAPIView(APIView):
    """Reviews user"""

    def post(self, request):
        review = SerialReviewSerializer(data=request.data)
        if review.is_valid():
            review.save()
            return Response(status=201)
        else:
            return Response(status=400)


class SerialRatingAPIView(APIView):
    """Rating user"""

    def post(self, request):
        rating = SerialRatingSerializer(data=request.data)
        if rating.is_valid():
            rating.save()
            return Response(status=201)
        else:
            return Response(status=400)

