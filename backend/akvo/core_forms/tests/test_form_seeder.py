import json

from io import StringIO

from django.test.utils import override_settings
from django.core.management import call_command
from django.test import TestCase

from akvo.core_forms.models import Forms
from akvo.core_forms.serializers.form import (
    FormDefinitionSerializer
)


@override_settings(USE_TZ=False)
class FormSeederTestCase(TestCase):
    def call_command(self, *args, **kwargs):
        out = StringIO()
        call_command(
            "form_seeder",
            *args,
            stdout=out,
            stderr=StringIO(),
            **kwargs,
        )
        return out.getvalue()

    def test_call_command(self):
        self.maxDiff = None
        forms = Forms.objects.all().delete()
        json_forms = [
            "IDH Form",
        ]

        # RUN SEED NEW FORM
        output = self.call_command("--file=./source/forms/1693403249322.json")
        output = list(filter(lambda x: len(x), output.split("\n")))
        forms = Forms.objects.all()
        self.assertEqual(forms.count(), 1)
        for form in forms:
            self.assertIn(
                f"Form Created | {form.name} V{form.version}", output
            )
            self.assertIn(form.name, json_forms)

        # RUN UPDATE EXISTING FORM
        output = self.call_command("--file=./source/forms/1693403249322.json")
        output = list(filter(lambda x: len(x), output.split("\n")))
        forms = Forms.objects.all()
        # form_ids = [form.id for form in forms]
        for form in forms:
            if form.version == 2:
                self.assertIn(
                    f"Form Updated | {form.name} V{form.version}", output
                )
            # FOR NON PRODUCTION FORM
            if form.version == 1:
                self.assertIn(
                    f"Form Created | {form.name} V{form.version}", output
                )
            self.assertIn(form.name, json_forms)

    def test_get_form_after_seed_return_expected_form_definition(self):
        self.call_command("--file=./source/forms/1693403249322.json")
        form = Forms.objects.filter(id=1693403249322).first()
        form_serializer = FormDefinitionSerializer(instance=form)
        form_definition = form_serializer.data
        # Load expected form definition from JSON
        with open('./source/static/expected_form_definition.json', 'r') as f:
            expected_form_definition = json.load(f)
        self.assertEqual(form_definition, expected_form_definition)
