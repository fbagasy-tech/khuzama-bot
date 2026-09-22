
import discord, re, aiohttp, os
from discord.ext import commands, tasks

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents, case_insensitive=True)

QURAN_STABLE = "https://server03.quran-uni.com:7002/;stream.mp3"
PAGE = "https://radioplus.sba.sa/live/7"
FFMPEG = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

last_channel = None

async def get_khuzama():
    try:
        async with aiohttp.ClientSession() as s:
            async with s.get(PAGE, headers={"User-Agent":"Mozilla/5.0"}, timeout=15) as r:
                html = await r.text()
                m = re.findall(r'https://[^"']+\.m3u8[^"']*', html)
                if m:
                    return m[0].replace('\\u002F','/').replace('\\','')
    except: pass
    return None

@tasks.loop(seconds=20)
async def keeper():
    global last_channel
    if not last_channel: return
    try:
        vc = last_channel.guild.voice_client
        if not vc or not vc.is_connected():
            try: vc = await last_channel.connect(self_deaf=False)
            except: vc = await last_channel.connect()
        if vc and not vc.is_playing():
            url = await get_khuzama() or QURAN_STABLE
            vc.play(discord.FFmpegPCMAudio(url, **FFMPEG))
    except Exception as e:
        print(f"Keeper error: {e}")

@bot.command()
async def ping(ctx):
    await ctx.send(f"Pong! {round(bot.latency*1000)}ms")

@bot.command()
async def join(ctx):
    global last_channel
    if not ctx.author.voice:
        await ctx.send("ادخل روم صوتي")
        return
    last_channel = ctx.author.voice.channel
    vc = ctx.voice_client
    if not vc:
        try: vc = await last_channel.connect(self_deaf=False)
        except: vc = await last_channel.connect()
    elif vc.channel!= last_channel:
        await vc.move_to(last_channel)
    if vc.is_playing(): vc.stop()
    kh = await get_khuzama()
    if kh:
        url = kh
        await ctx.send("✅ شغال: خزامى الرسمي 🎵")
    else:
        url = QURAN_STABLE
        await ctx.send("⚠️ خزامى محجوب (لسه على أمريكا) - شغلت قرآن مستقر")
    vc.play(discord.FFmpegPCMAudio(url, **FFMPEG))
    if not keeper.is_running(): keeper.start()

@bot.command()
async def leave(ctx):
    global last_channel
    last_channel = None
    keeper.stop()
    if ctx.voice_client: await ctx.voice_client.disconnect()

@bot.event
async def on_ready():
    print(f"ONLINE {bot.user}")

bot.run(os.getenv("DISCORD_TOKEN"))
