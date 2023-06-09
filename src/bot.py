import discord
import os
import asyncio
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


@tasks.loop(minutes=15) 
async def check_for_recent_problems(channel):
    print("Checking for recent problems...") 
    for user in db.get_followed():
        print(f"Running an audit on {user}...")
        recent_problem = lc.superRecentProblem(user)
        if recent_problem != "" and db.push_cache(user, recent_problem):
            await channel.send(f"{user} just completed {recent_problem}!")


@tasks.loop(hours=24)
async def update_streak(channel):
    print(f"update_streak(): Sleeping for {hlpr.seconds_until_7pm() / 3600} hours... ")
    await asyncio.sleep(hlpr.seconds_until_7pm())  # Wake up at 7pm every day
    print("update_streak(): Woke up. Cleaning cache...")
    db.clean_cache()
    for user in db.get_followed():
        print(f"update_streak(): Checking if {user} is recent...")
        if lc.leetcodeScrape(user).recent: 
            print("\tRecent.")
            streak = db.update_streak(user)
            await channel.send(f"{user} is on a roll with a streak of {streak}!")
        else: 
            print("\tNot recent.")
            if db.get_streak(user) != 0:
                await channel.send(f"<@&1112788036074356798> {user} just lost their streak!")
                db.reset_streak(user)


client.run(os.environ['DISCORD_KEY'])
