import logging

from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError


class Bot:
    def __init__(self, token, channel_id):
        self.client = WebClient(token=token)
        self.channel_id = channel_id

    def post(self, **kwargs):
        try:
            self.client.chat_postMessage(channel=self.channel_id, **kwargs)
        except SlackApiError as e:
            logging.error(e)

    def post_unanswered_comments(self, comments):
        if not comments:
            return

        blocks = []
        text = []

        i = len(comments)
        for user, cs in comments.items():
            txt = f"{user.name} has {len(cs)} unanswered comments in Bitbucket."
            text.append(txt)

            fields = []

            for comment in cs:
                pr = comment.pullrequest
                link_txt = f"{comment.id} @ {pr.title} (#{pr.id})"
                fields.append(
                    {
                        "type": "mrkdwn",
                        "text": f"<{comment.url}|{link_txt}>",
                    }
                )

            blocks.extend(
                [
                    {
                        "type": "section",
                        "text": {
                            "type": "plain_text",
                            "text": txt,
                        },
                    },
                    {
                        "type": "section",
                        "fields": fields,
                    },
                ]
            )

            i -= 1
            if i > 0:
                blocks.append({"type": "divider"})

        self.post(blocks=blocks, text="\n".join(text))
