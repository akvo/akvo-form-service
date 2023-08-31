from io import StringIO

from django.test.utils import override_settings
from django.core.management import call_command
from django.test import TestCase

from akvo.core_forms.models import Forms


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
            "TOILET AND HANDWASHING FACILITY OUTCOMES",
        ]

        # RUN SEED NEW FORM
        output = self.call_command("--file=1691495283921")
        output = list(filter(lambda x: len(x), output.split("\n")))
        forms = Forms.objects.all()
        self.assertEqual(forms.count(), 1)
        for form in forms:
            self.assertIn(
                f"Form Created | {form.name} V{form.version}", output
            )
            self.assertIn(form.name, json_forms)

        # RUN UPDATE EXISTING FORM
        output = self.call_command()
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
