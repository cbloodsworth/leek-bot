import leetcode as lc
import dbdriver as db
import asyncio
from discord import TextChannel, Message, Client
import os

X = os.getenv('CALL_TOKEN')

CMD_AUDIT = f'{X}lc-audit'
CMD_FOLLOW = f'{X}lc-follow'
CMD_UNFOLLOW = f'{X}lc-unfollow'
CMD_FOLLOWING = f'{X}lc-following'
CMD_HELP = f'{X}lc-help'

TIMEOUT = 10.0

async def lc_audit(args: list[str], channel: TextChannel):
    if len(args) != 1:
        await channel.send(f'Intended use: `{CMD_AUDIT} <leetcode_username>')
        return

    username: str = args[0] 
    await channel.send(f'Pulling the latest data on LeetCode user {username}...')
    await channel.send(f'{lc.leetcodeScrape(username)}')


async def lc_follow(args: list[str], channel: TextChannel, client: Client):
    if len(args) != 1:
        await channel.send(f'Intended use: `{CMD_FOLLOW} <leetcode_username>')
        return

    username: str = args[0] 
    await channel.send(f"Searching for user {username}...")
    if lc.checkUser(username):
        if db.query_user(username) == True:
            await channel.send(f"Error: {username} is already being followed!")
            return

        msg = await channel.send(f"Are you sure you want to follow this user?")
        await msg.add_reaction("✅")
        await msg.add_reaction("⛔")

        def check(reaction, user):
            return (
                    user != msg.author
                    and str(reaction.emoji) in ["✅", "⛔"]
                    and reaction.message.id == msg.id
            )

        try: reaction, user = await client.wait_for("reaction_add", timeout=TIMEOUT, check=check)
        except asyncio.TimeoutError:
            await channel.send("No reaction added within the time limit.")
            return

        # Decided to follow user
        if str(reaction.emoji) == "✅":
            db.change_follow(username, True)
            await channel.send(f"{username} was followed!")

        # Decided not to follow user
        elif str(reaction.emoji) == "⛔":
            await channel.send(f"{username} was not followed.")

    else:
        await channel.send(f"Sorry, no such user exists.")
        return


async def lc_unfollow(args: list[str], channel: TextChannel, client: Client):
    if len(args) != 1:
        await channel.send(f'Intended use: `{CMD_UNFOLLOW} <leetcode_username>')
        return

    username: str = args[0] 
    await channel.send(f"Searching for user {username}...")
    if lc.checkUser(username):
        # Can't unfollow if not being followed in the first place
        if not db.query_user(username):
            await channel.send(f"Error: Can't unfollow, because {username} was never followed in the first place!")
            return

        msg = await channel.send(f"Are you sure you want to *unfollow* this user?")
        await msg.add_reaction("✅")
        await msg.add_reaction("⛔")

        def check(reaction, user):
            return (
                    user != msg.author
                    and str(reaction.emoji) in ["✅", "⛔"]
                    and reaction.message.id == msg.id
            )

        try: reaction, user = await client.wait_for("reaction_add", timeout=TIMEOUT, check=check)
        except asyncio.TimeoutError:
            await channel.send("No reaction added within the time limit.")
            return

        # Decided to unfollow user
        if str(reaction.emoji) == "✅":
            db.change_follow(username, False)
            await channel.send(f"{username} was **unfollowed**!")

        # Decided to keep following user
        elif str(reaction.emoji) == "⛔":
            await channel.send(f"{username} is still being followed.")

    else:
        await channel.send(f"Sorry, no such user exists.")
        return


async def lc_following(channel: TextChannel):
    await channel.send(f"{db.get_followed()}")

