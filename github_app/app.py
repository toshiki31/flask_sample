import os
import requests

from flask import Flask, request
from github import Github, GithubIntegration

app = Flask(__name__)

with open('C:\\Users\\user\\OneDrive\\github\\flask-sample-bot-key.pem') as key:
    app_key = key.read()

app_id = 324665
git_integration = GithubIntegration(
    app_id,
    app_key,
)

@app.route("/", methods=["POST"])
def bot():
    payload = request.json

    owner = payload['repository']['owner']['login']
    repositoryName = payload['repository']['name']

    git_connection = Github(
        login_or_token=git_integration.get_access_token(
            git_integration.get_installation(owner, repositoryName).id
        ).token
    )
    repository = git_connection.get_repo(f"{owner}/{repositoryName}")
    repository.create_issue(
        title="test_issue",
        body="hello"
    )

    return "ok"

if __name__ == "__main__":
    app.run(debug=True, port=5000)