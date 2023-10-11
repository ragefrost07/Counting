import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!!', intents=intents)

counting_game_started = False
counting_channel = None
current_count = None
last_author = None

@bot.event
async def on_ready():
    print(f'Bot is online as {bot.user}')

def has_owner_role(user):
    owner_role = discord.utils.get(user.roles, name="❮👑❯ Owner")
    return owner_role is not None

@bot.command()
async def startcount(ctx):
    global counting_game_started, counting_channel, current_count

    if counting_game_started:
        return

    if not has_owner_role(ctx.author):
        return

    counting_game_started = True
    counting_channel = ctx.channel
    current_count = 28
    await ctx.send("Counting beginnt!")

@bot.command()
async def stopcount(ctx):
    global counting_game_started, counting_channel, current_count

    if not counting_game_started:
        await ctx.send("Das Zählspiel läuft nicht.")
        return

    if not has_owner_role(ctx.author):
        return

    counting_game_started = False

    if current_count is not None:
        await counting_channel.send(f"Counting ist beendet, ihr seid bis zur Zahl {current_count} gekommen. ✅")
    else:
        await counting_channel.send("Counting ist beendet, aber niemand hat etwas gezählt.")

    counting_channel = None
    current_count = None
    last_author = None

@bot.event
async def on_message(message):
    global counting_game_started, counting_channel, current_count, last_author

    if message.author == bot.user:
        return

    if counting_game_started and message.channel == counting_channel:
        try:
            count = int(message.content)
            if count == current_count + 1 and message.author != last_author:
                current_count = count
                await message.add_reaction('✅')  # Add a checkmark reaction for correct answers
                last_author = message.author
            else:
                await message.delete()
        except ValueError:
            await message.delete()

    await bot.process_commands(message)

bot.run('MTE2MTMyODIxOTMyOTQxMzI3Mg.GkxvAb.qQVvmkoJxvMsmsA--veJjM1ii8RWntBqKiBLt8')
