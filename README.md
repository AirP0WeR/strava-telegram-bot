# Strava Telegram Bot

A simple Strava bot using Telegram for fetching and calculating statistics.

## Getting Started

Create _config.json_ inside _scripts/_ in the below format:

```
{
  "ENVIRONMENT": "DEV/PROD",
  "PROD_TELEGRAM_BOT_TOKEN": "PROD_TELEGRAM_BOT_TOKEN",
  "DEV_TELEGRAM_BOT_TOKEN": "DEV_TELEGRAM_BOT_TOKEN",
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
2. requests
3. dateutil
4. python-telegram-bot

```
$ apt-get install python-pip
$ pip install requests
$ pip install python-dateutil
$ pip install python-telegram-bot
```

## License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/panchambharadwaj/strava-telegram-bot/blob/master/LICENSE) file for details