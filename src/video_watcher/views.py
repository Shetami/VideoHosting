from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Serial, Rating
from .serializers import SerialSerializer, SerialDetailSerializer, SerialReviewSerializer
from .filters import SerialFilter


class SerialAPIView(generics.ListAPIView):
    """Displaying the list of series"""
    queryset = Serial.objects.all()
    serializer_class = SerialSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
    filterset_class = SerialFilter
    search_fields = ('title', 'genres__name',)


class SerialRating(APIView):

    def get_rating_and_review(self, pk):
        rating = Rating.objects.filter(serial_id=pk)
        print(Rating.objects.filter(serial_id=pk))
        serializer = SerialReviewSerializer(rating)
        return Response(serializer.data)


class SerialDetailAPIView(SerialRating, APIView):
    """Series page"""

    def post(self, request):
        serializer = SerialReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
        return Response(status=201)

    def get(self, request, pk):
        serial = Serial.objects.get(id=pk)
        serializer = SerialDetailSerializer(serial)
        return Response(serializer.data)

