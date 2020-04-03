import json
import requests
from threading import Thread

class DonburiHandler:
    def __init__(self, jira, token, team_id):
        self.jira = jira
        self.slack_verification_token = token
        self.slack_team_id = team_id

    def init_member_info(self, file_name):
        with open(file_name) as f:
            self.members = json.load(f)
        return True

    def slackid_to_jirauser(self, slack_id):
        return self.members[slack_id]

    def respond_to_slack(self, webhook_url, body):
        payroad = {
            "text": body,
            "response_type": "in_channel",
            # "response_type": "ephemeral",
            # "delete_original": "true"
        }
        return requests.post(webhook_url, data=json.dumps(payroad))

    def is_request_valid(self, request):
        is_token_valid = request.form['token'] == self.slack_verification_token
        is_team_id_valid = request.form['team_id'] == self.slack_team_id
        return is_token_valid and is_team_id_valid

    def create_issue(self, response_url):
        return True
