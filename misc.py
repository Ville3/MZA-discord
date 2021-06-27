#Init
import discord
from discord.ext import commands
import asyncio

def make_sleep():
    async def sleep(delay, result=None, *, loop=None):
        coro = asyncio.sleep(delay, result=result, loop=loop)
        task = asyncio.ensure_future(coro)
        sleep.tasks.add(task)
        try:
            return await task
        except asyncio.CancelledError:
            return result
        finally:
            sleep.tasks.remove(task)

    sleep.tasks = set()
    sleep.cancel_all = lambda: sum(task.cancel() for task in sleep.tasks)
    return sleep


class Miscellaneous(commands.Cog):
    def __init__(self, client):
        self.client = client

    # /clear - command
    @commands.command(name='clear', hidden=True)
    async def clear(self, context, num_messages: int=10):
        """Clear <n> messages from current channel"""
        channel = context.message.channel
        await context.message.delete()
        await channel.purge(limit=num_messages, check=None, before=None)
        await context.message.channel.send('Successfully deleted ' + str(num_messages) + ' messages!', delete_after=3.0)
        return True