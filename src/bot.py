import discord
import leetcode as lc

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    # Don't pay attention to messages the bot itself sends
    if message.author == client.user:
        return

    msg: list[str] = message.content.split(' ')

    AUDIT_COMMAND = '$lc-audit'
    if msg[0] == AUDIT_COMMAND:
        if len(msg) != 2:
            await message.channel.send('Intended use: `$lc-audit <leetcode_username>')
            return

        username: str = msg[1]
        await message.channel.send(f'Pulling the latest data on LeetCode user {username}...')
        await message.channel.send(lc.leetcodeScrape(username))

with open('../auth.txt') as f:
    client.run(f.readline())
