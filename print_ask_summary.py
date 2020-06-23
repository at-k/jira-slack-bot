# -*- coding: utf-8 -*-
import os
import donburijira

# load param from env
auth_user = os.environ["JIRA_AUTH_USER"]
token = os.environ["JIRA_API_KEY"]
jira_server_url = os.environ["JIRA_SERVER_URL"]
jira_project_name = os.environ["JIRA_PROJECT_NAME"]

slack_verification_token = os.environ['SLACK_VERIFICATION_TOKEN']
slack_team_id = os.environ['SLACK_TEAM_ID']

debug_mode = True if 'DEBUG_MODE' in os.environ.keys() else False

# init modules
donburi = donburijira.DonburiJira(jira_server_url, jira_project_name, auth_user, token)

if __name__ == '__main__':
    issues = donburi.labeled_issues(label = "ask_SRE", resolutiondate='-80d')
    donburi.print_issues(issues)
