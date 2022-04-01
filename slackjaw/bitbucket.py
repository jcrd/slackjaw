import re
from collections import namedtuple

import requests
from requests.auth import HTTPBasicAuth

User = namedtuple("User", ["id", "name"])
PullRequest = namedtuple("PullRequest", ["id", "title"])


class Auth:
    def __init__(self, username, password):
        self.auth = HTTPBasicAuth(username, password)

    def get(self, url):
        return requests.get(url, auth=self.auth).json()


class Comment:
    mention_regex = re.compile(r"@\{(\w+)\}")

    def __init__(self, pr, data):
        self.pullrequest = pr
        self.id = data["id"]
        self.parent_id = None

        if "parent" in data:
            self.parent_id = data["parent"]["id"]

        self.url = data["links"]["html"]["href"]
        self.author = data["user"]["account_id"]
        self.mentions = [
            m for m in Comment.mention_regex.findall(data["content"]["raw"])
        ]


class Workspace:
    url = "https://api.bitbucket.org/2.0/workspaces/{workspace}"

    def __init__(self, slug, *args):
        self.auth = Auth(*args)
        self.ws = self.auth.get(Workspace.url.format(workspace=slug))
        self.links = {n: d["href"] for n, d in self.ws["links"].items()}

    def get_link(self, url_id, path=[]):
        return self.get(self.links[url_id], path)

    def get(self, url, path=[]):
        while True:
            r = self.auth.get(url)
            for v in r["values"]:
                i = v
                for p in path:
                    i = i[p]
                yield i
            if "next" in r:
                url = r["next"]
            else:
                break

    def get_users(self):
        return {
            v["account_id"]: v["display_name"]
            for v in self.get_link("members", ["user"])
        }

    def get_unanswered_comments(self):
        users = self.get_users()
        prs_url = next(self.get_link("repositories", ["links", "pullrequests", "href"]))
        unanswered = {}

        for pr in self.get(prs_url):
            pullrequest = PullRequest(pr["id"], pr["title"])
            comments = []

            for c in self.get(pr["links"]["comments"]["href"]):
                c = Comment(pullrequest, c)
                comments.append(c)
                for user_id in c.mentions:
                    if user_id not in users:
                        continue
                    if user_id not in unanswered:
                        unanswered[user_id] = {}
                    unanswered[user_id][c.id] = c

            for c in comments:
                if not c.parent_id or c.author not in unanswered:
                    continue
                cs = unanswered[c.author]
                if c.parent_id in cs:
                    del cs[c.parent_id]

        r = {}

        for user_id, cs in unanswered.items():
            r[User(user_id, users[user_id])] = [c for c in cs.values()]

        return r
