import discord
from discord.ext import commands
import sqlite3
import asyncio

class RollCall:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def add(self, ctx, member : discord.Member):
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
        con.commit()
        con.close()

    @add.error
    async def add_error(self, ctx, error):
        await ctx.send(error)

    @commands.command()
    async def remove(self, ctx, member : discord.Member):
        con = sqlite3.connect('members.db')
        c = con.cursor()
        id = member.id
        c.execute("DELETE FROM members WHERE member_id=(?)", (id,))
        await ctx.send('Succesfully removed **{}**'.format(member.display_name))
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
    async def call(self, ctx, time = None):
        role = discord.utils.get(ctx.guild.roles, id=438521521166876692)
        if role not in ctx.author.roles:
            await ctx.send('Only the Chamber Speaker can use this commmand')
            return
        con = sqlite3.connect('members.db')
        c = con.cursor()
        for i in c.execute('SELECT * FROM members'):
            await ctx.send('Mr <@{}>'.format(str(i[0])))
            print(i[0])
        if time == None:
            pass
        else:
            await ctx.send('***You have {} minutes. The clock is on.***'.format(time))
            minutes = int(time) * 60
            await asyncio.sleep(minutes)
            await ctx.send('***Voting time is up. Is there anyone who would like to cast or change a vote?***')
            await asyncio.sleep(60)
            await ctx.send('***All votes are now final***')
        con.commit()
        con.close()

    @call.error
    async def call_error(self, ctx, error):
        await ctx.send(error)

def setup(bot):
    bot.add_cog(RollCall(bot))