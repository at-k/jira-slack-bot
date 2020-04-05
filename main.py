# -*- coding: utf-8 -*-
from flask import abort, Flask, jsonify, request
import os
import shlex

import donburijira
import handler

# load param from env
auth_user = os.environ["JIRA_AUTH_USER"]
token = os.environ["JIRA_API_KEY"]
jira_server_url = os.environ["JIRA_SERVER_URL"]
jira_project_name = os.environ["JIRA_PROJECT_NAME"]

slack_verification_token = os.environ['SLACK_VERIFICATION_TOKEN']
slack_team_id = os.environ['SLACK_TEAM_ID']

# init modules
donburi = donburijira.DonburiJira(jira_server_url, jira_project_name, auth_user, token)
handler = handler.DonburiHandler(donburi, slack_verification_token, slack_team_id)
handler.init_member_info("./member.json")

# flask setup
app = Flask(__name__)
app.route('/waremado', methods=['POST'])
def waremado():
    if not handler.is_request_valid(request):
        abort(400)

    user_id = request.form['user_id']
    command = request.form['command']
    response_url = request.form['response_url']
    trigger_id = request.form['trigger_id']

    args = unidecode(request.form['text'])
    args = shlex.split(args)
    subcommand = args[0]

    text = ''

    if not handler.create_issue(response_url):
        abort(400)

    return jsonify(
        response_type='in_channel',
        text=text,
    )

# main
if __name__ == '__main__':
    # -- test jira
    # search issues
    # issues = donburi.labeled_issues(label = "ask_SRE", resolutiondate = '-90d')
    issues = donburi.epiced_issues(epic_name = u"割れ窓", createdDate = '-90d')
    donburi.print_issues(issues)
    # marked_issues = donburi.list_unlabeled_issues(issues, "ask_SRE")
    # donburi.print_issues(marked_issues)

    # start server
    # app.run()
