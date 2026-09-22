import discord, os, asyncio
from discord.ext import commands
TOKEN=os.getenv("DISCORD_TOKEN") or os.getenv("TOKEN")
RADIO_URL=os.getenv("RADIO_URL")
intents=discord.Intents.default()
intents.message_content=True
intents.voice_states=True
bot=commands.Bot(command_prefix="!",intents=intents)
@bot.event
async def on_ready():
    print(f"Online {bot.user}")
@bot.command()
async def join(ctx):
    if not ctx.author.voice:
        await ctx.send("ادخل روم")
        return
    ch=ctx.author.voice.channel
    if ctx.voice_client:
        await ctx.voice_client.disconnect(force=True)
        await asyncio.sleep(1)
    vc=await ch.connect(self_deaf=False,self_mute=False)
    before="-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5 -protocol_whitelist file,http,https,tcp,tls,crypto"
    src=discord.FFmpegPCMAudio(RADIO_URL,before_options=before,options="-vn")
    vc.play(src)
    await ctx.send("شغال 📻")
@bot.command()
async def leave(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect(force=True)
bot.run(TOKEN)
