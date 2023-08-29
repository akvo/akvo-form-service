from django.db import models

# Create your models here.
from akvo.core_forms.constants import QuestionTypes
from akvo.core_forms.models import Forms, Questions


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

    @property
    def to_data_frame(self):
        data = {
            "id": self.id,
            "datapoint_name": self.name,
            "geolocation": f"{self.geo[0]}, {self.geo[1]}" if self.geo else None,
            "created_at": self.created.strftime("%B %d, %Y"),
            "updated_at": self.updated.strftime("%B %d, %Y") if self.updated else None,
        }
        for a in self.data_answer.order_by(
            "question__question_group_id", "question__order"
        ).all():
            data.update(a.to_data_frame)
        return data

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

    def __str__(self):
        return self.data.name

    @property
    def to_data_frame(self) -> dict:
        q = self.question
        qname = f"{self.question.id}|{self.question.name}"
        if q.type in [
            QuestionTypes.geo,
            QuestionTypes.option,
            QuestionTypes.multiple_option,
        ]:
            answer = "|".join(map(str, self.options))
        elif q.type in [QuestionTypes.text, QuestionTypes.photo, QuestionTypes.date]:
            answer = self.name
        else:
            answer = self.value
        return {qname: answer}

    class Meta:
        db_table = "answers"
