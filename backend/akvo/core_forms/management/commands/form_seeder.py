import json
import os

from django.core.management import BaseCommand
from django.core.cache import cache

from akvo.core_forms.constants import QuestionTypes
from akvo.core_forms.models import (
    Forms, Questions, Options
)
from akvo.core_forms.models import QuestionGroups as QG


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument("-t",
                            "--test",
                            nargs="?",
                            const=1,
                            default=False,
                            type=int)
        parser.add_argument("-f", "--file", nargs="?", default=False, type=int)

    def handle(self, *args, **options):
        TEST = options.get("test")
        JSON_FILE = options.get("file")
        # Form source
        source_folder = "source/forms"
        source_files = [
            f"{source_folder}/{json_file}"
            for json_file in os.listdir(source_folder)
        ]
        source_files = list(filter(
            lambda x: "example" in x
            if TEST else "example" not in x, source_files
        ))
        if JSON_FILE:
            source_files = [f"{source_folder}{JSON_FILE}.json"]
        for source in source_files:
            json_form = open(source, 'r')
            json_form = json.load(json_form)
            form = Forms.objects.filter(id=json_form["id"]).first()
            if not form:
                form = Forms.objects.create(
                    id=json_form["id"],
                    name=json_form["form"],
                    description=json_form.get("description"),
                    version=json_form.get("form") or 1,
                    languages=json_form.get("languages"),
                    default_language=(
                        json_form.get("default_language") or "en"
                    ),
                    translations=json_form.get("translations"))
                if not TEST:
                    self.stdout.write(
                        f"Form Created | {form.name} V{form.version}")
            else:
                form.name = json_form["form"]
                form.version = json_form.get("form") or form.version + 1
                form.description = json_form.get("description")
                form.languages = json_form.get("languages")
                form.default_language = (
                        json_form.get("default_language") or
                        form.default_language
                    ),
                form.translations = json_form.get("translations")
                form.save()
                if not TEST:
                    self.stdout.write(
                        f"Form Updated | {form.name} V{form.version}")
            # question group loop
            for qg in enumerate(json_form["question_group"]):
                # TODO:: USE QG ID FROM JSON?
                question_group, created = QG.objects.update_or_create(
                    form=form,
                    name=qg["name"],
                    order=qg["order"],
                    repeatable=qg.get('repeatable') or False,
                    description=qg.get("description"),
                    translations=qg.get("translations"),
                    defaults={
                        "form": form,
                        "name": qg["name"],
                        "order": qg["order"],
                        "repeatable": qg.get('repeatable') or False,
                        "description": qg.get("description"),
                        "translations": qg.get("translations"),
                    })
                if created:
                    question_group.save()
                for q in enumerate(qg["question"]):
                    question = Questions.objects.filter(pk=q["id"]).first()
                    if not question:
                        question = Questions.objects.create(
                            form=form,
                            question_group=question_group,
                            id=q.get("id"),
                            name=q.get("name"),
                            tooltip=q.get("tooltip"),
                            order=q["order"],
                            meta=q.get("meta"),
                            rule=q.get("rule"),
                            required=q.get("required"),
                            dependency=q.get("dependency"),
                            api=q.get("api"),
                            type=getattr(QuestionTypes, q["type"]),
                            translations=q.get("translations"),
                            extra=q.get("extra"),
                            autofield=q.get("autofield"),
                        )
                    else:
                        question.name = q.get("name")
                        question.tooltip = q.get("tooltip")
                        question.order = q["order"]
                        question.meta = q.get("meta")
                        question.rule = q.get("rule")
                        question.required = q.get("required")
                        question.dependency = q.get("dependency")
                        question.type = getattr(QuestionTypes, q["type"])
                        question.api = q.get("api")
                        question.extra = q.get("extra")
                        question.translations = q.get("translations")
                        question.extra = q.get("extra"),
                        question.autofield = q.get("autofield")
                        question.save()
                    if q.get("options"):
                        Options.objects.filter(
                            question=question
                        ).all().delete()
                        Options.objects.bulk_create([
                            Options(
                                question=question,
                                code=o.get("code"),
                                name=o["name"].strip(),
                                order=o["order"],
                                translations=o.get("translations")
                            ) for o in enumerate(q.get("options"))
                        ])
        # DELETE CACHES AND REFRESH MATERIALIZED DATA
        cache.clear()
