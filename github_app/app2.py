import os
import openai
import requests

from flask import Flask, request
from github import Github, GithubIntegration


app = Flask(__name__)
# app_idを記入
app_id = 324665
# 秘密鍵の読み取り
with open("./private-key.pem") as cert_file:
    app_key = cert_file.read()

# GitHub integrationのインスタンスを作成
integration = GithubIntegration(
    app_id,
    app_key,
)

# @app.route("/")
# def index():
#     return "Hello, world!"


@app.route("/", methods=['POST'])
def bot():
    payload = request.get_json()
    # print(payload)
    keys = payload.keys()
    if payload['action'] == 'opened' or payload['action'] == 'reopened':
        if "issue" in keys:
            installation_id = payload['installation']['id']
            repo_full_name = payload['repository']['full_name']
            issue_number = payload['issue']['number']
            user = payload['issue']['user']['login']

            access_token = integration.get_access_token(installation_id).token
            github = Github(access_token)

            repo = github.get_repo(repo_full_name)
            issue = repo.get_issue(issue_number)

            issue.create_comment('Hello, @{}!'.format(user))
        elif "pull_request" in keys:
            installation_id = payload['installation']['id']
            repo_full_name = payload['repository']['full_name']
            pull_request_number = payload['pull_request']['number']
            user = payload['pull_request']['user']['login']
            
            # Githubのアクセストークンを設定
            access_token = integration.get_access_token(installation_id).token
            github = Github(access_token)

            repo = github.get_repo(repo_full_name)
            pull_request = repo.get_pull(pull_request_number)

            # プルリクエストのコードを取得
            diff = pull_request.get_files()[0].patch

            # OpenAI APIを用いてレビュー生成
            #openai.api_key=os.environ["OPENAI_API_KEY"]
            openai.api_key="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"
            # question= f"Please review the following code in Japanese.:\n{diff}\nReview:"
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "user", "content": "大谷翔平について教えて"},
                ],
            )
            #print(response)
            review = response.choices[0]["message"]["content"]
            pull_request.create_issue_comment(review)
        
    return "ok"

#おまじない
if __name__ == "__main__":
    app.run(debug=True, port=5000)