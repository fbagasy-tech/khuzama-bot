import discord
import os
import asyncio
from discord.ext import commands

TOKEN = os.getenv("DISCORD_TOKEN") or os.getenv("TOKEN")
RADIO_URL = os.getenv("RADIO_URL") or "https://stream.sba.sa/56b7a7e4-4f39-4835-89a0-e94a3ec6afec/1-audio-0/live/playlist.m3u8"

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Online {bot.user} - ID {bot.user.id}")

@bot.command()
async def join(ctx):
    if not ctx.author.voice:
        await ctx.send("ادخل روم صوتي أول")
        return
    
    channel = ctx.author.voice.channel
    
    # افصل لو متصل قبل
    if ctx.voice_client:
        await ctx.voice_client.disconnect(force=True)
        await asyncio.sleep(1)
    
    try:
        vc = await channel.connect(self_deaf=True, self_mute=False, timeout=20)
    except Exception as e:
        await ctx.send(f"ما قدرت ادخل الروم: {e}")
        return

    # خيارات تمنع التقطيع
    before_options = "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5 -protocol_whitelist file,http,https,tcp,tls,crypto -analyzeduration 0 -probesize 32k"
    
    try:
        source = discord.FFmpegPCMAudio(RADIO_URL, before_options=before_options, options="-vn -loglevel warning")
        vc.play(source)
        await ctx.send(f"شغال في {channel.name} 📻")
    except Exception as e:
        await ctx.send(f"خطأ في تشغيل الراديو: {e}")

@bot.command()
async def leave(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect(force=True)
        await ctx.send("طلعت 👋")
    else:
        await ctx.send("مو متصل")

bot.run(TOKEN)
