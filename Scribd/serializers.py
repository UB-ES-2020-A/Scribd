from rest_framework import serializers

from Scribd.models import ebook


class ebookSerializer(serializers.ModelSerializer):
    class Meta:
        model = ebook
        fields = ('id', 'title', 'autor', 'size', 'media_type', 'count_downloads')
