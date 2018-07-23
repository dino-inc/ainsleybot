from discord.ext import commands
import discord


class YandereSimulator:
    def __init__(self, bot):
        self.bot = bot
        self.banned_words = ['candlejack', 'candle jack', 'l-a-g', 'l a g', 'lag?', 'lag ', ' lag', 'laggy', 'l.ag', 'l.a.g',
                    'lagged','Iagging', 'lagging', 'l4gging', 'lagy', 'laag', 'laaag', 'laaaag', 'laaaaag', 'lagg', 'laggg',
                    'lagggg','laggggg', 'implying', 'lmplying', '1mplaying', 'in before', 'inb4', 'in-b4', 'in b4', 'in b 4',
                    'ib4 ','cool story', 'coolstory', 'doom3', 'doom 3', 'd00m 3', 'doom three', 'plz ', ' plz', 'pl0x',
                    'plox','should of', 'could of', 'would of', 'must of', 'could care less', 'halo invented', 'oscar mike',
                    'ramirez', 'nigger', 'nlgger', 'n1gger', 'n|gger', 'faggot', 'fagget', 'faggotry', 'protip',
                    'brotip','tldr', 'tl;dr', 'i am 12', 'im 12', 'i\'m 12', 'you dead', 'you ded', 'u dead', 'u ded', 'do et',
                    'do eet', 'do eet', 'doo eet', 'du et', 'wut.', 'wat.', 'lol wut', 'lol wat']
        guild = 231084230808043522
        memeecon = self.bot.get_channel(guild)
        self.banned_role = discord.utils.get(memeecon.roles, name='banned from stream')
        self.yandere = memeecon.get_channel(468474666718199838)


    async def on_message(self, message):
        if message.channel == self.yandere:
            for word in banned_words:
                if word in message.content:
                    await message.channel.send(f'Forcibly removing {message.display_name} for using a banned word.')
                    await message.author.add_roles(self.banned_role)
                    break


def setup(bot):
    bot.add_cog(YandereSimulator(bot))
