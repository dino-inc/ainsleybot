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
        super().__init__(*args, **kwargs)
        self.listeners = Event()

    def add_event(self, func: Callable):
        self.listeners.add_method(func)

    def has_event(self, name: str):
        return name in self.listeners

    def remove_event(self, name: str):
        self.listeners.remove_method(name)

    async def call_event(self, fname: str, *args, **kwargs):
        await self.listeners(fname, *args, **kwargs)


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
    global memeecon
    global banned_role
    global yandere
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
    yandere = memeecon.get_channel(468474666718199838)
    banned_role = discord.utils.get(memeecon.roles, name='banned from stream')


initial_extensions = ['cogs.rollcall', 'cogs.owner']


if __name__ == '__main__':
    for extension in initial_extensions:
        print(f'Loading {extension}.')
        try:
            bot.load_extension(extension)
            print('Finished loading.')
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
            await bot.call_event("during_call", message)

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
    banned_words = ['candlejack', 'candle jack', 'l-a-g', 'l a g', 'lag?', 'lag ', ' lag', 'laggy', 'l.ag', 'l.a.g',
                    'lagged', 'Iagging', 'lagging', 'l4gging', 'lagy', 'laag', 'laaag', 'laaaag', 'laaaaag', 'lagg',
                    'laggg',
                    'lagggg', 'laggggg', 'implying', 'lmplying', '1mplaying', 'in before', 'inb4', 'in-b4', 'in b4',
                    'in b 4',
                    'ib4 ', 'cool story', 'coolstory', 'doom3', 'doom 3', 'd00m 3', 'doom three', 'plz ', ' plz',
                    'pl0x',
                    'plox', 'should of', 'could of', 'would of', 'must of', 'could care less', 'halo invented',
                    'oscar mike',
                    'ramirez', 'nigger', 'nlgger', 'n1gger', 'n|gger', 'faggot', 'fagget', 'faggotry', 'protip',
                    'brotip', 'tldr', 'tl;dr', 'i am 12', 'im 12', 'i\'m 12', 'you dead', 'you ded', 'u dead', 'u ded',
                    'do et',
                    'do eet', 'do eet', 'doo eet', 'du et', 'wut.', 'wat.', 'lol wut', 'lol wat', 'lag']

    if message.channel == yandere:
        for word in banned_words:
            if banned_role in message.author.roles:
                await message.delete()
            elif word in message.content or word in message.content.lower():
                await message.channel.send(f'Forcibly removing {message.author.display_name} for using a banned word.')
                await message.author.add_roles(banned_role)
                break
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
# worst of
    if str(message.id) in open('worstof.txt').read():
        match = True
    if reaction.id == 379319474639208458:
        shitpostreaction = None
        for x in message.reactions:
            if str(x.emoji) == "<:shitpost:379319474639208458>":
                shitpostreaction = x
        if (shitpostreaction.count > 5 and message.channel.name != bestof.name\
                and message.channel.name != worstof.name and message.channel.name != memes.name and match == False):
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
            print("Terrible worst of post by "+str(message.author)+".")
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
        if (starboardreaction.count > 6 and message.channel.name != bestof.name\
                and message.channel.name != worstof.name and match == False):
            # embed message itself
            em = discord.Embed(title='⭐ Best Of ⭐', description=message.content, colour=0xFFD700)
            em.set_author(name=message.author.display_name, icon_url=message.author.avatar_url)
            # embed url images
            try:
                attach = message.attachments
                em.set_image(url = attach[0].url)
            except:
                pass
            # writing message id to starboard.txt in order to check for dupes
            cache = open("starboard.txt", "a+",encoding="utf8")
            cache.write(str(message.id) + " ")
            cache.close()

            # sending actual embed
            print("Best of post by "+str(message.author)+".")
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

        if str(i.emoji) == ("<:upvote:335141910773628928>") and i.count > 34 and votearrow.channel != bestof:
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


