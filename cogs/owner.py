from discord.ext import commands


# mostly not my code, stolen from cogs example because lazy

class OwnerCog:

    def __init__(self, bot):
        self.bot = bot

    # Hidden means it won't show up on the default help.
    @commands.command(name='load', hidden=True)
    @commands.is_owner()
    async def cog_load(self, ctx, *, cog: str):
        """Command which Loads a Module.
        Remember to use dot path. e.g: cogs.owner"""

        try:
            self.bot.load_extension(cog)
        except Exception as e:
            await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}')
        else:
            await ctx.send('**`SUCCESS`**')
            print('loaded module '+cog)

    @cog_load.error
    async def cog_load_error(self, ctx, error):
        if isinstance(error, commands.errors.CheckFailure):
            await ctx.send("You are not the owner of this bot.")
        else:
            await ctx.send("Could not load; {0}.".format(error))


    @commands.command(name='unload', hidden=True)
    @commands.is_owner()
    async def cog_unload(self, ctx, *, cog: str):
        """Command which Unloads a Module.
        Remember to use dot path. e.g: cogs.owner"""

        try:
            self.bot.unload_extension(cog)
        except Exception as e:
            await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}')
        else:
            await ctx.send('**`SUCCESS`**')
            print('unloaded module ' + cog)

    @cog_unload.error
    async def cog_load_error(self, ctx, error):
        if isinstance(error, commands.errors.CheckFailure):
            await ctx.send("You are not the owner of this bot.")
        else:
            await ctx.send("Could not unload; {0}.".format(error))


    @commands.command(name='reload', hidden=True)
    @commands.is_owner()
    async def cog_reload(self, ctx, *, cog: str):
        """Command which Reloads a Module.
        Remember to use dot path. e.g: cogs.owner"""

        try:
            self.bot.unload_extension(cog)
            self.bot.load_extension(cog)
        except Exception as e:
            await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}')
        else:
            await ctx.send('**`SUCCESS`**')
            print('reloaded module ' + cog)

    @cog_reload.error
    async def cog_load_error(self, ctx, error):
        if isinstance(error, commands.errors.CheckFailure):
            await ctx.send("You are not the owner of this bot.")
        else:
            await ctx.send("Could not reload; {0}.".format(error))


def setup(bot):
    bot.add_cog(OwnerCog(bot))