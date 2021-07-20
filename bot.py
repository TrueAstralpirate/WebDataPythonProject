from discord.ext import commands
from discord import FFmpegPCMAudio

from manager import Manager
from custom_queue import CustomQueue
from settings import DISCORD_TOKEN, GUILD_NAME

manager = Manager()
queues = CustomQueue()
bot = commands.Bot(command_prefix="!")


@bot.event
async def on_ready():
    print(f"{bot.user.name} has connected to Discord!")


def find_voice(ctx):
    voice = None
    for voice_client in bot.voice_clients:
        if voice_client.guild == ctx.guild:
            voice = voice_client
    return voice


async def start_playing(ctx, audio_name):
    if audio_name == None:
        return

    def play(id, voice):
        if not queues.get_loop(id):
            queues.pop(id)
            if queues.get_len(id) == 0:
                return

        source = FFmpegPCMAudio(queues.front(id))
        player = voice.play(source, after=lambda x=None: play(id, voice))

    id = ctx.message.guild.id
    if ctx.author.voice:
        channel = ctx.message.author.voice.channel

        voice = find_voice(ctx)
        if not voice:
            voice = await channel.connect()

        if voice.is_playing():
            stop(ctx)

        source = FFmpegPCMAudio(audio_name)
        player = voice.play(source, after=lambda x=None: play(id, voice))
    else:
        await ctx.send("You are not on audio server")


@bot.command(name="leave")
async def leave(ctx):
    id = ctx.message.guild.id
    queues.set_loop(id, False)
    queues.clear(id)
    if ctx.voice_client:
        await ctx.guild.voice_client.disconnect()
        await ctx.send("I left the voice channel")
    else:
        await ctx.send("I am not in a voice channel")


@bot.command(name="pause")
async def pause(ctx):
    voice = find_voice(ctx)
    if not voice:
        return
    if voice.is_playing():
        voice.pause()
    else:
        await ctx.send("Nothing is being played right now")


@bot.command(name="resume")
async def resume(ctx):
    voice = find_voice(ctx)
    if not voice:
        return
    if voice.is_playing():
        await ctx.send("It's already playing")
    else:
        voice.resume()


@bot.command(name="skip")
async def skip(ctx):
    id = ctx.message.guild.id
    queues.set_loop(id, False)
    voice = find_voice(ctx)
    if not voice:
        return
    voice.stop()


@bot.command(name="yt")
async def youtube(ctx, url):
    id = ctx.message.guild.id
    result_name = manager.youtube_query(url)
    queues.add(id, result_name)

    if queues.get_len(id) == 1:
        await start_playing(ctx, result_name)


@bot.command(name="tts")
async def text_to_speech(ctx, text):
    id = ctx.message.guild.id
    result_name = manager.tts_query(text)
    queues.add(id, result_name)

    if queues.get_len(id) == 1:
        await start_playing(ctx, result_name)


@bot.command(name="clear")
async def clear_queue(ctx):
    id = ctx.message.guild.id
    queues.clear(id)


@bot.command(name="loop")
async def loop(ctx):
    id = ctx.message.guild.id
    queues.set_loop(id, True)


@bot.command(name="unloop")
async def unloop(ctx):
    id = ctx.message.guild.id
    queues.set_loop(id, False)


bot.run(DISCORD_TOKEN)
