from config import (
    JIRA_SERVER_URI,
    JIRA_API_TOKEN_USER_EMAIL,
    JIRA_API_TOKEN,
    JIRA_PROJECT_KEY,
    JIRA_USER_EMAIL,
    JIRA_EXCLUDED_ISSUES,
    JIRA_CUSTOM_JQL,
    JIRA_FILTER_STATUSES
)
from jira import JIRA


def build_jql():
    excluded_issues_jql = ', '.join(
        [f'"{key}"' for key in JIRA_EXCLUDED_ISSUES]
    )
    statuses_jql = ', '.join(
        [f'"{status}"' for status in JIRA_FILTER_STATUSES]
    )
    return f'project = {JIRA_PROJECT_KEY} ' \
        f'AND assignee = "{JIRA_USER_EMAIL}" {JIRA_CUSTOM_JQL}' \
        f'AND key NOT IN ({excluded_issues_jql}) ' \
        f'AND status IN ({statuses_jql}) ' \
        'ORDER BY Rank ASC'


def get_issues(jql: str) -> list:
    return JIRA(
        JIRA_SERVER_URI,
        basic_auth=(JIRA_API_TOKEN_USER_EMAIL, JIRA_API_TOKEN)
    ).search_issues(
        jql,
        maxResults=10
    )
