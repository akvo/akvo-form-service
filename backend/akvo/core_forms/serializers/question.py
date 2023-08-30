from collections import OrderedDict

from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema_field, inline_serializer
from rest_framework import serializers

from akvo.core_forms.constants import QuestionTypes
from akvo.core_forms.models import Questions
from akvo.core_forms.serializers.option import ListOptionSerializer


class ListQuestionSerializer(serializers.ModelSerializer):
    option = serializers.SerializerMethodField()
    type = serializers.SerializerMethodField()
    api = serializers.SerializerMethodField()
    rule = serializers.SerializerMethodField()
    extra = serializers.SerializerMethodField()
    fn = serializers.SerializerMethodField()

    @extend_schema_field(ListOptionSerializer(many=True))
    def get_option(self, instance: Questions):
        if instance.type in [QuestionTypes.option, QuestionTypes.multiple_option]:
            return ListOptionSerializer(
                instance=instance.question_options.all(), many=True
            ).data
        return None

    @extend_schema_field(OpenApiTypes.STR)
    def get_type(self, instance: Questions):
        return QuestionTypes.FieldStr.get(instance.type).lower()

    @extend_schema_field(
        inline_serializer(
            "CascadeApiFormat",
            fields={
                "endpoint": serializers.CharField(),
                "list": serializers.CharField(),
                "id": serializers.IntegerField(),
            },
        )
    )
    def get_api(self, instance: Questions):
        if instance.type == QuestionTypes.cascade:
            return instance.api
        return None

    @extend_schema_field(
        inline_serializer(
            "QuestionRuleFormat",
            fields={
                "min": serializers.FloatField(),
                "max": serializers.FloatField(),
                "allowDecimal": serializers.BooleanField(),
            },
        )
    )
    def get_rule(self, instance: Questions):
        return instance.rule

    @extend_schema_field(
        inline_serializer(
            "QuestionExtraFormat", fields={"allowOther": serializers.BooleanField()}
        )
    )
    def get_extra(self, instance: Questions):
        return instance.extra

    @extend_schema_field(
        inline_serializer(
            "QuestionAutofieldFormat",
            fields={
                "multiline": serializers.BooleanField(),
                "fnString": serializers.CharField(),
            },
        )
    )
    def get_fn(self, instance: Questions):
        return instance.autofield

    def to_representation(self, instance):
        result = super(ListQuestionSerializer, self).to_representation(instance)
        return OrderedDict(
            [(key, result[key]) for key in result if result[key] is not None]
        )

    class Meta:
        model = Questions
        fields = [
            "id",
            "name",
            "order",
            "type",
            "tooltip",
            "required",
            "dependency",
            "meta",
            "rule",
            "api",
            "extra",
            "translations",
            "fn",
            "option",
        ]