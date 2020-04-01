from jira import JIRA
import os


class DonburiJira:
    def __init__(self, server, project, auth_user, auth_key):
        self.project = project
        self.jira = JIRA({'server': server}, basic_auth=(auth_user, auth_key))

    def create_issue(owner, summary, description, issuetype='Task'):
        account_id = self.jira.search_users(owner, maxResults=1)[0].accountId
        issue = self.jira.create_issue(project=self.project,
                                      summary=summary,
                                      description=description,
                                      assignee={'accountId': account_id},
                                      issuetype={'name': issuetype})
        return issue

    def add_to_epic(epic, issue):
        # add ticket to epic
        self.jira.add_issues_to_epic(epic_id=epic.id, issue_keys=[issue.key])

        # take over labels from epic
        labels = epic.fields.labels
        issue.fields.labels.extend(labels)
        issue.update(fields={"labels": issue.fields.labels})

    def search_issues(query):
        return self.jira.search_issues(query)



if __name__ == '__main__':
    # load param from env
    auth_user = os.environ["JIRA_AUTH_USER"]
    token = os.environ["JIRA_API_KEY"]
    jira_server_url = os.environ["JIRA_SERVER_URL"]
    jira_project_name = os.environ["JIRA_PROJECT_NAME"]
    issue_url_base = jira_url.rstrip("/") + '/browse/'

    # init jira
    donburi = DonburiJira(jira_server_url, jira_project_name, auth_user, token)

