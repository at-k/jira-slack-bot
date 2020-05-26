# -*- coding: utf-8 -*-
import json
import os
import random
import logging
import requests
import traceback
from jira import JIRA

def init_jira(server, project, user, api_key):
    options = {'server': server}

    jira = JIRA(options, basic_auth=(user, api_key))

    return jira



if __name__ == '__main__':
    # get params from env
    user = os.environ["JIRA_USER"]
    token = os.environ["JIRA_API_KEY"]
    # slack_webhook_url = os.environ["SLACK_WEBHOOK_URL"]
    slack_webhook_url = ""

    jira_url = 'https://jira-freee.atlassian.net/'
    issue_url_base = jira_url + 'browse/'
    jira_project = 'DONBURI'

    jira = init_jira(jira_url, jira_project, user, token)

    # epic & subtask以外の未完
    issues = jira.search_issues("project = DONBURI AND "
                                "(\"Epic Link\" = 障害対応 OR labels in (\"donburi_troubleshoot\"))  AND "
                                "labels != ask_SRE AND "
                                "resolution = Unresolved AND "
                                "issuetype != 'Sub-task' AND issuetype != 'Epic'")
                                # "duedate < 7d")

    # taskに未完のsubtaskあればリストに挙げる
    for issue in issues:

        issue_url = issue_url_base + issue.key
        print(f"* [{issue.key}]({issue_url}) : {issue.fields.summary}")
        if not hasattr(issue.fields, 'subtasks'):
            continue
        for subtask in issue.fields.subtasks:
            subtask_issue = jira.issue(subtask.key)
            if str(subtask_issue.fields.resolution) == 'Done':
                continue

            duedate = subtask_issue.fields.duedate if hasattr(subtask_issue.fields, 'duedate') else ""
            issue_url = issue_url_base + subtask_issue.key
            assignee = "unassigned"
            if hasattr(subtask_issue.fields.assignee, 'displayName'):
                assignee = subtask_issue.fields.assignee.displayName

            print(f"  * [{subtask_issue.key}]({issue_url}), {duedate}, {subtask_issue.fields.status}, {subtask_issue.fields.summary}, {assignee}")
