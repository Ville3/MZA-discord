#Init
import discord
from discord.ext import commands
import asyncio
#bot/bot.py
from bot.bot import google_meet

class Botcommands(commands.Cog):
    def __init__(self, client, ah):
        self.client = client
        self.ah = ah
    
    @commands.command(name='startnow', description="Starts a meeting session right away")
    async def startnow(self, context):
        fetch = self.ah.list_meetings(context.message.author.id)
        #await context.message.channel.send(ah.list_meetings(context.message.author.id))
        Embed = discord.Embed(title="Choose a meeting to start:", description="--------------------", color=0x00ff80)
        Embed.set_author(name="Meetings")
        numbers = 1
        number_checker = []
        meetings = []
        links = []
        times = []
        for meet in fetch:
            Embed.add_field(name=str(numbers) + " - " + meet[1], value=meet[2], inline=False)
            meetings.append(meet[1])
            links.append(meet[2])
            times.append(meet[3])
            number_checker.append(numbers)
            numbers += 1
        Embed.set_footer(text="ID: " + str(context.message.author.id))
        await context.message.channel.send(embed=Embed)
        await context.message.channel.send("*You can cancel with: 'cancel'*.")
        def check(m):
            return m.author == context.message.author
        try:
            meeting = await self.client.wait_for('message', check=check, timeout=60.0)
            meetingnr = meeting.content
        except asyncio.TimeoutError:
            return await context.message.channel.send('Sorry, you took too long.')
        if meetingnr == "cancel":
            return await context.message.channel.send('Meeting canceled!')
        try:
            meetingnr = int(meetingnr)-1
        except:
            return await context.message.channel.send('Meeting canceled, **next time please specify a number!**')
        if meetingnr+1 not in number_checker:
            return await context.message.channel.send('Meeting canceled, **invalid number!**')
        
        await context.message.channel.send("*Launching meeting: " + meetings[meetingnr] + ".*")
        session_id = self.ah.create_session(context.message.author.id, links[meetingnr], times[meetingnr])
        guild = context.message.guild
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            guild.me: discord.PermissionOverwrite(read_messages=True),
            guild.get_member(context.message.author.id): discord.PermissionOverwrite(read_messages=True)
        }

        channel = await guild.create_text_channel('Meetingid-' + str(session_id), overwrites=overwrites)
        self.ah.update_session(session_id, channel.id)
        details = self.ah.get_session(session_id)
        Embed = discord.Embed(title="Automatic meeting", description="------------------------", color=0x00ff80)
        Embed.set_author(name="This sessions ID: " + str(details['session_id']))
        Embed.add_field(name="Current channels ID: ", value=str(details['channel_id']), inline=False)
        Embed.add_field(name="Current meetings link: ", value=details['link'], inline=False)
        Embed.add_field(name="Current meetings duration: ", value=str(int(details['time'])/60) + " minutes", inline=False)
        Embed.set_footer(text="Your Discord User ID: " + str(details['discord_id']))
        await channel.send(embed=Embed)

        #Bot part
        #gm = google_meet(self.client, self.ah)
        await google_meet(self.client, self.ah, channel).joinmeet(details['discord_id'], details['link'], details['session_id'], int(details['time']))
        await channel.send("Testttt")

