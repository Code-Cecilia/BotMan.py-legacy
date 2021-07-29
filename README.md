# A Discord bot made with 💖and Python.

![BotMan Wallpaer Logo thing](./images/botman_logo.png)
###### If for some reason you wanted a low-effort BotMan wallpaper, you're welcome.

# BotMan

A discord bot written by [Mahasvan](https://github.com/Mahas1) in python using the library [Discord.py](https://discordpy.readthedocs.io/en/latest/index.html#).
Don't use my code without giving credit. You are free to host it and fork it yourself but don't claim any of this code as yours.


## If all you want is a stable instance of the bot, I'd recommend using my instance - [Link](https://discord.com/oauth2/authorize?client_id=845225811152732179&permissions=4294836215&scope=bot)
# Usage and installation

## GitHub Pages deployment for a better experience: [Link](https://code-cecilia.github.io/BotMan.py/)

### What we're gonna do
 - Download the repo's files
 - Get the Discord Bot Application's token (while setting the appropriate OAuth permissions)
 - Fill in the Reddit App details
 - Get the API key from RSA
 - Get the currency API key from ExchangeRatesAPI
 - Fill in details in `config.json` and `reddit_details.json`
 - Actually run the bot

Download the repo as zip or do the following below in a terminal window:

```bash
sudo apt-get install git
git clone https://github.com/Code-Cecilia/BotMan.py
``` 
`cd` into the project's directory and run this command
```bash
python3 -m pip install -r requirements.txt
```
Get to the [Discord Developer Portal](https://discord.com/developers/applications) and make a new application.

![new application](./images/new_application.png)

![name the app](./images/name_app.png)

![add bot](./images/add_bot.png)
You also need to enable Privileged gateway intents in the `Bot` section of your application's page

![image](https://user-images.githubusercontent.com/82939599/125238018-3eec9b00-e304-11eb-9fd8-efcac130d250.png)

The bot doesn't use prescence intents as of now, so feel free to disable it if you want. You need to enable the `Server Members Intent`, though.

![copy token](./images/copy_token.png)

 Now that you have copied your token, paste it in `config.json` in its corresponding entry.

# Getting the API key from the Random Stuff API

RSA (Random Stuff API) is what we use for BotChat in this bot. For this to work, we need to get an API Key.

You can get one [Here](https://api-info.pgamerx.com/register) by signing up with discord. It adds you to a server, and sends you a PM with the API key.

When you get it, set the value of `rsa_api_key` to the API key you recieved.

# Getting the currency API key from ExchangeRatesAPI

ExchangeRatesAPI is what this bot uses for working with currency.
You can get an API key [Here](https://exchangeratesapi.io/).

When you get the API key, copy and paste it into the `currency_api_key` entry in the `config.json` file.


A properly set-up config.json looks something like this

```javascript
{
  "prefix": "bm-",
  "token": "ODQ4NTI5xxxxx._cvTBeEHbk1z6iTtCHY92TFN5DU",
  "owner_id": "775176626773950474",
  "rsa_api_key": "XXXXXXXXXX",
  "currency_api_key": "XXXXXXXXXX"
}
```

`owner_id` is the ID of the owner (ie. you.). This is used for various owner-only commands
 
 - reload
 - reboot
 - shutdown

These are some of the owner-only commands available.

 ### Note: If you're going to host the bot in Repl.it, check the bottom of this page for extended information.

# Setting up Reddit details

You're gonna need to setup an application for proper functioning of the commands that use Reddit (nocontext, meme).

Go to [Reddit](https://www.reddit.com), and make a new account (or use the one you have.)

The first step you need to do is turn on dark mode, because that's what cool people do 😎

Now go to the [Reddit Applications page](https://www.reddit.com/prefs/apps/) 

If you already have an app, you'd see something like this

![reddit app page](./images/make_reddit_app.png)

You'd probably feel disappointed, cause the dark mode doesn't reflect in this page. (I know. I feel disappointed too.)

If you don't have an app already, you'd see something like "Create an app"

What you need to do now, is to enter these details

 - Name - Input any name for your application
 - Choose the `script` checkbox
 - set `about url` and `redirect url` as `https://localhost:8080` (It's what I do. If you know what you're doing, feel free to mess around.)
 - Click on `Create app`

![filling in the details](./images/filling_reddit_app_details.png)

Now, you'd see an entry for your application **above** the portion of the screen where you entered the details. (weird, I know.)

You can get the Client ID and Client Secret from these entries

![client id and secret](./images/getting_id_secret.png)

Fill in the details for your reddit application in `reddit_details.json`.
 - `client_id` is the Client ID we got from the application (the one under the application name in the above screenshot)
 - `client_secret` is the Client Secret we got from the entry called `secret`
 - `username` is the username of the Reddit account you used to make the application
 - `password` is the password of the Reddit account you used to make the application

A properly set-up `reddit_details.json` looks something like this.

```javascript
{
  "client_id" : "E3RXXXXXXXjlKzOg",
  "client_secret": "nEdXXXXXXXXXS_9tBYyo1Q",
  "username": "PrawBot12345",
  "password": "Praw1234"
}
```
(don't worry, the password is wrong)

And that should be it.
You can run `main.py` to run the bot. I'm working on a startup file, so bear with me till I finish it.

# Instructions for Repl.it

If you're going to host your bot on repl.it, these steps can be followed for features like 24/7 functioning without paying.

 - Change the `replit` variable in `main.py` from `False` to `True`.

```python
# previous lines
# status_link = details_data['status_link']

# owner_id = int(details_data['owner_id'])

replit = True   # change this to False or True depending on what you need

# intents = discord.Intents.default()
# continuing lines
```

 This enables 24/7 functioning of your bot **without the premium plan**. (pretty cool, huh?)

 - Delete `requirements.txt` from the Repl's project files, or rename it to something else for the first startup.
    It kind-of hindered the first setup for me, and I don't know why.
You can add it later when the first boot is done, and the dependencies are installed automatically and the lock file is in place.
   
 - If you follow the above point, you'll probably find a few Cogs fail to load. If that is the case, install the dependencies one by one via the shell. Requests, AsyncPraw, and Prsaw need to be installed separately, as of the time I am writing this.
 
- If Replit errors out while installing the dependencies from the lock file, remove modules that conflict. 

Continuation for 24/7 Replit functioning. You need to follow this step, or it won't work.

 - When you run your repl, you'll see a web view pop up. (top-right in most cases). You need to copy the URL of this page.
 - Make an account in [UptimeRobot](https://uptimerobot.com/)
 - add a new monitor with these credentials

        Monitor type: HTTP(S)
        Friendly Name : Whatever you want
        URL : The URL we copied earlier
        Monitoring Interval : I'd recommend setting it to 30 minutes, but you can go as low as 5 minutes for this.
    You don't need to change any other settings. Click on `Create Monitor` to create the monitor.
    
 ### So how does this work?
    
Good question.

Free Repls shut down (More like sleep) after 60 minutes of inactivity. So we ping the bot every [x] minutes to prevent the bot from shutting down.

That's pretty much it.
 You can select an alert email while making the UptimeRobot Monitor to notify you if the bot goes offline, but I don't really know how far it works, since I haven't tried it yet.

# Running the bot

1. Open up Command Prompt, Terminal, or what you have in your OS

2. (Very important) `cd` into the directory of the project. (if this is not done, it might break everything that uses the OS module, and maybe a few others)
```
cd [path to project folder]
```
3.  run this command
```
python3 main.py
```
4. Enjoy.

# Credits

[CorpNewt](https://github.com/corpnewt) for [CorpBot.py](https://github.com/corpnewt/CorpBot.py), from which I ~~stole~~ got the ideas of quite a few commands from.

[YuiiiPTChan](https://github.com/YuiiiPTChan0) for helping me with commands, and agreeing to work on the bot together.

[Discord.py](https://github.com/Rapptz/discord.py) for obvious reasons

[abhinavs](https://github.com/abhinavs/moonwalk) for the GitHub Pages theme


And a **LOT** of friends who helped make this bot what it is today. Thanks, guys!



