from rest_framework import serializers
from .models import SMS


class SMSListSerializer(serializers.ModelSerializer):
    """Serializer for listing all SMSes with full data."""

    # Convert author id to his username
    author = serializers.CharField(source='author.username')

    class Meta:
        model = SMS
        fields = ('id', 'author', 'message', 'views_count')


class SMSDetailSerializer(serializers.ModelSerializer):
    """Serializer for single SMS information."""

    class Meta:
        model = SMS
        fields = ('message', 'views_count')
