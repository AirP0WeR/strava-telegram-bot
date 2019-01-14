# Strava Telegram Bot

A simple Strava bot using Stravlib & Telegram for fetching and calculating statistics. It's ready to be deployed on Heroku as well.

### Prerequisites

1. pip
2. stravalib
3. python-telegram-bot
4. psycopg2-binary
5. requests

```
$ apt-get install python-pip
$ pip install stravalib
$ pip install python-telegram-bot
$ pip install psycopg2-binary
$ pip install requests
```

```
$ heroku addons:attach <database-app-name> -a <this-app-name>
```

## License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/panchambharadwaj/strava-telegram-bot/blob/master/LICENSE) file for details