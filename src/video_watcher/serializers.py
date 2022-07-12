from rest_framework import serializers

from .models import Serial, Rating


class SerialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Serial
        fields = ('title', 'image', 'date', 'studio', 'genres')


class SerialDetailSerializer(serializers.ModelSerializer):
    """All info serial"""
    studio = serializers.SlugRelatedField(slug_field="name", read_only=True)
    genres = serializers.SlugRelatedField(slug_field="name", read_only=True, many=True)

    class Meta:
        model = Serial
        fields = '__all__'


class SerialReviewSerializer(serializers.ModelSerializer):
    """Review and rating serial"""
    user = serializers.SlugRelatedField(slug_field="name", read_only=True)
    serial = serializers.SlugRelatedField(slug_field="name", read_only=True, many=True)

    class Meta:
        model = Rating
        fields = '__all__'
