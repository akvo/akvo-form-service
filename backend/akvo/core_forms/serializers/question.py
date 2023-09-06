from collections import OrderedDict

from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema_field, inline_serializer
from rest_framework import serializers

from akvo.core_forms.constants import QuestionTypes
from akvo.core_forms.models import (
    Questions,
    Options
)
from akvo.core_forms.serializers.option import (
    ListOptionSerializer,
    AddOptionSerializer,
)
from akvo.utils.custom_serializer_fields import (
    CustomIntegerField,
    CustomCharField,
    CustomJSONField,
    CustomListField,
    CustomBooleanField,
)
from akvo.utils.custom_serializer_fields import validate_serializers_message


class ListQuestionSerializer(serializers.ModelSerializer):
    option = serializers.SerializerMethodField()
    type = serializers.SerializerMethodField()
    api = serializers.SerializerMethodField()
    rule = serializers.SerializerMethodField()
    extra = serializers.SerializerMethodField()
    fn = serializers.SerializerMethodField()
    dataApiUrl = serializers.SerializerMethodField()

    @extend_schema_field(ListOptionSerializer(many=True))
    def get_option(self, instance: Questions):
        if instance.type in [
            QuestionTypes.option,
            QuestionTypes.multiple_option
        ]:
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
            "QuestionExtraFormat",
            fields={"allowOther": serializers.BooleanField()}
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

    @extend_schema_field(OpenApiTypes.STR)
    def get_dataApiUrl(self, instance: Questions):
        return instance.data_api_url

    def to_representation(self, instance):
        result = super(
            ListQuestionSerializer, self
        ).to_representation(instance)
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
            "dataApiUrl",
            "option",
        ]


class AddQuestionSerializer(serializers.Serializer):
    form = CustomIntegerField(read_only=True)
    question_group = CustomIntegerField(read_only=True)
    id = CustomIntegerField()
    name = CustomCharField()
    order = CustomIntegerField()
    type = CustomCharField()
    tooltip = CustomJSONField(required=False, allow_null=True)
    required = CustomBooleanField(
        required=False, allow_null=True, default=False)
    meta = CustomBooleanField(
        required=False, allow_null=True, default=False)
    rule = CustomJSONField(required=False, allow_null=True)
    dependency = CustomListField(required=False, allow_null=True)
    api = CustomJSONField(required=False, allow_null=True)
    extra = CustomListField(required=False, allow_null=True)
    autofield = CustomJSONField(required=False, allow_null=True)
    data_api_url = CustomCharField(required=False, allow_null=True)
    translations = CustomListField(required=False, allow_null=True)
    option = AddOptionSerializer(many=True, required=False, allow_null=True)

    def __init__(self, *args, **kwargs):
        # Get the value
        data_api_url = kwargs.pop('dataApiUrl', None)
        autofield = kwargs.pop('fn', None)
        super(AddQuestionSerializer, self).__init__(*args, **kwargs)
        # Set the value
        if data_api_url:
            self.fields['data_api_url'].initial = data_api_url
        if autofield:
            self.fields['autofield'].initial = autofield

    def validate_type(self, value):
        qtype = getattr(QuestionTypes, value)
        if not qtype:
            raise serializers.ValidationError("Invalid question type")
        return value

    def validate_option(self, value):
        if not value:
            return None
        serializer = AddOptionSerializer(data=value, many=True)
        if not serializer.is_valid():
            print('OPT ERROR', serializer.errors)
            raise serializers.ValidationError({
                "message": validate_serializers_message(serializer.errors),
                "details": serializer.errors,
            })
        return value

    def create(self, validated_data):
        options_data = validated_data.pop("option", [])
        qtype = validated_data.pop("type", None)
        validated_data["type"] = getattr(QuestionTypes, qtype)
        q = Questions.objects.create(**validated_data)
        for opt in options_data:
            serializer = AddOptionSerializer(data=opt)
            if not serializer.is_valid():
                raise serializers.ValidationError({
                    "message": validate_serializers_message(serializer.errors),
                    "details": serializer.errors,
                })
            serializer.save(question=q)
        return q

    def update(self, instance, validated_data):
        # update question
        instance.name = validated_data.get(
            'name', instance.name)
        instance.order = validated_data.get(
            'order', instance.order)
        instance.type = validated_data.get(
            'type', instance.type)
        instance.tooltip = validated_data.get(
            'tooltip', instance.tooltip)
        instance.required = validated_data.get(
            'required', instance.required)
        instance.meta = validated_data.get(
            'meta', instance.meta)
        instance.rule = validated_data.get(
            'rule', instance.rule)
        instance.dependency = validated_data.get(
            'dependency', instance.dependency)
        instance.api = validated_data.get(
            'api', instance.api)
        instance.extra = validated_data.get(
            'extra', instance.extra)
        instance.autofield = validated_data.get(
            'autofield', instance.autofield)
        instance.data_api_url = validated_data.get(
            'data_api_url', instance.data_api_url)
        instance.translations = validated_data.get(
            'translations', instance.translations)

        # check and delete options
        current_options = Options.objects.filter(question=instance).all()
        current_opt_ids = [co.id for co in current_options]

        new_option_data = validated_data.get('option', [])
        new_opt_ids = [no.get('id') for no in new_option_data]

        for opt in new_option_data:
            current_opt = Options.objects.filter(id=opt.get('id')).first()
            serializer = AddOptionSerializer(data=opt)
            if not serializer.is_valid():
                raise serializers.ValidationError({
                    "message": validate_serializers_message(serializer.errors),
                    "details": serializer.errors,
                })
            if not current_opt:
                serializer.save(question=instance)
            if current_opt:
                serializer.update(
                    instance=current_opt,
                    validated_data=serializer.validated_data)

        missing_opt_ids = list(set(current_opt_ids) - set(new_opt_ids))
        # delete old options then create new
        Options.objects.filter(id__in=missing_opt_ids).delete()

        return instance
