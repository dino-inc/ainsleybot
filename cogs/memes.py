import discord
from discord.ext import commands
import configparser
import os
import sys
import datetime

botconfig = configparser.ConfigParser()
botconfig.read('config.ini')
class Memes(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        global counter
        global owner
        counter = 0
        owner = int(botconfig['GLOBAL']['owner_id'])

    @commands.Cog.listener()
    async def on_ready(self):
        # global shitposting
        global memes
        global bestof
        global worstof
        global memeecon
        global modlog
        if botconfig['GLOBAL'].getboolean('use_test_guild'):
            guild_ids = botconfig['Test Server']
        else:
            guild_ids = botconfig['Meme Economy']
        guild = int(guild_ids['guild_id'])
        memeecon = self.bot.get_guild(guild)
        # shitposting = memeecon.get_channel(int(guild_ids['shitposting_id']))
        memes = memeecon.get_channel(int(guild_ids['memes_id']))
        worstof = memeecon.get_channel(int(guild_ids['worst_of_id']))
        bestof = memeecon.get_channel(int(guild_ids['best_of_id']))
        modlog = memeecon.get_channel(int(guild_ids['mod_log_id']))

    @commands.Cog.listener()
    async def on_message(self, message):
        try:
            # global shitposting
            global memes
            global bestof
            global counter
            global worstof
            try:
                test = message.guild.id
            except:
                return

            if message.channel == memes:
                if message.content != "":
                    if message.content.startswith("http") and "/" in message.content and "." in message.content and \
                            " " not in message.content:
                        await message.add_reaction(botconfig['GLOBAL']['upvote_emoji'])
                        await message.add_reaction(botconfig['GLOBAL']['downvote_emoji'])

                    else:
                        await message.delete()
                        await modlog.send(embed = await mod_log_format("Text in #memes Deleted",
                                                               f'Posted by {message.author}({message.author.id}) at {message.created_at}.',
                                                               0xFF0000,
                                                               datetime.datetime.now()))
                        print("Deleted text by " + str(message.author) + " in #memes.")
                else:
                    await message.add_reaction(botconfig['GLOBAL']['upvote_emoji'])
                    await message.add_reaction(botconfig['GLOBAL']['downvote_emoji'])
        except:
            pass

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, reaction):
        # global shitposting
        global memes
        global bestof
        global counter
        global worstof
        match = False
        reactchannel = memeecon.get_channel(reaction.channel_id)
        message = await reactchannel.fetch_message(reaction.message_id)
        member = memeecon.get_member(reaction.user_id)
        if member == self.bot.user.id:
            return
        voting = memes
        emojitest = reaction.emoji.id
        negativevotedifference = 0
        positivevotedifference = 0

        #Check if reactions in #memes
        if message.channel == voting:
            if member == message.author or str(member.id) in open('blocked.txt').read():
                await message.remove_reaction(reaction.emoji, member)
                return
            for x in message.reactions:
                if str(x.emoji) == "<" + botconfig['GLOBAL']['upvote_emoji'] + ">":
                    upvote = x
                elif str(x.emoji) == "<" + botconfig['GLOBAL']['downvote_emoji'] + ">":
                    downvote = x
            try:
                negativevotedifference = downvote.count - upvote.count
                positivevotedifference = upvote.count - downvote.count
            except:
                await message.add_reaction(botconfig['GLOBAL']['upvote_emoji'])
                await message.add_reaction(botconfig['GLOBAL']['downvote_emoji'])
        if message.channel == voting and negativevotedifference > (int(botconfig['GLOBAL']['downvotes']) - 1) \
                and emojitest == (int(botconfig['GLOBAL']['downvote_emoji_id'])):
            await message.delete()
            print("deleted post for negative votes by " + str(message.author))
            em = await mod_log_format("Terrible Meme Deleted",
                                         f'Posted by {message.author}({message.author.id}) at {message.created_at}.',
                                         0xFF0000,
                                         datetime.datetime.now())
            em = await log_reaction_users(em, reaction)
            await modlog.send(em)

        if message.channel == voting and emojitest == (int(botconfig['GLOBAL']['upvote_emoji_id'])):
            await check_votes(message, positivevotedifference)

        # worst of
        if str(message.id) in open('worstof.txt').read():
            match = True
        if reaction.emoji.id == 379319474639208458:
            shitpostreaction = None
            for x in message.reactions:
                if str(x.emoji) == "<:shitpost:379319474639208458>":
                    shitpostreaction = x
            #makes sure posts aren't ancient
            message_age = datetime.datetime.now() - message.created_at
            if message_age.days > 7:
                print(f"Prevented a message from {message_age} from being starred.")
                #for reaction_emoji in message.reactions:
                    #if reaction.emoji.id == 379319474639208458:
                        #async for users in reaction_emoji.users():
                            #await message.remove_reaction(reaction_emoji, users)
                return
            # removes shitpost star if author is reacting user
            if message.author == message.guild.get_member(member.id):
                react_user = message.guild.get_member(member.id)
                await message.remove_reaction(shitpostreaction, react_user)
                return
            if (shitpostreaction.count > (
                    int(botconfig['GLOBAL']['downstars']) - 1) and message.channel.name != bestof.name \
                    and message.channel.name != worstof.name and message.channel.name != memes.name and match == False):
                # embed message itself
                em = discord.Embed(description=message.content + '\n\n[Jump to post](' + message.jump_url + ')',
                                   colour=0xFF0000, timestamp=message.created_at)
                em.set_author(name='Worst of by: ' + message.author.display_name,
                              icon_url='http://rottenrat.com/wp-content/uploads/2011/01/Marty-Rathbun-anti-sign.jpg',
                              url=message.jump_url)
                em.set_thumbnail(url=message.author.avatar_url)
                em.set_footer(text=f"Posted in #{message.channel.name}")
                # embed url images
                try:
                    em = await(handle_image_embed(em, message))
                except:
                    pass
                # writing message id to worstof.txt in order to check for dupes
                cache = open("worstof.txt", "a+", encoding="utf8")
                cache.write(str(message.id) + " ")
                cache.close()

                # sending actual embed
                print("Terrible worst of post by " + str(message.author) + ".")
                await worstof.send(embed=em)

                em = await mod_log_format("Message Sent To Worst Of",
                                             f'Posted by {message.author}({message.author.id}) at {message.created_at}.',
                                             0xFF0000,
                                             datetime.datetime.now())
                em = await log_reaction_users(em, reaction)
                await modlog.send(em)

        # starboard
        match = False
        if str(message.id) in open('starboard.txt').read():
            match = True
        # checks for the star emoji
        if reaction.emoji.name == '⭐':
            starboardreaction = None
            for x in message.reactions:
                if x.emoji == "⭐":
                    starboardreaction = x
            # removes stars in #memes
            if message.channel == memes:
                react_user = message.guild.get_member(member.id)
                await message.remove_reaction(starboardreaction, react_user)
                return
            # removes star if author is reacting user
            if message.author == message.guild.get_member(member.id):
                react_user = message.guild.get_member(member.id)
                await message.remove_reaction(starboardreaction, react_user)
                return
            # checks if message is more than 1 week old
            message_age = datetime.datetime.now() - message.created_at
            if message_age.days > 7:
                print(f"Prevented a message from {message_age} from being starred.")
                #for reaction_emoji in message.reactions:
                    #if reaction_emoji.emoji == '⭐':
                        #async for users in reaction_emoji.users():
                            #await message.remove_reaction(reaction_emoji, users)
                return
            # checks all of the things to see if it meets best of criteria
            if (starboardreaction.count > (int(botconfig['GLOBAL']['stars']) - 1)
                    and message.channel.name != bestof.name
                    and message.channel.name != worstof.name
                    and match == False
                    and message.channel.name != memes.name):
                # embed message itself
                em = discord.Embed(description=message.content+'\n\n[Jump to post]('+message.jump_url+')',
                                   colour=0xFFD700, timestamp=message.created_at)
                em.set_author(name='Best of by: '+message.author.display_name,
                              icon_url='https://upload.wikimedia.org/wikipedia/commons/f/f3/Star_Emoji.png',
                              url = message.jump_url)
                em.set_thumbnail(url=message.author.avatar_url)
                em.set_footer(text=f"Posted in #{message.channel.name}")
                # em.add_field(name= "[Context]("+message.jump_url+")", value='whatever I guess')
                # embed url images
                try:
                    em = await(handle_image_embed(em, message))
                except:
                    pass
                # writing message id to starboard.txt in order to check for dupes
                cache = open("starboard.txt", "a+", encoding="utf8")
                cache.write(str(message.id) + " ")
                cache.close()

                # sending actual embed
                print("Best of post by " + str(message.author) + ".")
                await bestof.send(embed=em)
                em = await mod_log_format("Message Starred",
                                             f'Posted by {message.author}({message.author.id}) at {message.created_at}.',
                                             0xFFD700,
                                             datetime.datetime.now())
                em = await log_reaction_users(em, reaction)
                await modlog.send(embed=em)

