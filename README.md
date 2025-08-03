# Honeypot-discord-bot
Honeypot bot, works with multiple server. 

> [!WARNING]
> The discord bot use .json
> Multiple servers require multiple settings.

## Dependencies
[Python ](https://www.python.org) versions 3.9+. Other versions and implementations may or may not work correctly.

[Discord.py](https://discordpy.readthedocs.io/en/stable/) ```pip install discord.py```

## Installation
Clone the github project
```
git clone https://github.com/froyln/honeypot-discord-bot/
```
Open .env
```
cd simple-honeypot-discord-bot
nano .env
```
Set bot token and prefix

## How to use 
> [!IMPORTANT]
> ! is the defauld prefix
> 
> if you changed it, use your own prefix

Add honeypot channel
```
!honeypot <channelId>
```
Remove honeypot channel
```
!disable_honeypot
```
Modify honeypot message
```
!honeypot_message <NewMessage>
```
Help
```
!help
```

## How works
When people send any message on #honeypot, bot bans the author message. 
