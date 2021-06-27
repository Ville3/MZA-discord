#Init
import discord
from discord.ext import commands, tasks
import asyncio, concurrent.futures

#from . import browser
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import os
import time
#import sys

#sys.path.append('../')
#misc.py
#from .misc import Miscellaneous, make_sleep

#def make_sleep():
#    async def sleep(delay, result=None, *, loop=None):
#        coro = asyncio.sleep(delay, result=result, loop=loop)
#        task = asyncio.ensure_future(coro)
#        sleep.tasks.add(task)
#        try:
#            return await task
#        except asyncio.CancelledError:
#            return result
#        finally:
#            sleep.tasks.remove(task)

#    sleep.tasks = set()
#    sleep.cancel_all = lambda: sum(task.cancel() for task in sleep.tasks)
#    return sleep

#async def wait_meeting(channel, time):
#    while True:
#        # do something
#        time_split = time/8
#        count = 0
#        sleep = make_sleep()
#        for x in range(len("12345678")):
#            if count % 2 == 0:
#                remaining_seconds = time_split*(8-x)
#                if remaining_seconds < 60:
#                    await channel.send("In " + str(remaining_seconds) + " seconds the meeting will end.")
#                else:
#                    await channel.send("In " + str(round(remaining_seconds/60)) + " minutes the meeting will end.")
#            await asyncio.sleep(time_split)

#usernameStr = "hhtr4444@gmail.com"
#passwordStr = "123123321321abCCC***"

#@run_async

