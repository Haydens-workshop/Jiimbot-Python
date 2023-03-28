import discord
from discord.ext import commands
from discord.utils import get
from youtube_search import YoutubeSearch
import distube
import os
import json
import time
import datetime
import sqlite3
import asyncio

db = sqlite3.connect('songtracker.db')
sql = db.cursor()

seeking = False
stopped = False
skipping = True

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.player = distube.DisTube(bot)

    async def play_audio(self, ctx, query, seeking_value=None):
        global sql, db
        voice = get(self.bot.voice_clients, guild=ctx.guild)

        def get_sec(val):
            m, s = val.split(':')
            return int(m) * 60 + int(s)

        if seeking_value:
            seek_time = get_sec(seeking_value)
            self.player.seek(seek_time)
            voice.stop()
            print("Stopped the music")

        try:
            await self.player.play(ctx, query)
        except Exception as e:
            print(f"An error occurred while playing audio: {e}")

    def updatenumbering(self, server_id):
        sql.execute(f'SELECT count(*) FROM `{server_id}`')
        number_of_entry = sql.fetchone()

        changed_all = False
        number_of_entry_before = number_of_entry[0] + 1
        row_to_be_changed = 0

        while changed_all is False:
            row_to_be_changed = row_to_be_changed + 1
            number_to_be_changed_with = row_to_be_changed - 1

            sql.execute(f'UPDATE `{server_id}` SET number = {number_to_be_changed_with} WHERE number = {row_to_be_changed}')
            db.commit()

            if row_to_be_changed == number_of_entry_before:
                changed_all = True

    async def clear_song_list(self, ctx):
        try:
            global stopped
            global sql, db

            if stopped is True:
                return
            server_id = ctx.guild.id
            sql.execute(f'DELETE FROM `{server_id}` WHERE number = 1')
            db.commit()

            sql.execute(f'SELECT count(*) FROM `{server_id}`')
            number_of_entry = sql.fetchone()
            if number_of_entry[0] == 0:
                sql.execute(f'DROP TABLE `{server_id}`')
                db.commit()
        except Exception as e:
            raise e

    async def stop_and_clear_queue(self, ctx):
        global stopped
        global sql, db

        voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        server_id = ctx.guild.id
        channel = ctx.author.voice.channel

        if voice and voice.is_playing():
            stopped = True
            await asyncio.sleep(1)
            voice.stop()
            await asyncio.sleep(1)
            stopped = False

async def end_queue(self, ctx):
    voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)

    if voice and voice.is_playing():
        voice.stop()
        try:
            sql.execute("SELECT name FROM sqlite_master WHERE type='table';")
            list_of_tables = sql.fetchall()
            if any(f"{server_id}" in word for word in list_of_tables):
                sql.execute(f'DROP TABLE `{server_id}`')
                db.commit()
            else:
                pass
        except Exception as e:
            print("ERROR FROM GTFO CMD:" + str(e))

        await ctx.send('Queue ended!')
    else:
        await ctx.send("I'm not playing music!")
        return

async def disconnect_voice_channel(self, ctx):
    voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
    channel = ctx.author.voice.channel

    if voice and voice.is_connected():
        await voice.disconnect()
        embed = discord.Embed(color=discord.Color.random(),
                              title=f"**:white_check_mark:Disconnected From `{channel}`:white_check_mark:**",
                              timestamp=ctx.message.created_at
                              )
        embed.set_footer(text="Jimbot", icon_url=self.bot.user.avatar.url)
        await ctx.send(embed=embed)
    else:
        self.updatenumbering(server_id)

async def handle_after_play_audio(self, ctx):
    await self.clear_song_list(ctx)
    await self.play_audio(ctx, None)