def get_filename_from_cd(cd):
    """
    Get filename from content-disposition
    """
    if not cd:
        return None
    fname = re.findall('filename=(.+)', cd)
    if len(fname) == 0:
        return None
    return fname[0]


async def fetch_img(session, url):
  with aiohttp.Timeout(10):
    async with session.get(url) as response:
      assert response.status == 200
      return await response.read()

async def mod_log_format(event_name, event_message, color, time):
    em = discord.Embed(description=event_message,
                       colour=color,
                       title=event_name)
    return em

async def check_votes(votearrow, positivevotedifference):
    global shitposting
    global memes
    global bestof
    global counter
    global worstof
    voting = memes
    if str(votearrow.id) in open('bestof.txt').read():
        match = True
    else:
        match = False
    if match == True:
        return
    isstar = False
    
    #checking if it's an old meme
    message_age = datetime.datetime.now() - votearrow.created_at
    if message_age.days > 14:
        print(f"Prevented a message from {message_age} from being starred.")
        return

    for i in votearrow.reactions:

        if str(i.emoji) == ("<" + botconfig['GLOBAL']['upvote_emoji'] + ">") and positivevotedifference > (
                int(botconfig['GLOBAL']['upvotes']) - 1) and votearrow.channel != bestof:
            isstar = True
    if isstar == True:

        # embed message itself
        em = discord.Embed(title='A good meme has been located!', colour=0x00FF00,
                           timestamp= votearrow.created_at)
        em.set_author(name=votearrow.author, icon_url=votearrow.author.avatar_url)
        # em.set_thumbnail(url=votearrow.author.avatar_url)
        # em.set_footer(text=f"[Jump to meme]("+votearrow.jump_url+") ")
        # em.set_footer(text='Need context? Click here: '+votearrow.message.jump_url)
        # embed url images
        global breakstar
        breakstar = True
        try:
            if votearrow.content.startswith('https://'):
                em.set_image(url=votearrow.content)
                breakstar = False
        except:
            pass
        try:
            attach = votearrow.attachments
            em = await(handle_image_embed(em, votearrow.message))
            breakstar = False
        except:
            pass
        if breakstar == True:
            return
        # sending actual embed
        await bestof.send(embed=em)
        print("Sent a good meme to the channel in the sky, by " + str(votearrow.author))
        await modlog.send(embed = await mod_log_format("Message Upvoted into #best_of",
                                               f'Posted by {votearrow.author}({votearrow.author.id}) at {votearrow.created_at}.',
                                               0x00FF00,
                                               datetime.datetime.now()))
        cache = open("bestof.txt", "a")
        cache.write(str(votearrow.id) + " ")
        cache.close()

async def handle_image_embed(em, message):
    if len(message.embeds) > 0:
        em.set_image(url=message.embeds[0].url)
    if len(message.attachments) > 0:
        attach_list = ""
        count = 0
        embed_type = ""
        vid_embeddables = (".mp4", ".webm")
        aud_embeddables = (".wav", ".ogg", ".mp3")
        for atta in message.attachments:
            count += 1
            if atta.url.endswith(vid_embeddables):
                embed_type = "Video"
            if atta.url.endswith(aud_embeddables):
                embed_type = "Audio"
            attach_list += f"[{embed_type} Link {count}]({atta.url})\n"
        em.add_field(name="\u200b", value=f"{attach_list}", inline=True)
        em.set_image(url=message.attachments[0].url)
    return em


async def log_reaction_users(em, reaction):
    userlist = await reaction.users().flatten()
    reactionstring = ""
    for user in userlist:
        reactionstring += f" <@{user}>({user.id}) "
    em.add_field(name="\u200b", value=f"Reactors: {reactionstring}", inline=True)
    return em

def setup(bot):
    bot.add_cog(Memes(bot))
