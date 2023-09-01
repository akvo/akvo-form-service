import requests

# from akvo.core_data.models import Answers
from akvo.core_forms.models import Questions
from akvo.core_forms.constants import QuestionTypes


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
        QuestionTypes.photo,
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
