#Init
import discord
from discord.ext import commands
import asyncio



class Credentials(commands.Cog):
    def __init__(self, client, ah):
        self.client = client
        self.ah = ah
    # /setupcredentials - command
    @commands.command(name='setupcredentials', description="Setups the credentials to your account")
    async def setupcredentials(self, context):
        if self.ah.check_if_user_exists(context.message.author.id) == True:
            await context.message.channel.send("Sorry, you already have entered the credentials to your account.")
            return await context.message.channel.send("You can change your credentials with: **!changecredentials**.")
        await context.message.channel.send("I messaged you!")
        await context.message.author.send("Your id: " + str(context.message.author.id))
        user_id = context.message.author.id #Store id

        #Enter email
        await context.message.author.send("**Enter your email:**")
        def check(m):
            return m.author == context.message.author
        try:
            email = await self.client.wait_for('message', check=check, timeout=60.0)
            user_email = email.content #Store email
        except asyncio.TimeoutError:
                return await context.message.author.send('Sorry, you took too long.')
        
        #Enter password
        await context.message.author.send("**Enter your password:**")
        try:
            password = await self.client.wait_for('message', check=check, timeout=60.0)
            user_password = password.content #Store password
        except asyncio.TimeoutError:
                return await context.message.author.send('Sorry, you took too long.')
        await context.message.author.send("Successfully recorded the credentials!")
        self.ah.add_user(user_id, user_email, user_password) #Store in db



    # /changecredentials - command
    @commands.command(name='changecredentials', description="Changes the credentials to your account")
    async def changecredentials(self, context):
        await context.message.channel.send("I messaged you!")
        #print embed
        details = self.ah.get_credentials_blurred(context.message.author.id)
        Embed = discord.Embed(title="Your account", description="--------", color=0x00ff80)
        Embed.set_author(name="Credentials")
        Embed.add_field(name="Email:", value=details['email'], inline=False)
        Embed.add_field(name="Password:", value=details['blur'], inline=False)
        Embed.set_footer(text="ID: " + str(context.message.author.id))
        await context.message.author.send(embed=Embed, delete_after=30.0)
        #print id
        #await context.message.author.send("Your id: " + str(context.message.author.id))
        user_id = context.message.author.id #Store id

        #Enter email
        await context.message.author.send("Enter your Google email:")
        def check(m):
            return m.author == context.message.author
        try:
            email = await self.client.wait_for('message', check=check, timeout=60.0)
            user_email = email.content #Store email
        except asyncio.TimeoutError:
                return await context.message.author.send('Sorry, you took too long.')
        
        #Enter password
        await context.message.author.send("Enter your password:")
        try:
            password = await self.client.wait_for('message', check=check, timeout=60.0)
            user_password = password.content #Store password
        except asyncio.TimeoutError:
                return await context.message.author.send('Sorry, you took too long.')
        await context.message.author.send("Successfully changed the credentials!")#, delete_after=3.0)
        self.ah.update_credentials(user_id, user_email, user_password) #Update in db

    # /credentials - command
    @commands.command(name='credentials', description="Sends you the credentials to your account")
    async def credentials(self, context):
        if self.ah.check_if_user_exists(context.message.author.id) == False:
            await context.message.channel.send("Looks like you havent setup your credentials.")
            return await context.message.channel.send("You can setup your credentials with: **!setupcredentials**.")
        await context.message.channel.send("I messaged you!")
        #print embed
        details = self.ah.get_credentials_blurred(context.message.author.id)
        Embed = discord.Embed(title="Your account", description="--------", color=0x00ff80)
        Embed.set_author(name="Credentials")
        Embed.add_field(name="Email:", value=details['email'], inline=False)
        Embed.add_field(name="Password:", value=details['blur'], inline=False)
        Embed.set_footer(text="ID: " + str(context.message.author.id))
        await context.message.author.send(embed=Embed, delete_after=30.0)
        await context.message.author.send("You can change your credentials with **!changecredentials**")

    # /removecredentials - command
    @commands.command(name='removecredentials', description="Removes the credentials from the server")
    async def removecredentials(self, context):
        self.ah.delete_credentials(context.message.author.id)
        await context.message.channel.send("Successfully deleted your credentials!")