class google_meet():#commands.Cog):
    def __init__(self, client, ah, channel):
        BROWSER_DRIVER = "bot/webdriver/geckodriver.exe"

        firefoxOptions = webdriver.FirefoxOptions()
        firefoxOptions.add_argument("--width=800"), firefoxOptions.add_argument("--height=800")
        #firefoxOptions.headless = True
        firefoxOptions.set_preference("general.useragent.override", "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:84.0) Gecko/20100101 Firefox/84.0")
        #firefoxOptions.set_preference("intl.accept_languages", 'en-us')
        firefoxOptions.set_preference("layers.acceleration.disabled", True)
        firefoxOptions.set_preference("browser.privatebrowsing.autostart", True)
        firefoxOptions.set_preference("permissions.default.microphone", 2)
        firefoxOptions.set_preference("permissions.default.camera", 2)
        self.browser = webdriver.Firefox(executable_path=BROWSER_DRIVER, options=firefoxOptions)
        self.client = client
        self.ah = ah
        self.channel = channel
        self.user_controls_enabled = True
        self.pool = concurrent.futures.ThreadPoolExecutor()

    @tasks.loop(seconds=10)
    async def user_controls(self, time):
        #if channel_id == self.channel.id:
        #    await self.channel.send("Channel id-s match!")
        #else:
        #    await self.channel.send("Channel id-s do not match!")
        #await self.channel.send("test")
        await self.channel.send("time: " + str(time))
        while self.user_controls_enabled:
            await asyncio.sleep(1)
            await self.channel.send("test")
        #return True

    async def joinmeet(self, discord_id, meet_link, session_id, time):

        fetch = self.ah.get_credentials(discord_id)
        usernameStr = fetch['email']
        passwordStr = fetch['password']
        await self.channel.send("*Logging in...*")
        self.browser.get('https://accounts.google.com/o/oauth2/auth/identifier?client_id=717762328687-iludtf96g1hinl76e4lc1b9a82g457nn.apps.googleusercontent.com&scope=profile%20email&redirect_uri=https%3A%2F%2Fstackauth.com%2Fauth%2Foauth2%2Fgoogle&state=%7B%22sid%22%3A1%2C%22st%22%3A%2259%3A3%3Abbc%2C16%3Afad07e7074c3d678%2C10%3A1601127482%2C16%3A9619c3b16b4c5287%2Ca234368b2cab7ca310430ff80f5dd20b5a6a99a5b85681ce91ca34820cea05c6%22%2C%22cdl%22%3Anull%2C%22cid%22%3A%22717762328687-iludtf96g1hinl76e4lc1b9a82g457nn.apps.googleusercontent.com%22%2C%22k%22%3A%22Google%22%2C%22ses%22%3A%22d18871cbc2a3450c8c4114690c129bde%22%7D&response_type=code&flowName=GeneralOAuthFlow')
        username = self.browser.find_element_by_id('identifierId')
        username.send_keys(usernameStr)
        nextButton = self.browser.find_element_by_id('identifierNext')
        nextButton.click()
        await asyncio.sleep(7)

        self.browser.save_screenshot("ss.png")
        await self.channel.send(file=discord.File('ss.png'))
        os.remove('ss.png')
        await self.channel.send("*Trying to put the password in...*")

        password = self.browser.find_element_by_xpath("//input[@class='whsOnd zHQkBf']")
        password.send_keys(passwordStr)
        signInButton = self.browser.find_element_by_id('passwordNext')
        signInButton.click()
        await asyncio.sleep(7)
        try:
            if(self.browser.find_element_by_xpath('/html[1]/body[1]/div[1]/div[1]/div[2]/div[1]/div[2]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/form[1]/span[1]/section[1]/div[1]/div[1]/div[1]/div[2]/div[2]/span[1]')):
                await self.channel.send("**Wrong password, you can change the credentials with !changecredentials**")
                self.browser.quit()
                Embed = discord.Embed(title="Unsuccessful meeting", description="------------------------", color=0x00ff80)
                Embed.set_author(name="This sessions ID: " + str(session_id))
                Embed.add_field(name="Current channels ID: ", value=str(self.channel.id), inline=False)
                Embed.add_field(name="Cause: ", value="Wrong password", inline=False)
                Embed.add_field(name="This channel will be deleted in:", value="5 minutes", inline=False)
                Embed.set_footer(text="Your Discord User ID: " + str(discord_id))
                await self.channel.send(embed=Embed)
                await asyncio.sleep(300)
                await self.channel.delete()
                return False
        except:
            await self.channel.send("*Successful login*")

        if(self.browser.find_elements_by_xpath('//*[@id="authzenNext"]/div/button/div[2]')):
            #context.bot.send_chat_action(chat_id=userId, action=ChatAction.TYPING)
            #context.bot.send_message(chat_id=userId, text="Need Verification. Please Verify")
            self.browser.find_element_by_xpath('//*[@id="authzenNext"]/div/button/div[2]').click()
            await asyncio.sleep(5)

            self.browser.save_screenshot("ss.png")
            await self.channel.send(file=discord.File('ss.png'))
            os.remove('ss.png')
            await self.channel.send("*Needing Verification...*")

            await asyncio.sleep(5)
        try:
            self.browser.get(meet_link)
            await asyncio.sleep(3)  

            self.browser.save_screenshot("ss.png")
            await self.channel.send(file=discord.File('ss.png'))
            os.remove('ss.png')
            await self.channel.send("*Going into the meeting...*")

            if(self.browser.find_elements_by_xpath('//*[@id="yDmH0d"]/div[3]/div/div[2]/div[3]/div')):
                self.browser.find_element_by_xpath('//*[@id="yDmH0d"]/div[3]/div/div[2]/div[3]/div').click()
                await asyncio.sleep(3)  

                #context.bot.delete_message(chat_id=userId ,message_id = mid)

                self.browser.save_screenshot("ss.png")
                await self.channel.send(file=discord.File('ss.png'))
                os.remove('ss.png')
                await asyncio.sleep(15)
            try:
                self.browser.find_element_by_xpath("//span[@class='NPEfkd RveJvd snByac' and contains(text(), 'Ask to join')]").click()
                await asyncio.sleep(10)
            except:
                self.browser.find_element_by_xpath("//span[@class='NPEfkd RveJvd snByac' and contains(text(), 'Join now')]").click()
                await asyncio.sleep(10)

            #context.bot.delete_message(chat_id=userId ,message_id = mid)
            self.browser.save_screenshot("ss.png")
            await self.channel.send(file=discord.File('ss.png'))
            os.remove('ss.png')
            await self.channel.send("*Sitting in the meeting...*")
            await asyncio.sleep(15)  

            #context.bot.delete_message(chat_id=userId ,message_id = mid)
            #await asyncio.sleep(10)  

            self.browser.save_screenshot("ss.png")
            await self.channel.send(file=discord.File('ss.png'))
            os.remove('ss.png')
            await self.channel.send("*Sitting in the meeting, you can relax now...*")
            #Splitting the time into 8 pieces
            #time = 80
            time_split = time/8
            count = 0
            #sleep = make_sleep()
            self.user_controls.start(time)
            for x in range(len("12345678")):
                if count % 2 == 0:
                    remaining_seconds = time_split*(8-x)
                    if remaining_seconds < 60:
                        await self.channel.send("In " + str(remaining_seconds) + " seconds the meeting will end.")
                    else:
                        await self.channel.send("In " + str(round(remaining_seconds/60)) + " minutes the meeting will end.")
                await asyncio.sleep(time_split)
                #await sleep(time_split)

            #self.client.loop.create_task(wait_meeting(channel, time))


            self.browser.quit()
            Embed = discord.Embed(title="Successful meeting", description="------------------------", color=0x00ff80)
            Embed.set_author(name="This sessions ID: " + str(session_id))
            Embed.add_field(name="Current channels ID: ", value=str(self.channel.id), inline=False)
            Embed.add_field(name="This channel will be deleted in:", value="5 minutes", inline=False)
            Embed.set_footer(text="Your Discord User ID: " + str(discord_id))
            await self.channel.send(embed=Embed)
            await asyncio.sleep(300)
            await self.channel.delete()
            return True


        except Exception as e:
            #self.browser.quit()
            print(str(e))
            await self.channel.send("**Error occurred! Do !startnow or join the meeting yourself immediately if necessary!!**")
            return False
            #context.bot.send_message(chat_id=userId, text="Error occurred! Fix error and retry!")
            #context.bot.send_message(chat_id=userId, text=str(e))
            #execl(executable, executable, "chromium.py")




