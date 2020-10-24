from rest_framework import serializers

from Scribd.models import Ebook


class ebookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ebook
        fields = ('id', 'title', 'autor', 'size', 'media_type', 'count_downloads')
