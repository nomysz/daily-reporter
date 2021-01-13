from datetime import date
from random import random


def it_got_a_chance(chance=.5):
    return bool(random() < chance)


def jira_issue_was_created_today(issue: dict) -> bool:
    date_string = issue.fields.created[0:10]
    date_list = date_string.split('-')

    return date(
        int(date_list[0]),
        int(date_list[1]),
        int(date_list[2])
    ) == date.today()
