import discord
from discord.ext import commands
import sqlite3
import json
import datetime
import re
import asyncio
import os
from keep_alive import keep_alive
keep_alive()

# Charger la configuration
with open('config.json') as f:
    config = json.load(f)
token = os.environ.get("token")
prefix = config["prefix"]

intents = discord.Intents.all()
bot = commands.Bot(command_prefix=commands.when_mentioned_or(prefix), intents=intents)
bot.remove_command('help')

# Configuration de la base de données
conn = sqlite3.connect('db.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS prevnames (user_id TEXT, timestamp INTEGER, username TEXT)''')
conn.commit()

@bot.event
async def on_ready():
    print(f'connecté en tant que {bot.user.name}')

@bot.event
async def on_user_update(before, after):
    if before.name != after.name:
        timestamp = int(datetime.datetime.now().timestamp())
        c.execute('INSERT INTO prevnames (user_id, timestamp, username) VALUES (?, ?, ?)', (before.id, timestamp, after.name))
        conn.commit()
        print(f'{before.name} => {after.name}')

@bot.command()
@commands.has_permissions(administrator=True)
async def clear(ctx):
    user_id = str(ctx.author.id)
    c.execute('DELETE FROM prevnames WHERE user_id = ?', (user_id,))
    conn.commit()
    await ctx.send(f'Tous les anciens pseudos ont été supprimés de votre historique.')

@clear.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("Vous n'avez pas la permission d'utiliser cette commande.")

@bot.command()
async def prevname(ctx, user: discord.User = None):
    user = user or ctx.author

    c.execute('SELECT timestamp, username FROM prevnames WHERE user_id = ? ORDER BY timestamp DESC', (str(user.id),))
    data = c.fetchall()
    
    if not data:
        await ctx.send("Aucune donnée trouvée")
        return

    entries_per_page = 15
    total_pages = (len(data) + entries_per_page - 1) // entries_per_page
    pages = [data[i:i+entries_per_page] for i in range(0, len(data), entries_per_page)]

    def create_embed(page_index):
        embed = discord.Embed(title=f'Ancien pseudo de - {user.name}', color=0xF10303)
        embed.set_footer(text=f'Page {page_index + 1}/{total_pages}', icon_url=user.avatar.url)
        embed.set_thumbnail(url=user.avatar.url)
        page_data = pages[page_index]
        embed.description = '\n'.join([f"**<t:{timestamp}>** - **{username}**" for timestamp, username in page_data])
        return embed

    current_page = 0
    message = await ctx.send(embed=create_embed(current_page))

    if total_pages > 1:
        await message.add_reaction('◀')
        await message.add_reaction('▶')

        def check(reaction, user_react):
            return user_react == ctx.author and str(reaction.emoji) in ['◀', '▶'] and reaction.message.id == message.id

        while True:
            try:
                reaction, user_react = await bot.wait_for('reaction_add', timeout=300.0, check=check)

                if str(reaction.emoji) == '▶':
                    if current_page < total_pages - 1:
                        current_page += 1
                        await message.edit(embed=create_embed(current_page))
                elif str(reaction.emoji) == '◀':
                    if current_page > 0:
                        current_page -= 1
                        await message.edit(embed=create_embed(current_page))

                await message.remove_reaction(reaction, user_react)

            except asyncio.TimeoutError:
                break

@bot.command()
async def help(ctx):
    embed = discord.Embed(title="Aide - Liste des commandes", color=0xF10303)
    embed.set_thumbnail(url=ctx.author.avatar.url)
    embed.set_footer(text=f"Demandé par {ctx.author}", icon_url=ctx.author.avatar.url)
    
    embed.add_field(name=f"{prefix}clear", value="Supprime tous les anciens pseudonymes de votre historique.", inline=False)
    embed.add_field(name=f"{prefix}prevname [user]", value="Affiche la liste des anciens pseudonymes de l'utilisateur mentionné ou de vous-même si aucun utilisateur n'est mentionné.", inline=False)

    await ctx.send(embed=embed)

def escape_regex(text):
    return re.escape(text)

bot.run(token)
