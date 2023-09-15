from django.db import models

# Create your models here.
from akvo.core_forms.models import (
    Forms, Questions
)
from akvo.utils.functions import (
    define_column_from_answer_value
)


class AnswerManager(models.Manager):
    def define_answer_value(self, data, answer):
        # define answer column
        name, value, option = define_column_from_answer_value(
            question=answer.get("question"), answer=answer
        )
        answer_data = self.create(
            data=data,
            question=answer.get("question"),
            name=name,
            value=value,
            options=option,
            repeat=answer.get("repeat", 0)
        )
        return answer_data


class Data(models.Model):
    form = models.ForeignKey(
        to=Forms,
        on_delete=models.CASCADE,
        related_name="data"
    )
    name = models.TextField()
    geo = models.JSONField(null=True, default=None)
    submitter = models.CharField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(default=None, null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "data"


class Answers(models.Model):
    data = models.ForeignKey(
        to=Data,
        on_delete=models.CASCADE,
        related_name="data_answers"
    )
    question = models.ForeignKey(
        to=Questions,
        on_delete=models.CASCADE,
        related_name="question_answers"
    )
    name = models.TextField(null=True, default=None)
    value = models.FloatField(null=True, default=None)
    options = models.JSONField(default=None, null=True)
    repeat = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(default=None, null=True)

    objects = AnswerManager()

    def __str__(self):
        return self.data.name

    class Meta:
        db_table = "answers"
