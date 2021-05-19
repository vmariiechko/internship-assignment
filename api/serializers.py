from rest_framework import serializers
from .models import SMS


class SMSListSerializer(serializers.ModelSerializer):
    """
    Serializer for listing SMSes with all data.
    """

    # Convert author id to his username
    author = serializers.CharField(source='author.username')

    class Meta:
        model = SMS
        fields = ('id', 'author', 'message', 'views_count')


class SMSDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for single SMS data.
    """

    class Meta:
        model = SMS
        fields = ('message', 'views_count')
