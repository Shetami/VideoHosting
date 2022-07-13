from rest_framework import serializers

from .models import Serial, Rating, Review


class SerialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Serial
        fields = ('title', 'image', 'date', 'studio', 'genres')


class SerialRatingSerializer(serializers.ModelSerializer):
    """Rating serial"""

    class Meta:
        model = Rating
        fields = ('user', 'serial', 'rate')

    def create(self, validated_data):
        rating = Rating.objects.update_or_create(
            user=validated_data.get('user', None),
            serial=validated_data.get('serial', None),
            defaults={'rate': validated_data.get('rate')}
        )
        return rating


class SerialReviewSerializer(serializers.ModelSerializer):
    """Review serial"""

    class Meta:
        model = Review
        fields = "__all__"


class SerialDetailSerializer(serializers.ModelSerializer):
    """All info serial"""
    studio = serializers.SlugRelatedField(slug_field="name", read_only=True)
    genres = serializers.SlugRelatedField(slug_field="name", read_only=True, many=True)
    rating = SerialRatingSerializer(many=True)
    reviews = SerialReviewSerializer(many=True)

    class Meta:
        model = Serial
        fields = '__all__'
