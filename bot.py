import discord
import os
import asyncio
from discord.ext import commands

# التوكن
TOKEN = os.getenv("DISCORD_TOKEN") or os.getenv("TOKEN")

# رابط إذاعة خزامى عن طريق البروكسي (يشتغل في Railway)
RADIO_URL = os.getenv("RADIO_URL", "https://spring-butterfly-de76.fbagasy.workers.dev/?stream=https%3A%2F%2Fsba-radio-live1.sba.gov.sa%3A8443%2FkhuzamaRadio%2FkhuzamaRadio.m3u8")

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user} - Ready to play Khuzama Radio")

@bot.command()
async def join(ctx):
    if not ctx.author.voice:
        await ctx.send("❌ ادخل روم صوتي أولاً")
        return
    
    channel = ctx.author.voice.channel
    
    # لو البوت متصل في روم ثاني اطلع منه
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
    
    try:
        vc = await channel.connect(timeout=20, self_deaf=True)
        await ctx.send(f"🔊 دخلت {channel.name}، جاري تشغيل إذاعة خزامى...")
        
        # انتظر لين يثبت الاتصال
        await asyncio.sleep(1)
        
        # شغل البث
        source = discord.FFmpegPCMAudio(
            RADIO_URL,
            before_options="-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5 -probesize 200k",
            options="-vn -loglevel warning"
        )
        vc.play(source)
        await ctx.send("✅ شغلت إذاعة خزامى 📻")
        
    except Exception as e:
        await ctx.send(f"❌ خطأ: {e}")
        print(f"Join error: {e}")

@bot.command()
async def leave(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send("👋 طلعت من الروم")
    else:
        await ctx.send("❌ ماني داخل أي روم")

@bot.command()
async def stop(ctx):
    if ctx.voice_client and ctx.voice_client.is_playing():
        ctx.voice_client.stop()
        await ctx.send("⏹️ وقفت البث")
    else:
        await ctx.send("❌ ما في شي شغال")

bot.run(TOKEN)
