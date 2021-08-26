import asyncio
import discord
from discord.ext import commands
from discord.utils import get
import settings as s
import yunite
import _time
import gsheet

from threading import Thread



with open(s.DISCORD_TOKEN_FILENAME) as f:
    discord_token = f.readline()

bot = commands.Bot(command_prefix='!')

class Foo:
    def __init__(self):
        pass

    @bot.command()
    async def test(ctx):
        await ctx.send("response")


guild: discord.Guild

registration_msg: discord.Message
registration_open = False
registration_queue = []
registration_log = []
registered_list = []

yunite_ign = dict()

def convert(ms):
    if '!' in ms:
        return ms[3:-1]
    else:
        return ms[2:-1]


async def yunite_query_all():
    for member in guild.members:
        res = await yunite.get_user(member.id)
        if res:
            yunite_ign[member] = res


@bot.command()
@commands.has_role(s.ADMIN_ROLE_NAME)
async def make(ctx):
    channel_announce = get(guild.channels, name=s.CONTEST_CHANNEL_ANNOUNCE_NAME)

    embed = discord.Embed(
        title="Contest registration will begin shortly...",
        description="You must have linked your Epic Games account with Yunite to register.",
        color=s.EMBED_COLOR)

    embed.add_field(name="Contest", value=s.CONTEST_NAME, inline=False)
    embed.add_field(name="Format", value=s.CONTEST_FORMAT)
    embed.add_field(name="Players", value=s.CONTEST_CAPACITY)

    embed.set_thumbnail(url=ctx.message.author.avatar_url)
    embed.set_image(url=ctx.message.author.avatar_url)

    await channel_announce.send(embed=embed)

    embed = discord.Embed(
        title="\N{large yellow circle}  Collecting players data...",
        color=s.EMBED_COLOR)
    embed.set_footer(text=f"Started at {_time.gettime()}")
    _msg = await channel_announce.send(embed=embed)

    await yunite_query_all()

    await _msg.delete()

    embed = discord.Embed(
        title=f"\N{large green circle}  Collected {len(yunite_ign)} player data.",
        color=s.EMBED_COLOR)
    embed.set_footer(text=f"Finished at {_time.gettime()}")

    await channel_announce.send(embed=embed)


@bot.command()
@commands.has_role(s.ADMIN_ROLE_NAME)
async def open(ctx):
    global registration_msg, registration_open

    channel_announce = get(guild.channels, name=s.CONTEST_CHANNEL_ANNOUNCE_NAME)

    embed = discord.Embed(
        title="Contest is Open for Registration!",
        description="Click on the \N{raised hand} *raised hand icon* below to register.",
        color=s.EMBED_COLOR)

    registration_open = True
    registration_msg = await channel_announce.send(embed=embed)
    await registration_msg.add_reaction("\N{raised hand}")

players = None

@bot.command()
@commands.has_role(s.ADMIN_ROLE_NAME)
async def close(ctx):
    global registration_open
    channel_announce = get(guild.channels, name=s.CONTEST_CHANNEL_ANNOUNCE_NAME)

    registration_open = False
    await registration_msg.delete()

    embed = discord.Embed(
        title="Registration is now Closed.",
        description="Thank you for your registration.",
        color=s.EMBED_COLOR)

    embed.add_field(name="Contest", value=s.CONTEST_NAME, inline=False)

    players_raw = players[0]
    n = len(players_raw)

    pl = [f"{gid} <@!{mid}>" for _, _, gid, mid in players_raw]

    col1 = '\n'.join(str(p) for p in pl[:n//2])
    embed.add_field(name="Players", value=col1)
    col2 = '\n'.join(str(p) for p in pl[n//2:])
    embed.add_field(name="Players", value=col2)

    await channel_announce.send(embed=embed)


@bot.command()
@commands.has_role(s.ADMIN_ROLE_NAME)
async def getid(ctx, mention_str):
    if mention_str.startswith('<@') and mention_str.endswith('>'):
        await ctx.send(convert(mention_str))


def can_register(member: discord.Member):
    if member in registration_queue:
        return False
    if any(member == entry[0] for entry in registered_list):
        return False
    return True



async def gsheet_autolog():
    global players

    while True:
        await asyncio.sleep(5)
        ws = await gsheet.get_worksheet(s.GSHEET_URL, s.GSHEET_CONTEST_REGISTER_LOGGING_SHEET_NAME)
        await ws.insert_rows(registration_log, row=2)
        registration_log.clear()
        ws = await gsheet.get_worksheet(s.GSHEET_URL, s.GSHEET_CONTEST_REGISTER_SHEET_NAME)
        players = await ws.batch_get(['A2:D65'])
        print(players)

loop = asyncio.new_event_loop()
def f(loop):
    asyncio.set_event_loop(loop)
    loop.run_forever()

t = Thread(target=f, args=(loop,))
t.start()
asyncio.run_coroutine_threadsafe(gsheet_autolog(), loop)

async def register(member: discord.Member, game_id: str):
    time_str = _time.gettime()
    registration_no = len(registered_list)+1

    registered_list.append((member, game_id))
    registration_log.append((time_str, registration_no, member.display_name, game_id, convert(member.mention)))

    channel_log = get(guild.channels, name=s.CONTEST_CHANNEL_LOG_NAME)

    embed = discord.Embed(
        title="New Registration",
        color=s.EMBED_COLOR)

    embed.add_field(name="#", value=str(registration_no))
    embed.add_field(name="Discord ID", value=member.mention)
    embed.add_field(name="Game ID", value=game_id)

    embed.set_footer(text=time_str)

    await channel_log.send(embed=embed)




async def notify_registered(member: discord.Member, game_id: str):
    embed = discord.Embed(
        title="\N{large green circle}  Registration Form Sent!",
        description="If you have any questions, please contact our admin mods.",
        color=s.EMBED_COLOR)

    embed.add_field(name="Contest", value=s.CONTEST_NAME, inline=False)
    embed.add_field(name="#", value=str(len(registered_list)))
    embed.add_field(name="Discord ID", value=member.mention)
    embed.add_field(name="Game ID", value=game_id)

    await member.send(embed=embed)


async def notify_not_linked_with_yunite(member: discord.Member):
    channel_yunite = get(guild.channels, name=s.YUNITE_REGISTER_CHANNEL_NAME)

    embed = discord.Embed(
        title="\N{large red circle}  Your Registration was not successful...",
        description=f"It seems that you did not link your Epic Games account with Yunite.\n"
                    f"Please visit {channel_yunite.mention} to do so and try again.",
        color=s.EMBED_COLOR)

    await member.send(embed=embed)
    await registration_msg.remove_reaction("\N{raised hand}", member)


async def process_registration():
    member = registration_queue.pop(0)

    if member in yunite_ign:
        game_id = yunite_ign[member]
        await register(member, game_id)
        await notify_registered(member, game_id)
    else:
        game_id = await yunite.get_user(member.id)
        if game_id:
            await register(member, game_id)
            await notify_registered(member, game_id)
        else:
            await notify_not_linked_with_yunite(member)


@bot.event
async def on_raw_reaction_add(e: discord.RawReactionActionEvent):
    if e.event_type != "REACTION_ADD":
        return

    if e.user_id == bot.user.id:
        return

    if registration_open and e.message_id == registration_msg.id:
        if not can_register(e.member):
            return
        registration_queue.append(e.member)
        await process_registration()


@bot.event
async def on_ready():
    global guild, channel_announce, channel_log

    await yunite.auth()

    guild = get(bot.guilds, name=s.GUILD_NAME)

    for m in guild.members:
        print(m.mention)
    print(bot.user)


bot.run(discord_token)