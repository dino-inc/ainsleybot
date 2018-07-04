import discord
from discord.ext import commands
import aiohttp
import re
import sys
import traceback
from utils.events import Event
from typing import Callable


class BotWEvents(commands.Bot):
    def __init__(self, *args, **kwargs):
        super(BotWEvents, self).__init__(*args, **kwargs)
        self.listeners = Event()

    def add_event(self, func: Callable):
        self.listeners.add_method(func)

    def remove_event(self, name: str):
        self.listeners.remove_method(name)

    def call_event(self, fname: str, *args, **kwargs):
        self.listeners(fname, *args, **kwargs)


description = '''Reaction bot.'''
bot = BotWEvents(command_prefix=';', description=description)


@bot.event
async def on_ready():
    global shitposting
    global memes
    global bestof
    global counter
    global worstof
    global thotchamber
    global owner
    print('Logged in as')
    print(bot.user.name, bot.user.id)
    print('------')
    counter = 0
    owner = 141695444995670017
    guild = 231084230808043522
    memeecon = bot.get_guild(guild)
    shitposting = memeecon.get_channel(300377971234177024)
    memes = memeecon.get_channel(313400507743862794)
    worstof = memeecon.get_channel(395695465955328000)
    bestof = memeecon.get_channel(300792095688491009)
    thotchamber = memeecon.get_channel(438492624207478784)

initial_extensions = ['cogs.rollcall', 'cogs.owner']


if __name__ == '__main__':
    for extension in initial_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            print(f'Failed to load extension {extension}.', file=sys.stderr)
            traceback.print_exc()


@bot.event
async def on_message(message):
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

        if message.channel == thotchamber:
            bot.call_events(message)

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

        if message.channel == memes:
            if message.content != "":
                if message.content.startswith("http") and "/" in message.content and "." in message.content and \
                        " " not in message.content:
                    await message.add_reaction(':upvote:335141910773628928')
                    await message.add_reaction(':downvote:335141916989456384')

                else:
                    try:
                        em = discord.Embed(title='Deleted post', description='Please do not send any text in #memes.'
                                                                             ' Your post, omitting any image, was: '
                                                                             '\n'+message.content+'\n If you believe'
                                                                             ' this to be a mistake, ping dino_inc i'
                                                                             ' #mod_feedback.', colour=0xFF0000)
                        em.set_author(name=message.author, icon_url=message.author.avatar_url)
                        await message.send(embed=em)
                    except:
                        pass
                    await message.delete()
                    print("Deleted text by "+str(message.author)+" in #memes.")
            else:
                await message.add_reaction(':upvote:335141910773628928')
                await message.add_reaction(':downvote:335141916989456384')
    except:
        pass
    await bot.process_commands(message)

@bot.event
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
            if str(x.emoji) == "<:upvote:335141910773628928>":
                upvote = x
            elif str(x.emoji) == "<:downvote:335141916989456384>":
                downvote = x
        try:
            negativevotedifference = downvote.count - upvote.count
        except:
            await message.add_reaction(':upvote:335141910773628928')
            await message.add_reaction(':downvote:335141916989456384')
    if message.channel == voting and negativevotedifference > 5 and emojitest == (335141916989456384):
        await message.delete()
        print("deleted post for negative votes by "+str(message.author))
    if message.channel == voting and emojitest == (335141910773628928):
        await check_votes(message)
    if str(message.id) in open('worstof.txt').read():
        match = True
    if reaction.id == 379319474639208458:
        shitpostreaction = None
        for x in message.reactions:
            if str(x.emoji) == "<:shitpost:379319474639208458>":
                shitpostreaction = x
        if (shitpostreaction.count > 5 and message.channel.name != bestof.name\
                and message.channel.name != worstof.name and match == False) or member == owner:
            # embed message itself
            em = discord.Embed(title='👺 Shitpost 👺', description=message.content, colour=0xFFD700)
            em.set_author(name=message.author.display_name, icon_url=message.author.avatar_url)
            # embed url images
            try:
                attach = message.attachments
                em.set_image(url = attach[0].url)
            except:
                pass
            # writing message id to worstof.txt in order to check for dupes
            cache = open("worstof.txt", "a+",encoding="utf8")
            cache.write(str(message.id) + " ")
            cache.close()

            # sending actual embed
            if member == owner:
                print("Boosted worst_of post by "+str(message.author)+" via executive order.")
            else:
                print("Terrible worst of post by "+str(message.author)+".")
            await worstof.send(embed=em)


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

        if str(i.emoji) == ("<:upvote:335141910773628928>") and i.count > 27 and votearrow.channel != bestof:
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
            em.set_image(url = attach[0].url)
            breakstar = False
        except:
            pass
        if breakstar == True:
            return
        # sending actual embed
        await bestof.send(embed=em)
        print("Sent a good meme to the channel in the sky, by "+str(votearrow.author))
        cache = open("bestof.txt", "a")
        cache.write(str(votearrow.id) + " ")
        cache.close()

# ainsleybot
token = open("token.txt", 'r')
bot.run(token.read(), bot=True, reconnect=True)


