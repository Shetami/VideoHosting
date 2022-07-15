from djoser.serializers import PasswordSerializer
from rest_framework import generics, viewsets, status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Serial, User
from .serializers import SerialSerializer, SerialDetailSerializer, SerialReviewSerializer, SerialRatingSerializer, \
    UserRegistrationSerializer
from .filters import SerialFilter
from ..utils.calculate_rating import calculate_rating
from ..utils.pagination import PaginationSerials


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


class UserViewSet(viewsets.ModelViewSet):
    """
    A viewset that provides the standard actions
    """
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer

    @action(detail=True, methods=['post'])
    def set_password(self, request, pk=None):
        user = self.get_object()
        serializer = PasswordSerializer(data=request.data)
        if serializer.is_valid():
            user.set_password(serializer.validated_data['password'])
            user.save()
            return Response({'status': 'password set'})
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False)
    def recent_users(self, request):
        recent_users = User.objects.all().order_by('-last_login')

        page = self.paginate_queryset(recent_users)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(recent_users, many=True)
        return Response(serializer.data)
