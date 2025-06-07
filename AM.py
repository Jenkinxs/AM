from logging import exception
import discord
from discord.ext import commands
import yt_dlp
import os
import asyncio
from pytube import Search
import random


print("\n\n")
print("==================ATOMIC DISCORD BOT - Atomic Incorporated (C) 2025==================")
print("Version 2.1.0, May 27, 2025\n")

ffmpeg_path = "ffmpeg"
PREFIX = ""
TOKEN = ""
STATUS = ""
LOG = "false"
FILE_DIR = os.path.dirname(os.path.realpath(__file__))

#################INITIALIZE BOT#######################
intents = discord.Intents.default()
intents.message_content = True

###Pulls settings from bot_settings.txt, and assigns them to the global variables
def pullSettings():
    global PREFIX, TOKEN, STATUS, LOG

    with open("bot_settings.txt", 'r') as file:
        for line in file:
            if line.startswith("prefix"):
                PREFIX = line.split("=", 1)[1].strip().strip('"')
            elif line.startswith("token"):
                TOKEN = line.split("=", 1)[1].strip().strip('"')
            elif line.startswith("status"):
                STATUS = line.split("=", 1)[1].strip().strip('"')
            elif line.startswith("log"):
                LOG = line.split("=", 1)[1].strip().strip('"')


###Checks if a default status message is needed
def status():
    global STATUS

    status_message = STATUS

    if STATUS == "" or not STATUS:
        status_message = "www.atomiccorp.org"

    return status_message

pullSettings()

bot = commands.Bot(command_prefix=PREFIX, intents=intents, activity=discord.Game(name=status()))

###The core of the bot, keeps track of files, playlist, and the client
playlist = []
downloaded_files = []
downloaded_filename = None
voice_client = None


ydl_opts = {
    'format': 'bestaudio/best',
    'headers': {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9', 'X-Forwarded-For': f'ABC{random.getrandbits(50)}'
    },
}

#################INITIALIZE BOT######################


#################BOT COMMANDS########################


async def join(ctx):
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        await channel.connect()
        await ctx.send(f"Joined {channel.name}")
    else:
        await ctx.send("You need to join a voice channel first.")



@bot.command()
async def play(ctx, *, url: str):
    global voice_client, downloaded_filename

    try:
        if url:

            playlist.append(url)
            await ctx.send(f"Added {url} to the playlist.")


            if not voice_client or not voice_client.is_playing():
                if ctx.author.voice:
                    channel = ctx.author.voice.channel
                    if voice_client and voice_client.channel != channel:
                        await voice_client.disconnect()
                        voice_client = None
                    if not voice_client:
                        voice_client = await channel.connect()
                    await play_next(ctx)
                else:
                    await ctx.send("You need to join a voice channel first.")
        else:

            if not voice_client or not voice_client.is_playing():
                if ctx.author.voice:
                    channel = ctx.author.voice.channel
                    if voice_client and voice_client.channel != channel:
                        await voice_client.disconnect()
                        voice_client = None  #
                    if not voice_client:
                        voice_client = await channel.connect()
                    await play_next(ctx)
                else:
                    await ctx.send("You need to join a voice channel first.")
            else:
                await ctx.send("The bot is already playing a track!")
    except Exception as e:
        print("NO URL FOUND")

        search = Search(url)
        first_result = (search.results[0])
        video = first_result.watch_url

        playlist.append(video)
        await ctx.send(f"Added {video} to the playlist.")


        if not voice_client or not voice_client.is_playing():
            if ctx.author.voice:
                channel = ctx.author.voice.channel
                if voice_client and voice_client.channel != channel:
                    await voice_client.disconnect()
                    voice_client = None
                if not voice_client:
                    voice_client = await channel.connect()
                await play_next(ctx)
            else:
                await ctx.send("You need to join a voice channel first.")
    else:

        if not voice_client or not voice_client.is_playing():
            if ctx.author.voice:
                channel = ctx.author.voice.channel
                if voice_client and voice_client.channel != channel:
                    await voice_client.disconnect()
                    voice_client = None
                if not voice_client:
                    voice_client = await channel.connect()
                await play_next(ctx)
            else:
                await ctx.send("You need to join a voice channel first.")
        else:
            print("The bot is already playing a track!")




@bot.command()
async def stop(ctx):
    global voice_client
    if voice_client and voice_client.is_playing():
        voice_client.stop()
        playlist.clear()
        if downloaded_filename:
            await asyncio.sleep(1)
            try:
                delete_file(downloaded_filename)
            except PermissionError as e:
                print(f"Error deleting file: {e}. The file might still be in use.")
    await ctx.send("Cleaned up the file.")



@bot.command()
async def skip(ctx):
    global voice_client
    if voice_client and voice_client.is_playing():
        voice_client.stop()
        if downloaded_filename:
            await asyncio.sleep(1)
            try:
                delete_file(downloaded_filename)
            except PermissionError as e:
                print(f"Error deleting file: {e}. The file might still be in use.")

        await ctx.send("Track skipped.")

        await play_next(ctx)
    else:
        await ctx.send("No track is currently playing.")



