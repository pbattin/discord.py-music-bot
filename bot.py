import discord
import asyncio
import os

client = discord.Client()
current_song = ""
songs = []
current_vc = None
directory = "E:/Music/Music/Preston Battin/Youtube Rips"

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith('next'):
        await next(message)

    if message.content.startswith('play'):
        await play_playlist(message)

async def play_playlist(message):
    global current_song
    global current_vc
    global songs
    global directory

    await message.delete()
    # grab the user who sent the command
    user=message.author
    voice_channel=user.voice.channel
    # only play music if user is in a voice channel
    if voice_channel != None:
        current_vc = voice_channel
        for file in os.listdir(directory):
            filename = os.fsdecode(file)
            if filename.endswith(".mp3") or filename.endswith(".m4a"):
                songs.append(os.path.join(directory, filename))                        
        current_song=songs[0]
        current_vc = await voice_channel.connect()
        current_vc.play(discord.FFmpegOpusAudio(executable="ffmpeg.exe", source=current_song, bitrate=128))
        # Sleep while audio is playing.
        while current_vc.is_playing():
            await asyncio.sleep(1)
            if songs.index(current_song) + 1 < len(songs):
                await next()
            continue                
        if songs.index(current_song) + 1 < len(songs):
            await next()
        await current_vc.disconnect()
    else:
        await message.channel.send(str(message.author.name) + "is not in a channel.")
    # Delete command after the audio is done playing.
    await message.delete()

async def next(message = None):
    # Reference global objects
    global current_song
    global current_vc
    global songs 
    print(message != None)
    if message != None:
        await message.delete()
    # Check to make sure we are within the index
    if songs.index(current_song) + 1 < len(songs):
        current_vc.stop()
        current_song=songs[songs.index(current_song) + 1]
        current_vc.play(discord.FFmpegOpusAudio(executable="ffmpeg.exe", source=current_song, bitrate=128))
    else:
       current_vc.disconnect() 

client.run('OTI4ODI0NzY3NjY5MjM1Nzcy.YdeZeQ.lXLBJMcJSeY0t4Orl_gIjoolZCs')