from rest_framework import serializers

from akvo.core_forms.models import Forms


class ListFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = Forms
        fields = [
            "id", "name", "description", "default_language",
            "languages", "version", "translations"
        ]
