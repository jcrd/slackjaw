# slackjaw

slackjaw is a [Slack][slack] app with [Bitbucket][bitbucket] integration.

[slack]: https://slack.com/
[bitbucket]: https://bitbucket.org/

## Features

* Posts reminders of unanswered Pull Request comments on Bitbucket.

## Setup

slackjaw requires set up with both Bitbucket and Slack.

First, clone this repository and enter its directory:

```sh
git clone https://github.com/jcrd/slackjaw
cd slackjaw
```

Then, rename `.env-template`:

```sh
mv .env-template .env
```

This file contains the variables needed to run slackjaw.

### Bitbucket

slackjaw requires a Bitbucket app password. Follow [these][app-password] instructions
to create one.

Add the necessary permissions:

* Account (Read)
* Repositories (Read)
* Pull requests (Read)

Copy the generated password to the `BITBUCKET_PASSWORD` variable in the `.env` file.
Set the `BITBUCKET_USERNAME` variable to your username.

Finally, set the `BITBUCKET_WORKSPACE` variable to the name of the workspace to be scanned for unanswered comments.

[app-password]: https://support.atlassian.com/bitbucket-cloud/docs/app-passwords/

### Slack

slackjaw requires setting up a Slack app for your workspace. Follow [these][slack-app] instructions.

Add the necessary scopes:

* `chat:write.public`, which will include the `chat:write` scope

Make sure to install the app to your workspace.

Copy the *Bot User OAuth Token* to the `SLACK_BOT_TOKEN` variable in the `.env` file.

Finally, navigate to the Slack channel to receive the unanswered comments reminders and copy its **Channel ID** to the `SLACK_CHANNEL_ID` variable.

[slack-app]: https://api.slack.com/authentication/basics

### Schedule

slackjaw posts its unanswered comments reminder once daily at the time specified by the `SCHEDULE_TIME` variable in `.env`. It must be in the format: `%H:%M`, where:

* `%H` denotes the hour (range [0, 23])
* `%M` denotes the minute (range [0, 59])

## Running

Once the above set up instructions have been completed, install slackjaw's
dependencies with:

```sh
pip install -r requirements.txt
```

Then, run slackjaw:

```sh
python -m slackjaw
```

### Docker

A `Dockerfile` is available for running slackjaw in a container which includes
dependencies.

Build and run the container:

```sh
docker build -t slackjaw .
docker run -d slackjaw
```

## License

This project is licensed under the MIT License (see [LICENSE](LICENSE)).
