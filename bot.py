import discord, os, asyncio
from discord.ext import commands

TOKEN = os.getenv("DISCORD_TOKEN") or os.getenv("TOKEN")
RADIO_URL = os.getenv("RADIO_URL", "https://spring-butterfly-de76.fbagasy.workers.dev/?stream=https%3A%2F%2Fsba-radio-live1.sba.gov.sa%3A8443%2FkhuzamaRadio%2FkhuzamaRadio.m3u8")

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
        await asyncio.sleep(2)
        audio = discord.FFmpegOpusAudio(RADIO_URL, before_options="-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5", options="-vn")
        vc.play(audio)
        await ctx.send(f"✅ شغلت إذاعة خزامى في {channel.name} 📻")
    except Exception as e:
        await ctx.send(f"❌ خطأ: {e}")

@bot.command()
async def leave(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect(force=True)
        await ctx.send("👋 طلعت")

bot.run(TOKEN)
