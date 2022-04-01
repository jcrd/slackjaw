from setuptools import setup

setup(
    name="slackjaw",
    version="0.1.0",
    packages=["slackjaw"],
    entry_points={
        "console_scripts": [
            "slackjaw = slackjaw.__main__:main",
        ],
    },
    install_requires=[
        "python-dotenv",
        "requests",
        "schedule",
        "slack_sdk",
    ],
    description="Slack app with Bitbucket integration",
    url="https://github.com/jcrd/slackjaw",
    license="MIT",
    author="James Reed",
    author_email="james@twiddlingbits.net",
)
