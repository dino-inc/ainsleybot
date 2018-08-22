import discord
from discord.ext import commands
import sqlite3
import asyncio
import re
from collections import Counter


class RollCall:
    FOR = "aye|yeet|jeff|yea"
    AGAINST = "nay|nae|gay"
    NEUTRAL = "abstain|present"
    FAVORS = (FOR, AGAINST, NEUTRAL)
    ANY = "|".join(FAVORS)

    def __init__(self, bot):
        self.bot = bot
        self.voting = {}
        self.quorum_size = 0

    async def end_motion(self, sender):
        votes = Counter(self.voting.values())
        yeas = votes[RollCall.FOR]
        nays = votes[RollCall.AGAINST]
        abst = votes[RollCall.NEUTRAL]
        votestatus = "agreed to" if yeas > nays else "denied"
        abststatus = f" with {abst} abstentions" if abst > 0 else ""
        m = f"The Yeas and Nays are {yeas} - {nays}{abststatus}.  The motion is {votestatus}."
        await sender(m)
        self.voting = {}
        self.bot.remove_event(self.during_call.__name__)

    def meets_quorum(self):
        return len(self.voting.keys()) >= self.quorum_size

    def active_motion(self):
        return self.bot.has_event(self.during_call.__name__)

    async def during_call(self, message: discord.Message):
        def exists(regex):
            return re.search(regex, message.content, re.IGNORECASE) is not None

        if self.meets_quorum():
            return

        if exists(RollCall.ANY):
            user = message.author.id
            if user == self.bot.user.id:
                return
            for favor in RollCall.FAVORS:
                if exists(favor):
                    self.voting[user] = favor
            if self.meets_quorum():
                await self.end_motion(message.channel.send)

    @commands.command()
    async def add(self, ctx, member: discord.Member):
        con = sqlite3.connect('members.db')
        c = con.cursor()
        id = member.id
        '''try:
            c.execute('SELECT * FROM members WHERE member_id=(?)', (id,))
            await ctx.send('Member <@{}> is already a member.'.format(id))
        except:'''
        try:
            c.execute('INSERT INTO members VALUES(?)', (id,))
            await ctx.send('Succesfully added **{}**'.format(member.display_name))
        except:
            c.execute('''CREATE TABLE members
                         (member_id)''')
            c.execute('INSERT INTO members VALUES (?)', (id,))
            await ctx.send('Succesfully added **{}**'.format(member.display_name))
        role = discord.utils.get(ctx.guild.roles, id=438492778134110218)
        if role not in member.roles:
                await member.add_roles(role)
        con.commit()
        con.close()

    @add.error
    async def add_error(self, ctx, error):
        await ctx.send(error)

    @commands.command()
    async def remove(self, ctx, member: discord.Member):
        con = sqlite3.connect('members.db')
        c = con.cursor()
        id = member.id
        c.execute("DELETE FROM members WHERE member_id=(?)", (id,))
        await ctx.send('Successfully removed **{}**'.format(member.display_name))
        role = discord.utils.get(ctx.guild.roles, id=438492778134110218)
        if role in member.roles:
                await member.remove_roles(role)
        con.commit()
        con.close()

    @remove.error
    async def remove_error(self, ctx, error):
        await ctx.send(error)

    @commands.command()
    async def list(self, ctx):
        con = sqlite3.connect('members.db')
        c = con.cursor()
        for i in c.execute('SELECT * FROM members'):
            thot = discord.utils.get(ctx.guild.members, id=i[0])
            print(i[0])
            try:
                await ctx.send(thot)
            except:
                pass

    @commands.command()
    async def call(self, ctx, time=None):
        role = discord.utils.get(ctx.guild.roles, id=438521521166876692)
        if role not in ctx.author.roles:
            await ctx.send('Only the Chamber Speaker can use this commmand')
            return
        con = sqlite3.connect('members.db')
        c = con.cursor()
        # Will determine initial quorum size
        qcounter = 0
        rtext = ""
        for i in c.execute('SELECT * FROM members'):
            rtext += 'Mr <@{}>\n'.format(str(i[0]))
            qcounter = qcounter + 1
            print(i[0])
        await ctx.send(rtext)
        self.quorum_size = qcounter
        self.bot.add_event(self.during_call)
        self.voting = {}
        if time is not None:
            await ctx.send('***You have {} minutes. The clock is on.***'.format(time))
            minutes = int(time) * 60
            await asyncio.sleep(minutes)
            if self.active_motion():
                self.quorum_size = int(self.quorum_size / 2)
                nvotes = len(self.voting.keys())
                await ctx.send(f'***Quorum is now reduced to {self.quorum_size}. There are currently {nvotes} votes. '
                               'Is there anyone who would like to cast or change a vote?***')
                await asyncio.sleep(60)
                if self.meets_quorum() and self.active_motion():
                    await self.end_motion(ctx.send)
                # await ctx.send('***All votes are now final***')
        con.commit()
        con.close()

    @commands.command()
    async def purge(self, ctx):
        role = discord.utils.get(ctx.guild.roles, id=438521521166876692)
        if role not in ctx.author.roles:
            await ctx.send('Only the Chamber Speaker can use this commmand')
            return
        con = sqlite3.connect('members.db')
        c = con.cursor()
        for i in c.execute('SELECT * FROM members'):
            if ctx.guild.get_member(i[0]) is None:
                c.execute("DELETE FROM members WHERE member_id=(?)", (i[0],))
                await ctx.send('Automatically removed <@{}> for no longer being in the server.'.format(i[0]))
        con.commit()
        con.close()

    @commands.command()
    async def getvotes(self, ctx):
        counter = 0
        rtext = ""
        votes = Counter(self.voting.values())
        yeas = votes[RollCall.FOR]
        nays = votes[RollCall.AGAINST]
        abst = votes[RollCall.NEUTRAL]
        for k in self.voting:
            response = {RollCall.FOR: "For", RollCall.AGAINST: "Against", RollCall.NEUTRAL: "Abstain"}
            v = self.voting[k]
            if v is None:
                continue
            rtext += f"{ctx.guild.get_member(k).display_name}: {response[v]}\n"
            counter = counter + 1
        if not self.active_motion():
            await ctx.send("No motion is on the table.")
        elif counter == 0:
            await ctx.send("No one has voted.")
        else:
            await ctx.send(f"The Yeas and Nays are currently {yeas} - {nays} with {abst} abstentions.\n"+rtext)

    @commands.command()
    async def endvoting(self, ctx):
        if self.active_motion():
            await self.end_motion(ctx.send)
        else:
            await ctx.send("No motion is on the table.")

    @call.error
    async def call_error(self, ctx, error):
        await ctx.send(error)


def setup(bot):
    bot.add_cog(RollCall(bot))
