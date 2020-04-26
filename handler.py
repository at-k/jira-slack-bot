import json
import requests
from threading import Thread

class DonburiHandler:
    def __init__(self, donburi_jira, token, team_id):
        self.donburi_jira = donburi_jira
        self.slack_verification_token = token
        self.slack_team_id = team_id

    # json format: {owners: { memer: { slack: xx, jira:xx } } }
    def init_member_info(self, file_name):
        with open(file_name) as f:
            self.members = json.load(f)
        return True

    def slackid_to_jirauser(self, slack_id):
        for m in self.members['owners']:
            if self.members['owners'][m]['slack'] == str(slack_id):
                return  self.members['owners'][m]['jira']
        return ""

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

    def create_issue(self, slack_user, epic_id, labels, summary, description, response_url):
        jira_user = self.slackid_to_jirauser(slack_user)

        thread = Thread(target=self._create_issue,
                kwargs={
                    'reporter': jira_user,
                    'epic_id': epic_id,
                    'labels': labels,
                    'summary': summary,
                    'description': description,
                    'webhook_url': response_url
                    })
        thread.start()

        return True

    def _create_issue(self, reporter, epic_id, labels, summary, description, webhook_url):
        issue = self.donburi_jira.create_issue(reporter, summary, description)
        print(issue)

        if epic_id != "":
            self.donburi_jira.add_to_epic(issue, epic_id)

        if isinstance(labels, list):
            self.donburi_jira.add_labels(issue, labels)

        if webhook_url != "":
            body = f"{jira_url}/browse/{issue.key}"
            respond_to_slack(webhook_url, body)

        return True

    def search_issues(self, epic_id, labels, assignee_slack_id="", response_url):
        jira_user = self.slackid_to_jirauser(assignee_slack_id) if assignee_slack_id != "" else ""

        thread = Thread(target=self._search_issues,
                kwargs={
                    'assignee': jira_user,
                    'epic_id': epic_id,
                    'labels': labels,
                    'webhook_url': response_url
                    })
        thread.start()

        return True

    def _search_issues(self, epic_id, labels, assignee, webhook_url):

        # issues = self.donburi_jira.

        if webhook_url != "":
            body = f"{jira_url}/browse/{issue.key}"
            respond_to_slack(webhook_url, body)

        return True
