import discord
import os
from discord.ext import tasks
import commands as cm

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

    channel = client.get_channel(1112495961130934312)
    mytask.start(channel=channel)

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    msg = message.content.split(' ')
    cmd, args = msg[0], msg[1:]

    if   cmd == cm.CMD_AUDIT: await cm.lc_audit(args, message.channel)
    elif cmd == cm.CMD_FOLLOW: await cm.lc_follow(args, message.channel, client)


@tasks.loop(seconds=10)
async def mytask(channel):
    # later we would make this function perform some routine checking
    pass


client.run(os.environ['DISCORD_KEY'])