@bot.command()
async def seek(ctx, time: str):
    global voice_client, downloaded_filename, playlist

    if voice_client and voice_client.is_playing():
        try:
            minutes, seconds = map(int, time.split(':'))
            total_seconds = minutes * 60 + seconds
        except ValueError:
            await ctx.send("Please provide the time in MM:SS format (e.g., 2:30 for 2 minutes 30 seconds).")
            return


        voice_client.stop()


        source = discord.FFmpegPCMAudio(downloaded_filename, executable=ffmpeg_path, options=f"-ss {total_seconds}")


        def after_playback(error):
            if error:
                print(f"Error occurred: {error}")

            bot_loop = bot.loop
            bot_loop.create_task(delete_after_delay(downloaded_filename))

            if playlist:
                bot_loop.create_task(play_next(ctx))
            else:
                print("No more tracks in the playlist.")


        voice_client.play(source, after=after_playback)

        await ctx.send(f"Now seeking to {time} in the current track!")
    else:
        await ctx.send("No track is currently playing.")



@bot.command()
async def leave(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send("Disconnected from the voice channel.")
        delete_after_delay(downloaded_filename)
    else:
        await ctx.send("I'm not in a voice channel.")


@bot.command()
async def pause(ctx):
    if voice_client and voice_client.is_playing():
        voice_client.pause()
        await ctx.send("Track paused!")
    else:
        await ctx.send("Nothing is playing!")


@bot.command()
async def shutdown(ctx):
    try:
        playlist.clear()
        for file in downloaded_files:
            delete_file(file)
        downloaded_files.clear()
    except: ValueError("No file was created")
    await bot.close()


@bot.command()
async def smile(ctx):
    await ctx.send("https://tenor.com/view/hot-outside-gif-2448198275159709505")


@bot.command()
async def ping(ctx):
    await ctx.send(f"Ping between me and Discord: {bot.latency:.3f}ms")


@bot.command()
async def nowplaying(ctx):
    if voice_client and voice_client.is_playing():
        await ctx.send(f"Currently Playing: {downloaded_filename.removesuffix('.webm')}")
    else:
        await ctx.send("No track is currently playing.")


@bot.command()
async def queue(ctx):
    index = 1
    while playlist[index] != "" or playlist[index] != []:
        await ctx.send(f"Track {index}: {playlist[index]}.")
        index += 1

    if playlist[index] == "" or playlist[index] == []:
        await ctx.send(f"There are no more tracks in the playlist.")

@bot.command()
async def save(ctx):
    global playlist
    try:
        with open("saved.txt", 'a') as file:
            file.write(f"{playlist[0]}\n")
        await ctx.send("Playlist saved.")
    except: ValueError("Playlist is empty!")


@bot.command()
async def saved(ctx):
    global playlist
    try:

        with open("saved.txt", 'r') as file:
            for line in file:
                counter = 1
                await ctx.send(f"{counter}: {line}")
                counter += 1

    except: ValueError("File is empty!")


@bot.command()
async def load(ctx, line):
    global playlist
    try:

        with open("saved.txt", 'r') as file:
            fileLine = file.readlines()
            url = fileLine[line]
            await play(ctx, url)

    except:
        ValueError("File is empty!")


@bot.command()
async def removeall(ctx):
    try:
        playlist.clear()
        for file in downloaded_files:
            delete_file(file)
        downloaded_files.clear()
    except IndexError:
        await ctx.send("The playlist is empty!")


#################BOT COMMANDS########################




###################REFERENCE COMMANDS####################
async def play_next(ctx):
    global voice_client, downloaded_filename, playlist
    if playlist:

        next_url = playlist.pop(0)

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print("Downloading audio...")
            await ctx.send("Preparing to play, please wait.")
            videoInfo = ydl.extract_info(next_url, download=True,)
            downloaded_filename = ydl.prepare_filename(videoInfo)
            downloaded_files.append(downloaded_filename)


        source = discord.FFmpegPCMAudio(downloaded_filename, executable=ffmpeg_path)

        def after_playback(error):
            if error:
                print(f"Error occurred: {error}")

            bot_loop = bot.loop
            bot_loop.create_task(delete_after_delay(downloaded_filename))

            if playlist:
                bot_loop.create_task(play_next(ctx))
            else:
                print("No more tracks in the playlist.")


        voice_client.play(source, after=after_playback)
        await ctx.send(f"Now playing {downloaded_filename.removesuffix('.webm')}")


    else:
        print("The playlist is empty!")


async def delete_after_delay(filename):

    await asyncio.sleep(2)
    try:
        delete_file(filename)
    except PermissionError as e:
        print(f"Error deleting file: {e}. The file might still be in use.")



def delete_file(file_path):
    full_path = os.path.abspath(file_path)
    if os.path.exists(file_path):
        if voice_client and not voice_client.is_playing():
            if not full_path.startswith(FILE_DIR):
                raise ValueError("Attempt to delete a file outside of allowed directory.")

            try:
                os.remove(file_path)
                print(f"Deleted file: {file_path}")
            except PermissionError as e:
                print(f"Error deleting file: {file_path}. It might still be in use.")
        else:
            print("Can't Delete. Bot is playing audio.")
    else:
        print(f"File {file_path} not found, unable to delete.")




###################REFERENCE COMMANDS####################


bot.run(TOKEN)

input("Press Enter to exit...")