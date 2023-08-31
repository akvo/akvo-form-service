from django.db import models

# Create your models here.
from akvo.core_forms.constants import QuestionTypes


class Forms(models.Model):
    name = models.TextField()
    description = models.TextField(default=None, null=True)
    version = models.IntegerField(default=1)
    languages = models.JSONField(default=None, null=True)
    default_language = models.CharField(
        max_length=255, null=True, default=None
    )
    translations = models.JSONField(default=None, null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "forms"


class QuestionGroups(models.Model):
    form = models.ForeignKey(
        to=Forms,
        on_delete=models.CASCADE,
        related_name="question_groups"
    )
    name = models.TextField()
    description = models.TextField(default=None, null=True)
    order = models.BigIntegerField(null=True, default=None)
    repeatable = models.BooleanField(default=False)
    translations = models.JSONField(default=None, null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "question_groups"


class Questions(models.Model):
    form = models.ForeignKey(
        to=Forms,
        on_delete=models.CASCADE,
        related_name="questions"
    )
    question_group = models.ForeignKey(
        to=QuestionGroups,
        on_delete=models.CASCADE,
        related_name="question_group_questions",
    )
    name = models.TextField()
    order = models.BigIntegerField(null=True, default=None)
    type = models.IntegerField(choices=QuestionTypes.FieldStr.items())
    tooltip = models.JSONField(default=None, null=True)
    required = models.BooleanField(default=True)
    meta = models.BooleanField(default=False)
    rule = models.JSONField(default=None, null=True)
    dependency = models.JSONField(default=None, null=True)
    api = models.JSONField(default=None, null=True)
    extra = models.JSONField(default=None, null=True)
    autofield = models.JSONField(default=None, null=True)
    translations = models.JSONField(default=None, null=True)

    def __str__(self):
        return self.name

    def to_definition(self):
        options = ([
            options.name for options in self.question_question_option.all()
        ] if self.question_question_option.count() else False)
        return {
            "id": self.id,
            "question_group": self.question_group.id,
            "order": self.order,
            "name": self.name,
            "type": QuestionTypes.FieldStr.get(self.type),
            "tooltip": self.tooltip,
            "required": self.required,
            "meta": self.meta,
            "rule": self.rule,
            "dependency": self.dependency,
            "api": self.api,
            "extra": self.extra,
            "options": options,
            "translations": self.translations,
        }

    @property
    def to_excel_header(self):
        return f"{self.id}|{self.name}"

    class Meta:
        db_table = "questions"


class Options(models.Model):
    question = models.ForeignKey(
        to=Questions,
        on_delete=models.CASCADE,
        related_name="question_options"
    )
    code = models.CharField(max_length=255, null=True, default=None)
    name = models.TextField()
    order = models.BigIntegerField(null=True, default=None)
    translations = models.JSONField(default=None, null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "options"
