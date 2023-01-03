<div align="center">
<h1>Komi</h1>
<img alt="GitHub Repo stars" src="https://img.shields.io/github/stars/Kierstro/komi?style=social">
<img height="20" alt="Discord invite" src="https://discord.com/api/guilds/972183434522947584/widget.png">
<a href="https://github.com/Kierstro/komi/issues"><img alt="GitHub issues" src="https://img.shields.io/github/issues-raw/Kierstro/komi"></a>
<img alt="GitHub repo size" src="https://img.shields.io/github/repo-size/Kierstro/komi">
</div>
<br>
<img src="https://user-images.githubusercontent.com/38412336/182039655-f99324e5-0373-4573-b531-4f669f4ccd59.gif">
<br>
A simple Discord slash-command bot made using
<br>
<br>

* [`Hikari`](https://github.com/hikari-py/hikari) - An opinionated, static typed Discord microframework for Python3 and asyncio that supports Discord's V8 REST API and Gateway.
* [`Lightbulb`](https://github.com/tandemdude/hikari-lightbulb/) - A flexible command framework designed to extend Hikari.
<br>

Why slash-commands over prefixes? [Read me](https://discord.com/blog/welcome-to-the-new-era-of-discord-apps)

## Current Commands
Komi is a personal project however, I'm currently working on fleshing out the commands (*11/07/2022*).
<div align="center">
<img src="https://user-images.githubusercontent.com/38412336/178318058-f1a988ca-8209-4369-8e0c-8701b41f025f.png" />
</div>

## Prerequisites

You will need to configure the bot with the `static` files. This is needed to store some configuration data that is passed into the bot. The bot uses a few publicly available API (including Discord), it requires a token and api-key.
  * [Discord](https://discord.com/developers/applications)
  * [Steam](https://steamcommunity.com/dev)

## Using the bot
### Installation

1. Clone the repository
   ```sh
   git clone https://github.com/Kierstro/komi.git
   cd komi
   ```

2. Create a Virtual Enviroment and activate it
    ```sh
    python -m venv .venv
    source .venv/bin/activate
    ```

4. Install the required dependencies
   ```sh
   python -m pip install -r requirements.txt
   ```

5. Run the bot 
   ```sh
   chmod +x run.sh
   ./run.sh
   ```

