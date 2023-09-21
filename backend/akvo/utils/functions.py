import re
import requests

from akvo.core_forms.models import Questions
from akvo.core_forms.constants import QuestionTypes
from akvo.core_node.models import Node


def update_date_time_format(date):
    if date:
        # date = timezone.datetime.strptime(date, "%Y-%m-%d").date()
        return date.date().strftime("%B %d, %Y")
    return None


def get_answer_value(
    answer, toString: bool = False, trans: list = None
):
    if answer.question.type in [
        QuestionTypes.geo,
        QuestionTypes.option,
        QuestionTypes.multiple_option,
    ]:
        ops = answer.options
        if ops and trans and answer.question.type != QuestionTypes.geo:
            ops = [
                (
                    list(
                        filter(
                            lambda t: t["key"] == op
                            and t["question"] == answer.question.id,
                            trans,
                        )
                    ),
                    op,
                )
                for op in ops
            ]
            ops = [
                o[0].pop().get("value", o[1]) if len(o[0]) else o[1]
                for o in ops
            ]
        if toString:
            return "|".join([str(o) for o in ops]) if ops else None
        return answer.options
    elif answer.question.type in [
        QuestionTypes.number,
        QuestionTypes.autofield
    ]:
        return answer.value
    else:
        return answer.name


def define_column_from_answer_value(question: Questions, answer: dict):
    name = None
    value = None
    option = None
    if question.type in [
        QuestionTypes.geo,
        QuestionTypes.option,
        QuestionTypes.multiple_option,
    ]:
        option = answer.get("value")
    elif question.type in [
        QuestionTypes.input,
        QuestionTypes.text,
        QuestionTypes.image,
        QuestionTypes.date,
    ]:
        name = answer.get("value")
    elif question.type == QuestionTypes.cascade:
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
    return name, value, option


def generate_node_filename(name: str):
    name = name.strip().lower()
    name = name.split(" ")
    name = "_".join(name)
    return name


def is_string_integer(value):
    pattern = r'^[+-]?\d+$'
    return bool(re.match(pattern, value))


def get_node_sqlite_source(cascade_url: str):
    if not cascade_url:
        return None
    node_id = cascade_url.split("/")[-1]
    source_file = node_id
    if is_string_integer(node_id):
        node_id = int(node_id)
        node = Node.objects.filter(pk=node_id).first()
        if not node:
            return None
        source_file = generate_node_filename(name=node.name)
    return f"{source_file}.sqlite"
