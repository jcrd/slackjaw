import logging
import os
import time

import schedule
from dotenv import load_dotenv

from .bitbucket import Workspace
from .slack import Bot


def main():
    logging.basicConfig(format="%(asctime)s %(message)s", level=logging.INFO)

    load_dotenv()

    sched_time = os.environ["SCHEDULE_TIME"]
    try:
        time.strptime(sched_time, "%H:%M")
    except ValueError:
        logging.error(f"Invalid SCHEDULE_TIME: {sched_time}")
        return

    ws = Workspace(
        os.environ["BITBUCKET_WORKSPACE"],
        os.environ["BITBUCKET_USERNAME"],
        os.environ["BITBUCKET_PASSWORD"],
    )
    bot = Bot(os.environ["SLACK_BOT_TOKEN"], os.environ["SLACK_CHANNEL_ID"])

    def post():
        logging.info("Posting message...")
        bot.post_unanswered_comments(ws.get_unanswered_comments())

    schedule.every().day.at(sched_time).do(post)

    logging.info("Running...")
    while True:
        schedule.run_pending()
        time.sleep(30)


if __name__ == "__main__":
    main()
