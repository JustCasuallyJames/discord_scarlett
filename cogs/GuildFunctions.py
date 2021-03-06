import discord
from discord.ext import commands

import json


class GuildFunctions(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["changeprefix"])
    @commands.has_role("Moderators")
    async def change_prefix(self, ctx, prefix):
        with open('cogs/prefixes.json', 'r') as f:
            prefixes = json.load(f)

        if len(prefix) == 1:
            prefixes[str(ctx.guild.id)] = prefix
        else:
            await ctx.send("You can't put a prefix that's more than one character!")

        with open('cogs/prefixes.json', 'w') as f:
            json.dump(prefixes, f, indent=4)
        embed = discord.Embed(
            description=f"The changed prefix is: {prefixes[str(ctx.guild.id)]}",
            colour=discord.Colour.purple()
        )
        await ctx.send(embed=embed)

    @commands.command(aliases=["addrole"])
    @commands.has_role("Moderators")
    # The * causes role to hold the user input text after the member name, including any interior whitespace.
    # This lets the user write the following to add the "My Little Pony" role to hogarth: .addrole @hogarth My Little Pony
    async def add_roles(self, ctx, member: discord.Member, *, role: discord.Role):
        await member.add_roles(role)
        embed = discord.Embed(
            title="**Role added**",
            description=f"{member.mention} awarded the **{role}** role",
            colour=discord.Colour.red()
        )
        await ctx.send(embed=embed)

    @commands.command(aliases=["delrole"])
    @commands.has_role("Moderators")
    async def del_roles(self, ctx, member: discord.Member, *, role: discord.Role):
        await member.remove_roles(role)
        embed = discord.Embed(
            title="**Role deleted**",
            description=f"{role} role has been revoked from {member.mention}",
            colour=discord.Colour.red()
        )
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(GuildFunctions(client))
