from collections import OrderedDict

from rest_framework import serializers

from akvo.core_forms.models import Options


class ListOptionSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        result = super(ListOptionSerializer, self).to_representation(instance)
        return OrderedDict(
            [(key, result[key]) for key in result if result[key] is not None]
        )

    class Meta:
        model = Options
        fields = ["id", "code", "name", "order", "translations"]
