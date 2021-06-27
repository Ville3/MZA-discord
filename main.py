#Init
import discord
from discord.ext import commands
from pretty_help import PrettyHelp#, Navigation
import asyncio

#credentials.py
from credentials import Credentials
#misc.py
from misc import Miscellaneous
#meetings.py
from meetings import Meetings
#botcommands.py
from botcommands import Botcommands
#bot/bot.py
#from bot.bot import Meet_controls

#Sqlite
from accounts_handler import accounts_handler

#Init database
ah = accounts_handler()
ah.init_db()

#Bot prefix, other stuff
intents = discord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix='!', intents=intents)

# ":discord:743511195197374563" is a custom discord emoji format. Adjust to match your own custom emoji.
#nav = Navigation(":discord:743511195197374563", "👎", "\U0001F44D")
color = discord.Color.red()
client.help_command = PrettyHelp(color=color, active_time=10)#navigation=nav, color=color, active_time=10)

#Init discord
@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    await client.change_presence(status=discord.Status.do_not_disturb, activity=discord.Game('Google Meet'))


client.add_cog(Credentials(client, ah))

client.add_cog(Miscellaneous(client))

client.add_cog(Meetings(client, ah))

client.add_cog(Botcommands(client, ah))
#client.add_cog(Meet_controls(client, ah))



@client.command(name='test')
async def test(context):
    guild = context.message.guild
    overwrites = {
        guild.default_role: discord.PermissionOverwrite(read_messages=False),
        guild.me: discord.PermissionOverwrite(read_messages=True),
        guild.get_member(context.message.author.id): discord.PermissionOverwrite(read_messages=True)
    }

    channel = await guild.create_text_channel('secret', overwrites=overwrites)
    await channel.send(channel.id)



#Token
client.run('YOUR_BOT_TOKEN_HERE')