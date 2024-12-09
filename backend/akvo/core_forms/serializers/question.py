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
from akvo.core_data.models import Answers
from akvo.utils.functions import get_node_sqlite_source


class ListQuestionSerializer(serializers.ModelSerializer):
    option = serializers.SerializerMethodField()
    type = serializers.SerializerMethodField()
    api = serializers.SerializerMethodField()
    rule = serializers.SerializerMethodField()
    extra = serializers.SerializerMethodField()
    fn = serializers.SerializerMethodField()
    dataApiUrl = serializers.SerializerMethodField()
    source = serializers.SerializerMethodField()
    disableDelete = serializers.SerializerMethodField()

    @extend_schema_field(ListOptionSerializer(many=True))
    def get_option(self, instance: Questions):
        if instance.type in [
            QuestionTypes.option,
            QuestionTypes.multiple_option
        ]:
            return ListOptionSerializer(
                instance=instance.question_options.all(), many=True
            ).data
        if instance.type == QuestionTypes.tree:
            return instance.tree_option
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

    @extend_schema_field(
        inline_serializer(
            'QuestionSourceFormat',
            fields={
                'file': serializers.CharField(),
                'parent': serializers.IntegerField(),
            }
        )
    )
    def get_source(self, instance: Questions):
        if not instance.type == QuestionTypes.cascade:
            return None
        # get node name from api endpoint
        cascade_url = instance.api.get("endpoint", None)
        source_file = get_node_sqlite_source(cascade_url=cascade_url)
        if not source_file:
            return None
        return {
            "file": source_file,
            "parent_id": 0
        }

    @extend_schema_field(serializers.BooleanField())
    def get_disableDelete(self, instance: Questions):
        answers = Answers.objects.filter(question=instance).count()
        if answers:
            return True
        return None

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
            "label",
            "short_label",
            "order",
            "type",
            "tooltip",
            "required",
            "dependency",
            "meta",
            "display_only",
            "rule",
            "api",
            "extra",
            "translations",
            "fn",
            "pre",
            "dataApiUrl",
            "option",
            "source",
            "disableDelete",
            "required_double_entry",
            "hidden_string",
            "limit",
            "columns",
            "addonBefore",
            "addonAfter",
        ]


class AddQuestionSerializer(serializers.Serializer):
    form = CustomIntegerField(read_only=True)
    question_group = CustomIntegerField(read_only=True)
    id = CustomIntegerField()
    name = CustomCharField()
    label = CustomCharField(required=False, allow_null=True)
    short_label = CustomCharField(required=False, allow_null=True)
    order = CustomIntegerField()
    type = CustomCharField()
    tooltip = CustomJSONField(required=False, allow_null=True)
    required = CustomBooleanField(
        required=False, allow_null=True, default=False)
    meta = CustomBooleanField(
        required=False, allow_null=True, default=False)
    display_only = CustomBooleanField(
        required=False, allow_null=True, default=False)
    rule = CustomJSONField(required=False, allow_null=True)
    dependency = CustomListField(required=False, allow_null=True)
    api = CustomJSONField(required=False, allow_null=True)
    extra = CustomListField(required=False, allow_null=True)
    fn = CustomJSONField(required=False, allow_null=True)
    dataApiUrl = CustomCharField(required=False, allow_null=True)
    translations = CustomListField(required=False, allow_null=True)
    option = AddOptionSerializer(many=True, required=False, allow_null=True)
    pre = CustomJSONField(required=False, allow_null=True)
    required_double_entry = CustomBooleanField(
        required=False, allow_null=True, default=False)
    hidden_string = CustomBooleanField(
        required=False, allow_null=True, default=None)
    limit = CustomIntegerField(required=False, allow_null=True, default=None)
    columns = CustomJSONField(required=False, allow_null=True)
    tree_option = CustomCharField(required=False, allow_null=True)
    addonBefore = CustomCharField(required=False, allow_null=True)
    addonAfter = CustomCharField(required=False, allow_null=True)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def to_internal_value(self, data):
        if isinstance(data.get("option"), str):
            data["tree_option"] = data["option"]
            data["option"] = []
        return super().to_internal_value(data)

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
            raise serializers.ValidationError({
                "message": validate_serializers_message(serializer.errors),
                "details": serializer.errors,
            })
        return value

    def create(self, validated_data):
        options_data = validated_data.pop("option", [])
        if not options_data:
            options_data = []
        qtype = validated_data.pop("type", None)
        validated_data["type"] = getattr(QuestionTypes, qtype)
        validated_data["data_api_url"] = validated_data.pop("dataApiUrl", None)
        validated_data["autofield"] = validated_data.pop("fn", None)
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
        # get question type
        qtype = validated_data.get('type', instance.type)
        qtype = getattr(QuestionTypes, qtype)
        # check if question type change
        if instance.type != qtype:
            answers = Answers.objects.filter(question=instance).count()
            if answers:
                raise serializers.ValidationError({
                    "message": "Can't update question type",
                    "details": f"Question {instance.id} has answers",
                })
        # update question
        instance.type = qtype
        instance.name = validated_data.get(
            'name', instance.name)
        instance.label = validated_data.get(
            'label', instance.label)
        instance.short_label = validated_data.get(
            'short_label', instance.short_label)
        instance.order = validated_data.get(
            'order', instance.order)
        instance.tooltip = validated_data.get(
            'tooltip', instance.tooltip)
        instance.required = validated_data.get(
            'required', instance.required)
        instance.meta = validated_data.get(
            'meta', instance.meta)
        instance.display_only = validated_data.get(
            'display_only', instance.display_only)
        instance.rule = validated_data.get(
            'rule', instance.rule)
        instance.dependency = validated_data.get(
            'dependency', instance.dependency)
        instance.api = validated_data.get(
            'api', instance.api)
        instance.extra = validated_data.get(
            'extra', instance.extra)
        instance.autofield = validated_data.get(
            'fn', instance.autofield)
        instance.data_api_url = validated_data.get(
            'dataApiUrl', instance.data_api_url)
        instance.translations = validated_data.get(
            'translations', instance.translations)
        instance.pre = validated_data.get(
            'pre', instance.pre)
        instance.required_double_entry = validated_data.get(
            'required_double_entry', instance.required_double_entry)
        instance.hidden_string = validated_data.get(
            'hidden_string', instance.hidden_string)
        instance.limit = validated_data.get(
            'limit', instance.limit)
        instance.columns = validated_data.get(
            'columns', instance.columns)
        instance.tree_option = validated_data.get(
            'tree_option', instance.tree_option)
        instance.addonBefore = validated_data.get(
            'addonBefore', instance.addonBefore)
        instance.addonAfter = validated_data.get(
            'addonAfter', instance.addonAfter)

        # check and delete options
        current_options = Options.objects.filter(question=instance).all()
        current_opt_ids = [co.id for co in current_options]

        new_option_data = validated_data.get('option', [])
        if not new_option_data:
            new_option_data = []
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
        instance.save()
        return instance
