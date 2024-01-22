import os

import requests


def load_template():
    return open('./templates/base.md', 'r').read()


def prepare_template(template, data_values):
    for key, value in data_values.items():
        if isinstance(value, list):
            template = template.replace("${0}".format(key), "\n".join([f"* {item}" for item in value]))
        else:
            template = template.replace("${0}".format(key), str(value))
    return template


def execute_request(url, method="GET"):
    user_bitbucket = "Mostela"
    password_bitbucket = os.getenv("BITBUCKET_PASSWORD")
    return requests.request(method=method, url=url, auth=(user_bitbucket, password_bitbucket))


def get_commits_pull_request(owner, repository, pr_id):
    return execute_request(
        url=f"https://api.bitbucket.org/2.0/repositories/{owner}/{repository}/pullrequests/{pr_id}/commits"
    ).json()["values"]


def get_tags_pull_request(owner, repository):
    return execute_request(
        url=f"https://api.bitbucket.org/2.0/repositories/{owner}/{repository}/refs/tags"
    ).json()["values"]


def get_pull_requests(owner, repository):
    response = execute_request(
        url=f"https://api.bitbucket.org/2.0/repositories/{owner}/{repository}/pullrequests?state=ALL")

    if response.status_code == 200:
        return response.json()['values']
    else:
        print(f"Falha ao obter pull requests. Código de status: {response.status_code}")
        print(response.text)
        return None


owner_repositorio = "Mostela"
name_repositorio = "mytwitter_backend"

if __name__ == "__main__":
    pull_requests = get_pull_requests(owner_repositorio, name_repositorio)
    last_tag = get_tags_pull_request(owner_repositorio, name_repositorio)[0]['name']
    for pr in pull_requests:
        print(f"Pull Request: {pr['title']}")
        commit_list = get_commits_pull_request(owner_repositorio, name_repositorio, pr['id'])
        print(commit_list)
    with open('./data/output.md', 'w') as output:
        output.write(prepare_template(load_template(), {"version_tag": last_tag,
                                                        "prs_url_list":
                                                            ["value", "value2"],
                                                        "repository_name": name_repositorio}))
        output.close()
