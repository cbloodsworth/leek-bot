import discord
import os
from discord.ext import tasks
import commands as cm
import leetcode as lc
import dbdriver as db
import helper as hlpr

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

    channel = client.get_channel(1112495961130934312)
    check_for_recent_problems.start(channel=channel)
    clear_cache.start()
    update_streak.start(channel=channel)


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    msg = message.content.split(' ')
    cmd, args = msg[0], msg[1:]

    if   cmd == cm.CMD_AUDIT: await cm.lc_audit(args, message.channel)
    elif cmd == cm.CMD_FOLLOW: await cm.lc_follow(args, message.channel, client)
    elif cmd == cm.CMD_UNFOLLOW: await cm.lc_unfollow(args, message.channel, client)
    elif cmd == cm.CMD_FOLLOWING: await cm.lc_following(message.channel)


cache = set()
@tasks.loop(minutes=6)
async def check_for_recent_problems(channel):
    if not hlpr.is_business_hours: return
    for user in db.get_followed():
        recent_problem = lc.superRecentProblem(user)
        if not recent_problem: continue
        if (user, recent_problem) not in cache:
            cache.add((user, recent_problem))
            await channel.send(f"{user} just completed {recent_problem}!")


@tasks.loop(minutes=60)
async def clear_cache():
    if cache: cache.clear() 
    

@tasks.loop(hours=24)
async def update_streak(channel):
    for user in db.get_followed():
        if lc.leetcodeScrape(user).recent: db.update_streak(user)
        else: 
            if db.get_streak(user) != 0:
                await channel.send(f"<@&1112788036074356798> {user} just lost their streak!")
                db.reset_streak(user)


client.run(os.environ['DISCORD_KEY'])
