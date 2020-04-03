from jira import JIRA

class DonburiJira:
    def __init__(self, server, project, auth_user, auth_key):
        self.project = project
        self.issue_url_base = server.rstrip("/") + '/browse/'
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

    def add_label(issue, label):
        issue.fields.labels.append(label)
        issue.update(fields={"labels": issue.fields.labels})

    def search_issues(self, query):
        issues = []
        block_size = 100
        idx = 0
        while True:
            issues_tmp = self.jira.search_issues(query, idx, block_size)
            if len(issues_tmp) == 0:
                break
            idx = idx + len(issues_tmp)
            issues = issues + issues_tmp
        return sorted(issues, key=lambda u: str(u.fields.assignee))

    def labeled_issues(self, label, resolution='Done', resolutiondate='-60d'):
        query = f"project = {self.project} AND " \
                f"labels in (\"{label}\") AND " \
                f"resolution = {resolution} AND " \
                f"status != \"Canceled\" AND " \
                f"resolutiondate > {resolutiondate}"
                #f"updatedDate > {updatedDate}"
        return self.search_issues(query)

    def print_issues(self, issues):
        for issue in issues:
            url = self.issue_url_base + issue.key
            labels = issue.fields.labels
            if issue.fields.assignee is not None:
                assignee = issue.fields.assignee.displayName
            else:
                assignee = "None"
            print(f"{url}, {labels}, {assignee}")

    def list_unlabeled_issues(self, issues, exclude_label):
        marked_issues = []
        for issue in issues:
            labels = issue.fields.labels
            if len(labels) == 0 or (len(labels) == 1 and labels[0] == exclude_label):
                marked_issues.append(issue)
        return marked_issues

