import discord, os, asyncio
from discord.ext import commands

TOKEN = os.getenv("DISCORD_TOKEN") or os.getenv("TOKEN")
# الرابط المباشر بدون بروكسي
RADIO_URL = "https://sba-radio-live1.sba.gov.sa:8443/khuzamaRadio/khuzamaRadio.m3u8"

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ {bot.user} Online")

@bot.command()
async def join(ctx):
    if not ctx.author.voice:
        await ctx.send("❌ ادخل روم صوتي أولاً")
        return
    channel = ctx.author.voice.channel
    if ctx.voice_client:
        await ctx.voice_client.disconnect(force=True)
        await asyncio.sleep(1)
    try:
        vc = await channel.connect(self_deaf=False, self_mute=False, timeout=30)
        await asyncio.sleep(1)
        
        # مهم: whitelist للـ https
        before = "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5 -protocol_whitelist file,http,https,tcp,tls,crypto"
        source = discord.FFmpegPCMAudio(RADIO_URL, before_options=before, options="-vn")
        
        vc.play(source)
        await ctx.send(f"✅ شغلت إذاعة خزامى في {channel.name} 📻")
    except Exception as e:
        await ctx.send(f"❌ خطأ: {e}")
        print(f"ERROR JOIN: {e}")

@bot.command()
async def leave(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect(force=True)
        await ctx.send("👋 طلعت")

bot.run(TOKEN)
