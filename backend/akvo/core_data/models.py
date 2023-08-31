import requests
from django.db import models

# Create your models here.
from akvo.core_forms.models import (
    Forms, Questions, QuestionTypes
)


class AnswerManager(models.Manager):
    def define_answer_value(self, data, answer):
        name = None
        value = None
        option = None
        if answer.get("question").type in [
            QuestionTypes.geo,
            QuestionTypes.option,
            QuestionTypes.multiple_option,
        ]:
            option = answer.get("value")
        elif answer.get("question").type in [
            QuestionTypes.input,
            QuestionTypes.text,
            QuestionTypes.photo,
            QuestionTypes.date,
        ]:
            name = answer.get("value")
        elif answer.get("question").type == QuestionTypes.cascade:
            val = None
            id = answer.get("value")
            ep = answer.get("question").api.get("endpoint")
            ep = ep.split("?")[0]
            ep = f"{ep}?id={id}"
            val = requests.get(ep).json()
            val = val[0].get("name")
            name = val
        else:
            # for number question type
            value = answer.get("value")
        answer_data = self.create(
            data=data,
            question=answer.get("question"),
            name=name,
            value=value,
            options=option,
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
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(default=None, null=True)

    objects = AnswerManager()

    def __str__(self):
        return self.data.name

    class Meta:
        db_table = "answers"
