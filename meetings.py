#Init
import discord
from discord.ext import commands
import asyncio

class Meetings(commands.Cog):
    def __init__(self, client, ah):
        self.client = client
        self.ah = ah

    @commands.command(name='meetings', description="Lists defined meetings")
    async def meetings(self, context):
        fetch = self.ah.list_meetings(context.message.author.id)
        #await context.message.channel.send(ah.list_meetings(context.message.author.id))
        Embed = discord.Embed(title="Your account", description="--------------------", color=0x00ff80)
        Embed.set_author(name="Meetings")
        for meet in fetch:
            Embed.add_field(name=meet[1], value=meet[2], inline=False)
        Embed.set_footer(text="ID: " + str(context.message.author.id))
        await context.message.channel.send(embed=Embed)

        # /setupmeeting - command
    @commands.command(name='setupmeeting', description="Setup meeting")
    async def setupmeeting(self, context):
        user_id = context.message.author.id #Store id

        #Enter name
        await context.message.channel.send("**Enter the name of the meeting:**")
        def check(m):
            return m.author == context.message.author
        try:
            name = await self.client.wait_for('message', check=check, timeout=60.0)
            meeting_name = name.content #Store name
            if self.ah.check_if_meeting_exists(meeting_name, user_id) == True:
                await context.message.channel.send("Sorry, there already is a meeting with that name.")
                return await context.message.channel.send("You can update your meetings with: **!updatemeeting**.")
        except asyncio.TimeoutError:
                return await context.message.channel.send('Sorry, you took too long.')
        
        #Enter link
        await context.message.channel.send("**Enter the link (FORMAT: https://meet.google.com/xxx-xxx-xxx):**")
        try:
            link = await self.client.wait_for('message', check=check, timeout=60.0)
            meeting_link = link.content #Store link
        except asyncio.TimeoutError:
                return await context.message.channel.send('Sorry, you took too long.')

        #Enter time
        await context.message.channel.send("**Enter the duration: (FORMAT: 100s or 45m or 1h)(minimum: 1minute, maximum: 3hours)**")
        try:
            time = await self.client.wait_for('message', check=check, timeout=60.0)
            meeting_time = time.content.split(' ') #Store time
            count = 0
            for x in meeting_time:
                #print("x:", x)
                x = x.lower()
                try:
                    if "s" in x:
                        count += int(x.replace("s", "").replace("seconds", "").replace("secs", ""))
                    elif "m" in x:
                        count += int(x.replace("m", "").replace("minutes", "").replace("mins", ""))*60
                    elif "h" in x:
                        count += int(x.replace("h", "").replace("hours", "").replace("hrs", ""))*3600
                except:
                    return await context.message.channel.send('Invalid format!')
                #print("count:", count)
            #print("finalcount:", count)
            if count < 60:
                return await context.message.channel.send('The duration cannot be less than 60 seconds.')
            elif count > 10800:
                return await context.message.channel.send('The duration cannot be more than 3 hours.')
        except asyncio.TimeoutError:
                return await context.message.channel.send('Sorry, you took too long.')

        self.ah.register_meeting(user_id, meeting_name, meeting_link, count) #Store in db
        await context.message.channel.send("Successfully registered the details of the meeting!")



    @commands.command(name='updatemeeting', description="Updates a defined meeting")
    async def updatemeeting(self, context):
        fetch = self.ah.list_meetings(context.message.author.id)
        #await context.message.channel.send(ah.list_meetings(context.message.author.id))
        Embed = discord.Embed(title="Choose a meeting to update:", description="--------------------", color=0x00ff80)
        Embed.set_author(name="Meetings")
        numbers = 1
        number_checker = []
        meetings = []
        links = []
        for meet in fetch:
            Embed.add_field(name=str(numbers) + " - " + meet[1], value=str(numbers) + " - " + meet[2], inline=False)
            meetings.append(meet[1])
            links.append(meet[2])
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
            return await context.message.channel.send('Updateing canceled!')
        try:
            meetingnr = int(meetingnr)-1
        except:
            return await context.message.channel.send('Updateing canceled, **next time please specify a number!**')
        if meetingnr+1 not in number_checker:
            return await context.message.channel.send('Updateing canceled, **invalid number!**')

        #await context.message.channel.send(meetings[meetingnr])
        await context.message.channel.send("Do you want to update the name(1) or link(2)?")
        try:
            choice = await self.client.wait_for('message', check=check, timeout=60.0)
            choicenr = choice.content
        except asyncio.TimeoutError:
            return await context.message.channel.send('Sorry, you took too long.')
        try:
            choicenr = int(choicenr)
        except:
            return await context.message.channel.send('Updateing canceled, **invalid choice!**')
        if choicenr < 1 or choicenr > 2:
            return await context.message.channel.send('Updateing canceled, **invalid choice!**')
        elif choicenr == 1:
            await context.message.channel.send("Please enter the new name:")
            try:
                new_name = await self.client.wait_for('message', check=check, timeout=60.0)
                new_name = new_name.content
            except asyncio.TimeoutError:
                return await context.message.channel.send('Sorry, you took too long.')
            self.ah.update_meeting_name(context.message.author.id, new_name, links[meetingnr])
        elif choicenr == 2:
            await context.message.channel.send("Please enter the new link:")
            try:
                new_link = await self.client.wait_for('message', check=check, timeout=60.0)
                new_link = new_link.content
            except asyncio.TimeoutError:
                return await context.message.channel.send('Sorry, you took too long.')
            self.ah.update_meeting_name(context.message.author.id, meetings[meetingnr], new_link)
        return await context.message.channel.send('Successfully updated! :)')

    @commands.command(name='deletemeeting', description="Delete a defined meeting")
    async def deletemeeting(self, context):
        fetch = self.ah.list_meetings(context.message.author.id)
        #await context.message.channel.send(ah.list_meetings(context.message.author.id))
        Embed = discord.Embed(title="Choose a meeting to delete:", description="--------------------", color=0x00ff80)
        Embed.set_author(name="Meetings")
        numbers = 1
        number_checker = []
        meetings = []
        links = []
        for meet in fetch:
            Embed.add_field(name=str(numbers) + " - " + meet[1], value=str(numbers) + " - " + meet[2], inline=False)
            meetings.append(meet[1])
            links.append(meet[2])
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
            return await context.message.channel.send('Deleteing canceled!')
        try:
            meetingnr = int(meetingnr)-1
        except:
            return await context.message.channel.send('Deleteing canceled, **next time please specify a number!**')
        if meetingnr+1 not in number_checker:
            return await context.message.channel.send('Deleteing canceled, **invalid number!**')

        