def after_play_audio_pre(self, ctx, error):
    global seeking
    global stopped
    global skipping

    if seeking is True:
        seeking = False
        return
    if stopped is True:
        stopped = True
        return

    coro = self.handle_after_play_audio(ctx)
    fut = asyncio.run_coroutine_threadsafe(coro, self.bot.loop)

    try:
        fut.result()
    except Exception as e:
        raise e

    @commands.command()
    async def play(self, ctx, *, args):
        FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
                          'options': '-vn'}
        try:
            global db, sql
            channel = ctx.author.voice.channel
            if channel is None:
                await ctx.send("You were not connected to any channel.")
                return
            if channel:
                voice = get(self.bot.voice_clients, guild=ctx.guild)
                song = self.search(args)
                server_name = str(ctx.guild)
                server_id = ctx.guild.id
                sql.execute(f'DELETE FROM song WHERE Server_ID =? AND Server_Name =?', (server_id, server_name))
                db.commit()
                username = str(ctx.message.author)
                userid = ctx.message.author.id
                queue_name = f"Queue#{server_id}"
                song_name = f"Song#{server_id}"
                channel_id = ctx.message.author.voice.channel.id
                channel_name = str(ctx.message.author.voice.channel)
                queue_num = 1
                sql.execute('INSERT INTO song("Server_ID", "Server_Name", "Voice_ID", "Voice_Name", "User_Name", "Next_Queue", "Queue_Name", "Song_Name","User_ID") VALUES(?,?,?,?,?,?,?,?,?)',
                            (server_id, server_name, channel_id, channel_name, username, queue_num, queue_name, song_name, userid))
                db.commit()
                sql.execute("SELECT name FROM sqlite_master WHERE type='table';")
                list_of_tables = sql.fetchall()
                if any(f"{server_id}" in word for word in list_of_tables):
                    pass
                else:
                    sql.execute(f'CREATE TABLE `{server_id}` (number INTEGER PRIMARY KEY, title TEXT, url TEXT)')
                    db.commit()
                sql.execute(f'SELECT * FROM song WHERE Server_ID = {server_id} AND Server_Name = "{server_name}"')
                song_queue = sql.fetchall()
                if len(song_queue) == 1:
                    await self.play_audio(ctx, song[0]["url"])
                else:
            try:
    sql.execute(f"SELECT id FROM users WHERE id={ctx.author.id}")
    result = sql.fetchone()
    if result is None:
        sql.execute(f"INSERT INTO users VALUES ({ctx.author.id},'{ctx.author.name}')")
        db.commit()

    voice_channel = ctx.author.voice.channel
    voice = get(self.bot.voice_clients, guild=ctx.guild)

    if voice and voice.is_connected():
        await voice.move_to(voice_channel)
    else:
        voice = await voice_channel.connect()

    if query is None:
        sql.execute(f"SELECT * FROM `{server_id}` WHERE number = 1")
        song = sql.fetchone()

        url = song[2]
        userid = song[1]
        username = await self.bot.fetch_user(userid)
        await ctx.send(f"Playing: {song[3]} requested by {username}")
        await self.player.play(ctx, url, after=self.after_play_audio_pre)
    else:
        results = YoutubeSearch(query, max_results=1).to_dict()
        url = f"https://www.youtube.com{results[0]['url_suffix']}"
        video_id = results[0]['id']
        video_title = results[0]['title']

        if any(f"{server_id}" in word for word in list_of_tables):
            sql.execute(f'SELECT count(*) FROM `{server_id}`')
            number_of_entry = sql.fetchone()
            queue_num = int(number_of_entry[0])+1
            sql.execute(f'INSERT INTO `{server_id}` ("req_by","author","song_info","number") VALUES(?,?,?,?)',(ctx.author.id,ctx.author.name,video_title,queue_num))
            db.commit()
        else:
            sql.execute(f'create table `{server_id}`('
                        '"number" integer not null primary key autoincrement,'
                        '"req_by" integer,'
                        '"author" text,'
                        '"song_info" text'
                        ')')

            sql.execute(f'INSERT INTO `{server_id}` ("req_by","author","song_info","number") VALUES(?,?,?,?)',(ctx.author.id,ctx.author.name,video_title,1))
            db.commit()

        await ctx.send(f'Added to Queue: {video_title} requested by {ctx.author}')
        await self.player.play(ctx, url, after=self.after_play_audio_pre)

except Exception as e:
    print(f"An error occurred while playing audio: {e}")
    await ctx.send("There was an error playing the audio.")

                    sql.execute(f'INSERT INTO `{server_id}` ("req_by","author","song_info","number") VALUES(?,?,?,?)',(userid,username,song['title'],1))
                    db.commit()
                req_by = ctx.author.id
                sql.execute(f'SELECT * FROM users WHERE User_ID = {req_by}')
                if sql.fetchone() is None:
                    sql.execute('INSERT INTO users("User_ID","Last_Song","Url") VALUES(?,?,?)',
                    (req_by,song['title'],song['Song_URL']))
                    db.commit()
                else:
                    sql.execute(f'UPDATE users SET Last_Song = ?, Url = ? WHERE User_ID=?',(song['title'],song['Song_URL'],req_by))
                    db.commit()

                if voice and voice.is_connected():
                    await voice.move_to(channel)
                else:
                    voice = await channel.connect()
                    embed = discord.Embed(color=discord.Color.random(),
                      title=f"**:white_check_mark:Connected to `{channel}`:white_check_mark:**",
                      timestamp=ctx.message.created_at)

