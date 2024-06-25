from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import serializers

from akvo.core_forms.models import (
    Forms, QuestionGroups, Questions
)
from akvo.core_forms.constants import QuestionTypes
from akvo.core_data.models import Data, Answers
from akvo.core_data.serializers.data import (
    SubmitDataSerializer,
    SubmitFormSerializer,
    ListDataSerializer
)
from akvo.core_data.serializers.answer import (
    SubmitDataAnswerSerializer,
    ListAnswerSerializer
)


class TestDataAndAnswerSerializers(TestCase):
    def setUp(self):
        self.client = APIClient()
        form_data = {
            "name": "Test Form",
            "description": "Lorem ipsum sit dolor",
            "version": 1,
            "languages": ["en"],
            "default_language": "en",
            "translations": None,
        }
        self.form = Forms.objects.create(**form_data)
        question_group_data = {
            "form": self.form,
            "name": "group_1",
            "label": "Group 1",
            "description": "Lorem ipsum sit dolor",
            "order": 1,
            "repeatable": False,
            "translations": None,
        }
        self.question_group = QuestionGroups.objects.create(
            **question_group_data
        )
        question_data = {
            "form": self.form,
            "question_group": self.question_group,
            "name": "name",
            "label": "Name",
            "order": 1,
            "type": QuestionTypes.input,
            "tooltip": "Lorem ipsum",
            "required": True,
            "meta": True,
            "rule": None,
            "dependency": None,
            "api": None,
            "extra": None,
            "autofield": None,
            "translations": None,
        }
        self.question = Questions.objects.create(**question_data)

    def test_submit_data_serializer(self):
        # no submitter
        invalid_post_data = {
            'name': 'Datapoint name',
            'geo': {'lat': 40.7128, 'lng': -74.0060},
            'submitter': None
        }
        serializer = SubmitDataSerializer(data=invalid_post_data)
        self.assertFalse(serializer.is_valid())
        with self.assertRaises(serializers.ValidationError):
            serializer.is_valid(raise_exception=True)
        # correct value
        post_data = {
            'name': 'Datapoint name',
            'geo': {'lat': 40.7128, 'lng': -74.0060},
            'submitter': 'Akvo'
        }
        serializer = SubmitDataSerializer(data=post_data)
        self.assertTrue(serializer.is_valid())

    def test_submit_data_answer_serializer(self):
        # wrong question id
        invalid_post_data = {
            'value': 'Lorem',
            'question': 100
        }
        serializer = SubmitDataAnswerSerializer(data=invalid_post_data)
        self.assertFalse(serializer.is_valid())
        with self.assertRaises(serializers.ValidationError):
            serializer.is_valid(raise_exception=True)
        # empty value
        invalid_post_data = {
            'value': None,
            'question': self.question.id
        }
        serializer = SubmitDataAnswerSerializer(data=invalid_post_data)
        self.assertFalse(serializer.is_valid())
        with self.assertRaises(serializers.ValidationError):
            serializer.is_valid(raise_exception=True)
        # wrong value
        invalid_post_data = {
            'value': ['Lorem'],
            'question': self.question.id
        }
        serializer = SubmitDataAnswerSerializer(data=invalid_post_data)
        self.assertFalse(serializer.is_valid())
        with self.assertRaises(serializers.ValidationError):
            serializer.is_valid(raise_exception=True)
        # correct value
        post_data = {
            'value': 'Lorem',
            'question': self.question.id
        }
        serializer = SubmitDataAnswerSerializer(data=post_data)
        self.assertTrue(serializer.is_valid())
        # correct value with repeat
        post_data = {
            'value': 'Lorem',
            'question': self.question.id,
            'repeat': 1,
        }
        serializer = SubmitDataAnswerSerializer(data=post_data)
        self.assertTrue(serializer.is_valid())

    def test_submit_form_serializer_and_get_data_answer(self):
        # submit
        post_data = {
            'name': 'Datapoint name',
            'geo': {'lat': 40.7128, 'lng': -74.0060},
            'submitter': 'Akvo'
        }
        post_answer = {
            'value': 'Lorem',
            'question': self.question.id
        }
        submit_data = {
            'data': post_data,
            'answer': [post_answer]
        }
        serializer = SubmitFormSerializer(
            data=submit_data, context={'form': self.form}
        )
        self.assertTrue(serializer.is_valid())
        serializer.save()
        # get data
        data = Data.objects.first()
        serializer = ListDataSerializer(instance=data)
        res = serializer.data
        expected_data = {
            'id': res.get('id'),
            'name': 'Datapoint name',
            'form': self.form.id,
            'geo': {'lat': 40.7128, 'lng': -74.0060},
            'submitter': 'Akvo',
            'created': res.get('created'),
            'updated': None
        }
        self.assertEqual(res, expected_data)
        # get answer
        answer = Answers.objects.first()
        serializer = ListAnswerSerializer(instance=answer)
        res = serializer.data
        expected_data = {
            'question': self.question.id,
            'value': 'Lorem',
            'repeat': 0,
        }
        self.assertEqual(res, expected_data)

    def test_submit_form_serializer_and_get_data_answer_with_repeat(self):
        # submit
        post_data = {
            'name': 'Datapoint name',
            'geo': {'lat': 40.7128, 'lng': -74.0060},
            'submitter': 'Akvo'
        }
        post_answer = {
            'value': 'Lorem',
            'question': self.question.id,
            'repeat': 1,
        }
        submit_data = {
            'data': post_data,
            'answer': [post_answer]
        }
        serializer = SubmitFormSerializer(
            data=submit_data, context={'form': self.form}
        )
        self.assertTrue(serializer.is_valid())
        serializer.save()
        # get data
        data = Data.objects.first()
        serializer = ListDataSerializer(instance=data)
        res = serializer.data
        expected_data = {
            'id': res.get('id'),
            'name': 'Datapoint name',
            'form': self.form.id,
            'geo': {'lat': 40.7128, 'lng': -74.0060},
            'submitter': 'Akvo',
            'created': res.get('created'),
            'updated': None
        }
        self.assertEqual(res, expected_data)
        # get answer
        answer = Answers.objects.first()
        serializer = ListAnswerSerializer(instance=answer)
        res = serializer.data
        expected_data = {
            'question': self.question.id,
            'value': 'Lorem',
            'repeat': 1,
        }
        self.assertEqual(res, expected_data)
