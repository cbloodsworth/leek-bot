import discord
import commands as cm

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    msg = message.content.split(' ')
    cmd, args = msg[0], msg[1:]

    if cmd == cm.CMD_AUDIT: await cm.lc_audit(args, message.channel)


with open('secrets/auth.txt') as f:
    client.run(f.readline())