if not voice.is_playing():
    await self.play_audio(ctx, None)  # If there is no audio playing, start playing audio from the beginning
else:
    try:
        sql.execute(f'SELECT count(*) FROM `{server_id}`')
        number_of_entry = sql.fetchone()
        number_of_entry = number_of_entry[0]
        author = ctx.message.author

        if number_of_entry > 1:
            sql.execute(f'SELECT * FROM `{server_id}` WHERE number = 2')
            upcomming_info = sql.fetchone()
            upcomming_title = upcomming_info[3]
        else:
            upcomming_title = "Nothing"
        if number_of_entry == 2:
            song_will_play_after = "Next"
        else:
            song_after_num = number_of_entry - 2
            song_will_play_after = f"After {song_after_num} Song"

        embed = (discord.Embed(
                    description=f"`{song['title']}`",
                    timestamp = ctx.message.created_at,
                    color=discord.Color.random()))
        embed.set_author(name="Added To Queue",icon_url="https://media.discordapp.net/attachments/564520348821749766/696332404549222440/4305809_200x130..gif")
        embed.add_field(name='**Duration**', value=f"{song['Duration']}",inline = False)
        embed.add_field(name='**Requested by**', value=f'{author}', inline = False)
        embed.add_field(name='**Song Will Play**', value=f"{song_will_play_after}", inline = False)
        embed.add_field(name='**Upcoming**', value=f"{upcomming_title}", inline = False)
        embed.set_footer(text = "Jimbot",icon_url = self.bot.user.avatar_url)
        embed.set_thumbnail(url=song['Image_URL'])
        await ctx.send(embed=embed)
    except sqlite3.Error as error:
        print("Error occurred while selecting data from database: ", error)
        await ctx.send("Oops! Something went wrong while selecting data from the database.")
    except Exception as e:
        print("An error occurred while adding song to queue: ", e)
        await ctx.send("Oops! Something went wrong while adding song to queue.")

except Exception as e:
    print("An error occurred while adding song to queue: ", e)
    await ctx.send("Oops! Something went wrong while adding song to queue. Please try again later.")

@commands.command()
async def seek(self, ctx, *, val: str = None):
    print("Seek command called!")
    if val is None:
        await ctx.send('Please specify the duration to seek.')
        return
    m, s = val.split(':')
    if int(s) > 59:
        await ctx.send('Invalid value for seconds. Please specify a value between 0 and 59.')
        return
    duration = int(m) * 60 + int(s)
    voice = get(self.bot.voice_clients, guild=ctx.guild)
    if voice is not None:
        try:
            channel = ctx.author.voice.channel            
            if channel:
                voice = get(self.bot.voice_clients, guild=ctx.guild)
                if voice is not None:
                    global seeking
                    seeking = True
                    await self.play_audio(ctx, duration)  # Seek to the specified duration and play audio from there
                else:
                    return
            else:
                await ctx.send("Please connect to a voice channel first.")
        except Exception as e:
            raise e
    else:
        print("Please connect to a voice channel first.")

# Command to disconnect bot from voice channel and clear the queue
@commands.command()
async def gtfo(self, ctx):
    global sql, db
    voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
    server_id = ctx.guild.id
    channel = ctx.author.voice.channel
    
    # Stop playing music and clear queue if it is playing
    if voice and voice.is_playing():
        global stopped
        stopped = True
        await asyncio.sleep(1)
        voice.stop()
        await asyncio.sleep(1)
        stopped = False 
    
    # Check if bot is connected to voice channel and drop the queue table
    if voice and voice.is_connected():
        try:
            sql.execute("SELECT name FROM sqlite_master WHERE type='table';")
            list_of_tables = sql.fetchall()
            if any(f"{server_id}" in word for word in list_of_tables):
                sql.execute(f'DROP TABLE `{server_id}`')
                db.commit()
            else:
                pass
        except Exception as e:
            print("An error occurred while dropping the table:", str(e))
        await ctx.send('Stopping the music and clearing the queue!')
    else:
        await ctx.send("I'm not playing any music!")
        return
    
    # Disconnect the bot from the voice channel and send an embed message
    await voice.disconnect()
    embed = discord.Embed(color = discord.Color.random(),
                          title=f"**:white_check_mark:Disconnected From `{channel}`:white_check_mark:**",
                          timestamp = ctx.message.created_at
                         ) 
    embed.set_footer(text = "Jimbot",icon_url = self.bot.user.avatar.url)
    await ctx.send(embed=embed)

