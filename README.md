# Yoku

A minimal Yahoo! Auctions scraper deployed as a Telegram bot.

## Installation

```shell
pip install yoku
```

## Deployment

- Request a token from [BotFather](https://t.me/botfather) on Telegram.

- Set the `YOKU_BOT_TOKEN` environment variable to that token.

Run with:

```shell
yoku
```

To run in the background (Linux):

```shell
nohup yoku &
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
