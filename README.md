# stargaze-sales-bot
Stargaze Marketplace NFT Sales Tracker Discord Bot

## Overview
This is a free and open-source software that enables you to monitor NFT sales on the [Stargaze Marketplace](https://www.stargaze.zone/), receiving timely notifications about new sales on your Discord server.

Join for Free:

For NFT project founders, moderators, and creators, we invite you to deploy this application on your own servers at no cost. Simply follow the installation steps below.

Collaborate with Us:

Developers! We welcome you to join our community and contribute to this project. Together, we can create innovative tools that enhance the NFT experience.

![screenshot](resources/sale-notification.png)

## Requirements
1. Python: Please [install python](https://www.python.org/downloads/) in your development environment.
2. A discord webhook: This service will send sale notifications to a discord webhook, to show them in your discord server.  Please [create one](https://aidaform.com/help/how-to-create-a-discord-webhook.html) for the channel you want to display notifications.

## Running locally

### Clone this repository
```bash
$ git clone https://github.com/eleiton/stargaze-sales-bot.git
$ cd stargaze-sales-bot
````

### Create and activate a virtual environment for this service
```bash
$ python3 -m venv env
$ source env/bin/activate
````

### Install the required dependencies to run the service
```bash
$ pip3 install --upgrade pip
$ pip3 install -r requirements.txt
````

### Set the required environment variables
This service needs two environment variables:
1. The address of the NFT project you want to track sales for
2. The discord webhook url to be used to send notifications
```bash
$ export set COLLECTION_ADDRESS=<YOUR_STARS_ADDRESS> #example stars123abc
$ export set DISCORD_WEBHOOK=<WEBHOOK_URL> #example https://discord.com/api/webhooks/123/ABC
````

### Run the application
```bash
$ python3 main.py
````

## Deploying in production

Here are some options where you can deploy this bot, in no particular order:
1. [Koyeb](https://www.koyeb.com/)
2. [Render](https://render.com/)
3. [Heroku](https://heroku.com/)

