# Strava Telegram Bot

A simple Strava bot using Telegram for fetching and calculating statistics.

## Getting Started

Create _config.json_ inside _scripts/_ in the below format:

```
{
  "ENVIRONMENT": "DEV/PROD",
  "PROD_TELEGRAM_BOT_TOKEN": "",
  "DEV_TELEGRAM_BOT_TOKEN": "",
  "ATHLETES": {
    "telegram_username": ""
  },
  "ADMIN_USER_NAME": "@telegram_username",
  "SHADOW_MODE": true/false,
  "SHADOW_MODE_CHAT_ID": "telegram_chat_id"
}
```

### Prerequisites

1. pip
2. requests
3. python-telegram-bot

```
$ apt-get install python-pip
$ pip install requests
$ pip install python-telegram-bot
```

## License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/panchambharadwaj/strava-telegram-bot/blob/master/LICENSE) file for details