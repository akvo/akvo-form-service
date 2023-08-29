from django.db import models

# Create your models here.
from api.core.core_forms.constants import QuestionTypes


class Form(models.Model):
    name = models.TextField()
    description = models.TextField()
    version = models.IntegerField(default=1)
    languages = models.JSONField(default=None, null=True)
    translations = models.JSONField(default=None, null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "form"


class QuestionGroup(models.Model):
    form = models.ForeignKey(
        to=Form,
        on_delete=models.CASCADE,
        related_name="form_question_group"
    )
    name = models.TextField()
    description = models.TextField()
    order = models.BigIntegerField(null=True, default=None)
    repeatable = models.BooleanField(default=False)
    translations = models.JSONField(default=None, null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "question_group"


class Question(models.Model):
    form = models.ForeignKey(
        to=Form,
        on_delete=models.CASCADE,
        related_name="form_question"
    )
    question_group = models.ForeignKey(
        to=QuestionGroup,
        on_delete=models.CASCADE,
        related_name="question_group_question",
    )
    name = models.TextField()
    order = models.BigIntegerField(null=True, default=None)
    type = models.IntegerField(choices=QuestionTypes.FieldStr.items())
    tooltip = models.TextField()
    required = models.BooleanField(default=True)
    meta = models.BooleanField(default=False)
    rule = models.JSONField(default=None, null=True)
    dependency = models.JSONField(default=None, null=True)
    api = models.JSONField(default=None, null=True)
    extra = models.JSONField(default=None, null=True)
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
        db_table = "question"


class Option(models.Model):
    question = models.ForeignKey(
        to=Question,
        on_delete=models.CASCADE,
        related_name="question_question_option"
    )
    name = models.TextField()
    order = models.BigIntegerField(null=True, default=None)
    translations = models.JSONField(default=None, null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "option"
