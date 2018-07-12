# Strava Telegram Bot

A simple Strava bot using Stravlib & Telegram for fetching and calculating statistics. It's ready to be deployed on Heroku as well.

## Getting Started

Create _config.json_ inside _scripts/_ in the below format:

```
{
  "ATHLETES": {
    "TELEGRAM_USERNAME_1": "ATHLETE'S_STRAVA_TOKEN",
    "TELEGRAM_USERNAME_2": "ATHLETE'S_STRAVA_TOKEN"
  },
  "ADMIN_USER_NAME": "@TELEGRAM_USERNAME",
  "SHADOW_MODE": true/false,
  "SHADOW_MODE_CHAT_ID": "TELEGRAM_CHAT_ID"
}
```

### Prerequisites

1. pip
2. stravalib
3. python-telegram-bot
4. pycrypto

```
$ apt-get install python-pip
$ pip install stravalib
$ pip install python-telegram-bot
$ pip install pycrypto
```

## License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/panchambharadwaj/strava-telegram-bot/blob/master/LICENSE) file for details