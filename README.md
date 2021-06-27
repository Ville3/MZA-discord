MZA is a discord bot which can be deployed to a server. It can attend your Google Meet and Zoom classes for you. You can define you're links with names, which you can later select from and will be stored onto the database for easy user experience.

It will:
1. Login with you're specified account
2. Go into the meet
3. Wait till the meet ends or if the people left early, leave with them

# Integration with discord
## Commands:
    !setupcredentials - Setups the credentials to your account via PM
    !changecredentials - Changes the credentials to your account via PM
    !credentials - Sends you the credentials to your account via PM
    !removecredentials - Removes the credentials from you're account
    !startnow - Starts a meeting session right away
    !meetings - Lists defined meetings
    !setupmeeting - Let's you define a link
    !updatemeeting - Updates a defined link with a new name
    !deletemeeting - Deletes a defined link
    !clear - Clears the chat, usage(Clears 10 lines): !clear 10

## The Discord bot

You can create you're own bot in [here](https://discord.com/developers/applications).
You will need to give the bot Privileged Intents permission before also when you invite the bot into a server.
You will need to enter the bot's token into main.py. When you're ready to launch the bot, run **main.py**.

# Work that needs to be done:
1. Zoom is not integrated yet.
2. Active meeting controls.
3. User permissions(All people in the server can right now use the bot, individually).
4. Voice recognition if anybody calls you're name in the meeting.
