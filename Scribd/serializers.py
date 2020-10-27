from rest_framework import serializers

from Scribd.models import Ebook


class ebookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ebook
        fields = '__all__'