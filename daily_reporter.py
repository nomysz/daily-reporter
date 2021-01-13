from random import choice, shuffle
from jira_client import get_issues, build_jql
from config import *
from rephrazer import rephrase
from slack_client import post_blocks
from utils import it_got_a_chance, jira_issue_was_created_today


notes_options = [
    "-",
    "---",
    "None",
    "Nothing so far",
    "👌",
]

status_options_shared = [
    "• <{link}|{key}>: busy with{type} {summary}",
    "• <{link}|{key}>: working on{type} {summary}",
    "• <{link}|{key}>: dealing with{type} {summary}",
    "• <{link}|{key}>: solving{type} {summary}",
    "• <{link}|{key}>: preparing {summary}",
    "• <{link}|{key}>: hope to work on{type} {summary}",
    "• <{link}|{key}>: no issues with{type} {summary}",
    "• <{link}|{key}>: {summary}",
    "• <{link}|{key}>:",
]

status_options_yesterday = status_options_shared + [
    "• <{link}|{key}>: worked on{type} {summary}",
    "• <{link}|{key}>: spent some time on{type} {summary}",
]

status_options_today = status_options_shared + [
    "• <{link}|{key}>: will be working on{type} {summary}",
    "• <{link}|{key}>: will be dealing with{type} {summary}",
    "• <{link}|{key}>: will be solving{type} {summary}",
    "• <{link}|{key}>: doing{type} {summary}",
    "• <{link}|{key}>: doing {summary}",
]


def map_issue_type(issue) -> str:
    if it_got_a_chance():
        return ''
    original_type = str(issue.fields.issuetype).lower()
    if original_type in ['podzadanie', 'story']:
        return choice([' task', ' issue'])
    return choice([' task', ' issue', ' bug'])


def render_summary(issue) -> str:
    if it_got_a_chance(.5):
        return issue.fields.summary.lower()
    return rephrase(issue.fields.summary).lower()


def get_blocks(issues: list) -> list:
    shuffle(status_options_today)
    shuffle(issues)
    today_text = "\n".join(
        [
            status_options_today[i].format(
                key=f'{issue.key}',
                type=f'{map_issue_type(issue)}',
                summary=render_summary(issue),
                link=f'{JIRA_SERVER_URI}/browse/{issue.key}',
            )
            for i, issue in enumerate(issues)
        ]
    )

    shuffle(status_options_yesterday)
    shuffle(issues)

    for i, issue in enumerate(issues):
        if jira_issue_was_created_today(issue):
            issues.pop(i)

    if len(issues) >= 2 and it_got_a_chance(.1):
        issues.pop()

    yesterday_text = " \r\n ".join(
        [
            status_options_yesterday[i].format(
                key=f'{issue.key}',
                type=f'{map_issue_type(issue)}',
                summary=render_summary(issue),
                link=f'{JIRA_SERVER_URI}/browse/{issue.key}',
            )
            for i, issue in enumerate(issues)
        ]
    )

    blocks = [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "*Before:*"
            }
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": yesterday_text
            }
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "*Today:*"
            }
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": today_text
            }
        },
    ]

    if it_got_a_chance(.3):
        blocks.extend([
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "*Notes:*"
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": choice(notes_options)
                }
            }
        ])

    return blocks


if __name__ == "__main__":
    issues = get_issues(jql=build_jql())
    print(f'Found {str(len(issues))} issues')

    blocks = get_blocks(issues)
    print('Generated blocks\n', blocks)

    post_blocks(blocks=blocks)
    print(f'Published to slack!')
