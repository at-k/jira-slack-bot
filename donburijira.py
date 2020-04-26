from jira import JIRA

class DonburiJira:
    def __init__(self, server, project, auth_user, auth_key):
        self.project = project
        self.issue_url_base = server.rstrip("/") + '/browse/'
        self.jira = JIRA({'server': server}, basic_auth=(auth_user, auth_key))

    def create_issue(self, account_id, summary, description, issuetype='Task'):
        issue = self.jira.create_issue(project=self.project,
                                      summary=summary,
                                      description=description,
                                      assignee={'accountId': account_id},
                                      issuetype={'name': issuetype})
        return issue

    def add_to_epic(self, issue, epic_id):
        epic = self.jira.issue(epic_id)
        if epic == None:
            return False

        # add ticket to epic
        self.jira.add_issues_to_epic(epic_id=epic_id, issue_keys=[issue.key])

        # take over labels from epic
        labels = epic.fields.labels
        issue.fields.labels.extend(labels)
        issue.update(fields={"labels": issue.fields.labels})
        return True

    def add_labels(self, issue, labels):
        tmp_labels = issue.fields.labels + labels
        issue.update(fields={"labels": tmp_labels})

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

    def epiced_issues(self, epic_name, createdDate='-60d'):
        query = f"project = {self.project} AND " \
                f"\"Epic Link\" = {epic_name} AND " \
                f"createdDate > {createdDate}"
        return self.search_issues(query)

    def print_issues(self, issues):
        for issue in issues:
            url = self.issue_url_base + issue.key
            labels = issue.fields.labels
            if issue.fields.assignee is not None:
                assignee = issue.fields.assignee.displayName
            else:
                assignee = "None"
            summary = issue.fields.summary
            status = issue.fields.status
            resolution = issue.fields.resolution
            print(f"{url}, {labels}, {assignee}, {summary}, {resolution}")

    def list_unlabeled_issues(self, issues, exclude_label):
        marked_issues = []
        for issue in issues:
            labels = issue.fields.labels
            if len(labels) == 0 or (len(labels) == 1 and labels[0] == exclude_label):
                marked_issues.append(issue)
        return marked_issues

