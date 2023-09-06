from collections import OrderedDict

from rest_framework import serializers

from akvo.core_forms.models import Options
from akvo.utils.custom_serializer_fields import (
    CustomIntegerField,
    CustomCharField,
    CustomListField
)


class ListOptionSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        result = super(ListOptionSerializer, self).to_representation(instance)
        return OrderedDict(
            [(key, result[key]) for key in result if result[key] is not None]
        )

    class Meta:
        model = Options
        fields = ["id", "code", "name", "order", "color", "translations"]


class AddOptionSerializer(serializers.Serializer):
    question = CustomIntegerField(read_only=True)
    id = CustomIntegerField()
    name = CustomCharField()
    order = CustomIntegerField()
    code = CustomCharField(required=False, allow_null=True)
    color = CustomCharField(required=False, allow_null=True)
    translations = CustomListField(required=False, allow_null=True)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def create(self, validated_data):
        opt = Options.objects.create(**validated_data)
        return opt

    def update(self, instance, validated_data):
        instance.name = validated_data.get(
            'name', instance.name)
        instance.order = validated_data.get(
            'order', instance.order)
        instance.code = validated_data.get(
            'code', instance.code)
        instance.color = validated_data.get(
            'color', instance.color)
        instance.translations = validated_data.get(
            'translations', instance.translations)
        instance.save()
        return instance
