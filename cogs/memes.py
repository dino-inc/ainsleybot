import discord
from discord.ext import commands
import configparser
import os
import sys


class Memes:
    def __init__(self, bot):
        self.bot = bot
        botconfig = configparser.ConfigParser()
        botconfig.read('config.ini')
        global shitposting
        global memes
        global bestof
        global counter
        global worstof
        global memeecon
        global owner
        counter = 0
        owner = int(botconfig['GLOBAL']['owner_id'])
        if botconfig['GLOBAL'].getboolean('use_test_guild'):
            guild_ids = botconfig['Test Server']
        else:
            guild_ids = botconfig['Meme Economy']
        guild = int(guild_ids['guild_id'])
        memeecon = self.bot.get_guild(guild)
        shitposting = memeecon.get_channel(guild_ids['shitposting_id'])
        memes = memeecon.get_channel(guild_ids['memes_id'])
        worstof = memeecon.get_channel(guild_ids['worst_of_id'])
        bestof = memeecon.get_channel(guild_ids['best_of_id'])

    async def on_message(self, message):
        try:
            global shitposting
            global memes
            global bestof
            global counter
            global worstof
            try:
                test = message.guild.id
            except:
                return
            # shitposters reaction code
            '''
            if message.channel == shitposting:
                ainsleybot = ['🇦', '🇮', '🇳', '🇸', '🇱', '🇪', '🇾']
                if message.guild.id == 231084230808043522:
                    ainsleybot = [':spicyoil:331582837025406976', ':dab:310682824749350913'] + ainsleybot
                else:
                    ainsleybot = ['🇸', '🇸'] + ainsleybot
                if counter < len(ainsleybot) - 1:
                    counter += 1
                else:
                    counter = 0
                await message.add_reaction(ainsleybot[counter])
    '''
            if message.channel == memes:
                if message.content != "":
                    if message.content.startswith("http") and "/" in message.content and "." in message.content and \
                            " " not in message.content:
                        await message.add_reaction(botconfig['GLOBAL']['upvote_emoji'])
                        await message.add_reaction(botconfig['GLOBAL']['downvote_emoji'])

                    else:
                        try:
                            em = discord.Embed(title='Deleted post',
                                               description='Please do not send any text in #memes.'
                                                           ' Your post, omitting any image, was: '
                                                           '\n' + message.content + '\n If you believe'
                                                                                    ' this to be a mistake, ping dino_inc i'
                                                                                    ' #mod_feedback.', colour=0xFF0000)
                            em.set_author(name=message.author, icon_url=message.author.avatar_url)
                            # await message.send(embed=em)
                        except:
                            pass
                        await message.delete()
                        print("Deleted text by " + str(message.author) + " in #memes.")
                else:
                    await message.add_reaction(botconfig['GLOBAL']['upvote_emoji'])
                    await message.add_reaction(botconfig['GLOBAL']['downvote_emoji'])
        except:
            pass

    async def on_raw_reaction_add(reaction, messageid, channelid, member):
        global shitposting
        global memes
        global bestof
        global counter
        global worstof
        match = False
        reactchannel = bot.get_channel(channelid)
        message = await reactchannel.get_message(messageid)
        if member == bot.user.id:
            return
        voting = memes
        emojitest = reaction.id
        negativevotedifference = 0
        positivevotedifference = 0
        if message.channel == voting:
            for x in message.reactions:
                if str(x.emoji) == "<" + botconfig['GLOBAL']['upvote_emoji'] + ">":
                    upvote = x
                elif str(x.emoji) == "<" + botconfig['GLOBAL']['downvote_emoji'] + ">":
                    downvote = x
            try:
                negativevotedifference = downvote.count - upvote.count
            except:
                await message.add_reaction(botconfig['GLOBAL']['upvote_emoji'])
                await message.add_reaction(botconfig['GLOBAL']['downvote_emoji'])
        if message.channel == voting and negativevotedifference > (int(botconfig['GLOBAL']['downvotes']) - 1) \
                and emojitest == (int(botconfig['GLOBAL']['downvote_emoji_id'])):
            await message.delete()
            print("deleted post for negative votes by " + str(message.author))
        if message.channel == voting and emojitest == (int(botconfig['GLOBAL']['upvote_emoji_id'])):
            await check_votes(message)
        # worst of
        if str(message.id) in open('worstof.txt').read():
            match = True
        if reaction.id == 379319474639208458:
            shitpostreaction = None
            for x in message.reactions:
                if str(x.emoji) == "<:shitpost:379319474639208458>":
                    shitpostreaction = x
            if (shitpostreaction.count > (
                    int(botconfig['GLOBAL']['downstars']) - 1) and message.channel.name != bestof.name \
                    and message.channel.name != worstof.name and message.channel.name != memes.name and match == False):
                # embed message itself
                em = discord.Embed(title=f'👺 Shitpost From {message.channel.name} 👺', description=message.content,
                                   colour=0xFFD700)
                em.set_author(name=message.author.display_name, icon_url=message.author.avatar_url)
                # embed url images
                try:
                    attach = message.attachments
                    em.set_image(url=attach[0].url)
                except:
                    pass
                # writing message id to worstof.txt in order to check for dupes
                cache = open("worstof.txt", "a+", encoding="utf8")
                cache.write(str(message.id) + " ")
                cache.close()

                # sending actual embed
                print("Terrible worst of post by " + str(message.author) + ".")
                await worstof.send(embed=em)
        match = False
        # starboard
        if str(message.id) in open('starboard.txt').read():
            match = True
        if reaction.name == '⭐':
            starboardreaction = None
            for x in message.reactions:
                if x.emoji == "⭐":
                    starboardreaction = x
            if message.channel == memes:
                react_user = message.guild.get_member(member)
                message.remove_reaction(starboardreaction, react_user)
            if (starboardreaction.count > (
                    int(botconfig['GLOBAL']['stars']) - 1) and message.channel.name != bestof.name\
                    and message.channel.name != worstof.name and match == False and message.channel.name != memes.name):
                # embed message itself
                em = discord.Embed(title=f'⭐ Best Of From {message.channel.name}⭐', description=message.content,
                                   colour=0xFFD700)
                em.set_author(name=message.author.display_name, icon_url=message.author.avatar_url)
                # embed url images
                try:
                    attach = message.attachments
                    em.set_image(url=attach[0].url)
                except:
                    pass
                # writing message id to starboard.txt in order to check for dupes
                cache = open("starboard.txt", "a+", encoding="utf8")
                cache.write(str(message.id) + " ")
                cache.close()

                # sending actual embed
                print("Best of post by " + str(message.author) + ".")
                await bestof.send(embed=em)

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


async def check_votes(votearrow):
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

    for i in votearrow.reactions:

        if str(i.emoji) == ("<" + botconfig['GLOBAL']['upvote_emoji'] + ">") and i.count > (
                int(botconfig['GLOBAL']['upvotes']) - 1) and votearrow.channel != bestof:
            isstar = True
    if isstar == True:

        # embed message itself
        em = discord.Embed(title='👌Good meme👌', description='This meme has received enough upvotes'
                                                              ' to become certified™ dank.', colour=0x00FF00)
        em.set_author(name=votearrow.author, icon_url=votearrow.author.avatar_url)
        em.set_footer(text="All hail dino_inc, the creator of this bot. Feel free to give feedback by pinging him.")
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
            em.set_image(url=attach[0].url)
            breakstar = False
        except:
            pass
        if breakstar == True:
            return
        # sending actual embed
        await bestof.send(embed=em)
        print("Sent a good meme to the channel in the sky, by " + str(votearrow.author))
        cache = open("bestof.txt", "a")
        cache.write(str(votearrow.id) + " ")
        cache.close()

def setup(bot):
    bot.add_cog(Memes(bot))
