import leetcode as lc
from discord import TextChannel

CMD_AUDIT = '$lc-audit'
CMD_HELP = '$lc-help'

async def lc_audit(args: list[str], channel: TextChannel):
    if len(args) != 1:
        await channel.send(f'Intended use: `{CMD_AUDIT} <leetcode_username>')
        return

    username: str = args[0] 
    await channel.send(f'Pulling the latest data on LeetCode user {username}...')
    await channel.send(f'{lc.leetcodeScrape(username)}')

