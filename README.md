<h1 align="center">
  <br>
  <a href=""><img src="https://cdn.discordapp.com/attachments/861485353520726016/863401815516905512/discord_pfp_transparent.png" alt="Guren"></a>
  <br>
  BotMan - A Discord bot for Botchat, Moderation, Utilities, and other fun stuff.
  <br>
</h1>

# BotMan

A discord bot written by [Mahasvan](https://github.com/Mahas1) in python using the library [Discord.py](https://discordpy.readthedocs.io/en/latest/index.html#)
Don't use my code without crediting. You are free to host it and fork it yourself but don't claim any of my code as yours.


## If all you want is a stable instance of the bot, I'd recommend using my instance - [Link](https://discord.com/oauth2/authorize?client_id=845225811152732179&permissions=4294836215&scope=bot)
# Usage and installation

Download the repo as zip or do the following below in a terminal window:

```bash
sudo apt-get install git
git clone https://github.com/Code-Cecilia/BotMan.py
``` 
`cd` into the project's directory and run this command
```bash
python3 -m pip install -r requirements.txt
```
Get to the [developer page](https://discord.com/developers/applications) and make a new application.

![new application](./images/new_application.png)

![name the app](./images/name_app.png)

![add bot](./images/add_bot.png)

![copy token](./images/copy_token.png)

 Now that you have copied your token, paste it in `config.json` in its corresponding entry.

 ### Note: If you're going to host the bot in Repl.it, change the value of the `replit` key in config.json to "True"

A properly set-up config.json looks something like this

```json
{
  "prefix_list": ["bm-", "Bm-", "$"],
  "main_prefix": "bm-",
  "token": "ODQ4NTI5xxxxx._cvTBeEHbk1z6iTtCHY92TFN5DU",
  "replit": "True",
  "status_link": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
  "bio": "Hello! I am Botman, a bot written in Python by Mahasvan Mohan (github: Mahas1)."
}
```

You also need to enable Privileged gateway intents in the `Bot` section of your application's page

![image](https://user-images.githubusercontent.com/82939599/125238018-3eec9b00-e304-11eb-9fd8-efcac130d250.png)

The bot doesn't use prescence intents as of now, so feel free to disable it if you want. You need to enable the `Server Members Intent`, though.

# Setting up Reddit details

You're gonna need to setup an application for proper functioning of the Reddit Cog.

Go to [Reddit](https://www.reddit.com), and make a new account (or use the one you have.)

The first step you need to do is turn on dark mode, because that's what cool people do 😎

Now go to the [Reddit Applications page](https://www.reddit.com/prefs/apps/) 

If you already have an app, you'd see something like this

![reddit app page](./images/make_reddit_app.png)

If you don't have an app already, you'd see something like "Create an app"

What you need to do now, is to enter these details

 - Name - Enter a name for your application
 - Choose the `script` checkbox
 - set `about url` and `redirect url` as `https://localhost:8080` (if you know what you're doing, feel free to mess around.)
 - Click on `Create app`

![filling in the details](./images/filling_reddit_app_details.png)

Now, you'd see an entry for your application **above** the portion of the screen where you entered the details. (weird, I know.)

You can get the Client ID and Client Secret from these entries

![client id and secret](./images/getting_id_secret.png)

Fill in the details for your reddit appication in `reddit_details.json`.
 - `client_id` is the Client ID we got from the application (the one under the application name in the above screenshot)
 - `client_secret` is the Client Secret we got from the entry called `secret`
 - `username` is the username of the Reddit account you used to make the application
 - `password` is the password of the Reddit account you used to make the application

A properly set-up `reddit_details.json` looks something like this.

```json
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

 - Change the `replit` entry in the `config.json` to "True" - This can help you enable 24/7 functioning of your bot **without the premium plan**. (pretty cool, huh?)

 - Delete `requirements.txt` from the Repl's project files. It kind-of hindered the start function for me, and I don't know why.
You can add it later when the first boot is done, and the dependencies are installed automatically and the lock file is in place.
   
 - If you follow the above point, you'll find a few Cogs fail to load. If that is the case, install the dependencies one by one via the shell. Requests, AsyncPraw, and Prsaw need to be installed separately, as of the time I am writing this.

If you want the bot to function 24/7, you can follow these steps to enable this for free.

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

# Credits

[CorpNewt](https://github.com/corpnewt) for [CorpBot.py](https://github.com/corpnewt/CorpBot.py), from which I ~~stole~~ got the ideas of quite a few commands from.

[YuiiiPTChan](https://github.com/YuiiiPTChan0) for helping me with commands, and agreeing to work on the bot together.

[Discord.py](https://github.com/Rapptz/discord.py) for obvious reasons


And a **LOT** of friends who helped make this bot what it is today. Thanks, guys!



