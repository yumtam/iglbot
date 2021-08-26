import asyncio
import YuniteAPI
import settings as s

client = YuniteAPI.Client()
DELAY = s.YUNITE_DELAY

with open(s.YUNITE_TOKEN_FILENAME) as f:
    yunite_token = f.readline()


async def auth():
    await asyncio.sleep(DELAY)
    await client.add_token(guild_id=s.GUILD_ID, api_key=yunite_token)


async def get_user(user_id):
    await asyncio.sleep(DELAY)
    res = await client.fetch_user(guild_id=s.GUILD_ID, user_id=user_id)
    if res is not None:
        return res.displayname
