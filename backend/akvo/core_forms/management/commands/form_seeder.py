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
        parser.add_argument("-f", "--file", nargs="?", default=False, type=str)

    def handle(self, *args, **options):
        TEST = options.get("test")
        JSON_FILE = options.get("file")
        # Form source
        source_folder = "source/forms/"
        source_files = [
            f"{source_folder}/{json_file}"
            for json_file in os.listdir(source_folder)
        ]
        source_files = list(filter(
            lambda x: "example" in x
            if TEST else "example" not in x, source_files
        ))
        if JSON_FILE:
            source_files = [JSON_FILE]
        for source in source_files:
            json_form = open(source, 'r')
            json_form = json.load(json_form)
            form = Forms.objects.filter(id=json_form["id"]).first()
            if not form:
                form = Forms.objects.create(
                    id=json_form["id"],
                    name=json_form["name"],
                    description=json_form.get("description"),
                    version=json_form.get("form") or 1,
                    languages=json_form.get("languages") or ["en"],
                    default_language=(
                        json_form.get("defaultLanguage") or "en"
                    ),
                    translations=json_form.get("translations"))
                if not TEST:
                    self.stdout.write(
                        f"Form Created | {form.name} V{form.version}")
            else:
                form.name = json_form["name"]
                form.version = json_form.get("form") or form.version + 1
                form.description = json_form.get("description")
                form.languages = json_form.get("languages")
                form.default_language = (
                        json_form.get("defaultLanguage") or
                        form.default_language
                    ),
                form.translations = json_form.get("translations")
                form.save()
                if not TEST:
                    self.stdout.write(
                        f"Form Updated | {form.name} V{form.version}")
            # question group loop
            for qg in json_form["question_group"]:
                qgroup = QG.objects.filter(pk=qg.get("id")).first()
                if not qgroup:
                    qgroup = QG.objects.create(
                        id=qg["id"],
                        form=form,
                        name=qg["name"],
                        order=qg["order"],
                        repeatable=qg.get('repeatable') or False,
                        description=qg.get("description"),
                        translations=qg.get("translations")
                    )
                else:
                    qgroup.name = qg["name"],
                    qgroup.order = qg["order"],
                    qgroup.repeatable = (
                        qg.get('repeatable')
                        or qgroup.repeatable
                    ),
                    qgroup.description = qg.get("description"),
                    qgroup.translations = qg.get("translations"),
                # question loop
                for q in qg["question"]:
                    question = Questions.objects.filter(pk=q["id"]).first()
                    if not question:
                        question = Questions.objects.create(
                            form=form,
                            question_group=qgroup,
                            id=q.get("id"),
                            name=q.get("name"),
                            tooltip=q.get("tooltip"),
                            order=q["order"],
                            meta=q.get("meta") or False,
                            rule=q.get("rule"),
                            required=q.get("required") or False,
                            dependency=q.get("dependency"),
                            api=q.get("api"),
                            type=getattr(QuestionTypes, q["type"]),
                            translations=q.get("translations"),
                            extra=q.get("extra"),
                            autofield=q.get("fn"),
                            data_api_url=q.get("dataApiUrl")
                        )
                    else:
                        question.name = q.get("name")
                        question.tooltip = q.get("tooltip")
                        question.order = q["order"]
                        question.meta = q.get("meta") or False
                        question.rule = q.get("rule")
                        question.required = q.get("required") or False
                        question.dependency = q.get("dependency")
                        question.type = getattr(QuestionTypes, q["type"])
                        question.api = q.get("api")
                        question.extra = q.get("extra")
                        question.translations = q.get("translations")
                        question.extra = q.get("extra"),
                        question.autofield = q.get("fn")
                        question.data_api_url = q.get("dataApiUrl")
                        question.save()
                    # question options
                    if q.get("option"):
                        Options.objects.filter(
                            question=question
                        ).all().delete()
                        Options.objects.bulk_create([
                            Options(
                                id=o.get("id"),
                                question=question,
                                code=o.get("code"),
                                name=o["name"].strip(),
                                order=o["order"],
                                color=o.get("color"),
                                translations=o.get("translations")
                            ) for o in q.get("option")
                        ])
        # DELETE CACHES
        cache.clear()
