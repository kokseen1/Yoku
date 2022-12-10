# Yoku

A minimal Yahoo! Auctions scraper deployed as a Telegram bot.

## Installation

```shell
pip install yoku
```

## Deployment

- Request a bot token from BotFather on Telegram.

- Ensure that the `YOKU_BOT_TOKEN` environment variable is set.

```shell
yoku
```

## Bot Usage

Add a query

```
/add <query>
```

Remove a query

```
/rm <query>
```

List queries

```
/ls
```

Fetch queries

```
/force
```