# Command to pause the music
@commands.command()
async def pause(self,ctx):
    voice = get(self.bot.voice_clients, guild = ctx.guild)
    if voice and voice.is_playing():
        voice.pause()
        await ctx.send("Pausing!")
    else:
        await ctx.send("finna pause the music rlq")
        
# Command to resume the music
@commands.command()
async def resume(self, ctx):
    voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
    try:
        if voice and voice.is_paused():
            voice.resume()
            await ctx.send("Resuming the jams!")
        elif not voice.is_playing():
            await ctx.send("I need music to resume.")
        else:
            await ctx.send("Uh, Should I pause this?")
    except Exception as e:
        print(e)
        await ctx.send("Oops, something went wrong!")

@commands.command()
async def stop(self, ctx):
    global sql, db
    voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
    server_id = ctx.guild.id
    if voice and voice.is_playing():
        global stopped
        stopped = True
        await asyncio.sleep(1)
        voice.stop()
        await asyncio.sleep(1)
        stopped = False
        try:
            sql.execute("SELECT name FROM sqlite_master WHERE type='table';")
            list_of_tables = sql.fetchall()
            if any(f"{server_id}" in word for word in list_of_tables):
                sql.execute(f'DROP TABLE `{server_id}`')
                db.commit()
        except Exception as e:
            print("ERROR FROM STOP CMD:" + str(e))
        await ctx.send('Stopping the music and cleaning the queue.')
    else:
        await ctx.send("I'm not playing music!")

@commands.command()
async def queue(self, ctx):
    global sql, db
    server_id = ctx.guild.id
    try:
        sql.execute(f'SELECT count(*) FROM `{server_id}`')
        number_of_entry = sql.fetchone()[0]
        if number_of_entry == 0:
            await ctx.send("You don't have anything in queue.")
            return
        displayed_all = False
        a = 0
        while not displayed_all:
            a += 1
            sql.execute(f'SELECT * FROM `{server_id}` WHERE number = "{a}"')
            upcomming_info = sql.fetchone()
            if not upcomming_info:
                displayed_all = True
                return
            upcomming_title = upcomming_info[3]
            if a == 1:
                await ctx.send(f"`{a}:` `{upcomming_title}(Currently Playing)`")
            else:
                await ctx.send(f"`{a}:` `{upcomming_title}`")
    except Exception as e:
        print(e)
        await ctx.send("You don't have any music playing or in queue.")

@commands.command()
async def skip(self, ctx):
    # Check if user is in a voice channel
    channel = ctx.author.voice.channel
    if not channel:
        await ctx.send("Gotta connect to a channel my dude.")
        return
    
    # Check if a song is playing
    voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
    if not voice or not voice.is_playing():
        await ctx.send("Need a song at least to skip plz.")
        return
    
    # Stop the song and set skipping flag to True
    global skipping
    skipping = True
    await asyncio.sleep(1)
    voice.stop()
    await asyncio.sleep(1)
    skipping = False

@commands.command()
async def get(self, ctx):
    global sql, db
    try:
        # Get user's last played song from database
        userid = ctx.author.id
        sql.execute(f'SELECT * FROM users WHERE User_ID = {userid}')
        raw_info = sql.fetchone()
        if not raw_info:
            await ctx.author.send("You don't have any history")
            return
        last_song = raw_info[1]
        url = raw_info[2]

        # Search for song info and create an embed to send to the user
        song = self.search(last_song)
        embed = discord.Embed(
            color=discord.Color.random(),
            timestamp=ctx.message.created_at,
            title=f"**♪♪ Last Song Played For You ♪♪**",
            description=f'`{last_song}`\n{url}'
        )
        embed.set_thumbnail(url=song['Image_URL'])
        embed.set_footer(text="Jimbot", icon_url=self.bot.user.avatar.url)
        await ctx.author.send(embed=embed)

    except Exception as e:
        # Handle exceptions
        print(e)

        print(e)
        await ctx.author.send("You don't have any history")
