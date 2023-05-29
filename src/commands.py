import leetcode as lc
import dbdriver as db
import asyncio
import csv
from discord import TextChannel, Message, Client

CMD_AUDIT = '$lc-audit'
CMD_FOLLOW = '$lc-follow'
CMD_HELP = '$lc-help'

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
        msg = await channel.send(f"Are you sure you want to follow this user?")
        await msg.add_reaction("✅")
        await msg.add_reaction("⛔")

        def check(reaction, user):
            return (
                    user != msg.author
                    and str(reaction.emoji) in ["✅", "⛔"]
                    and reaction.message.id == msg.id
            )

        try: reaction, user = await client.wait_for("reaction_add", timeout=15.0, check=check)
        except asyncio.TimeoutError:
            await channel.send("No reaction added within the time limit.")
            return

        # Decided to follow user
        if str(reaction.emoji) == "✅":
            db.push_user(username, True)
            await channel.send(f"{username} was followed!")

        # Decided not to follow user
        elif str(reaction.emoji) == "⛔":
            await channel.send(f"{username} was not followed.")

    else:
        await channel.send(f"Sorry, no such user exists.")
        return



