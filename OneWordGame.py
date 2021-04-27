import asyncio
import discord
from discord import *
from discord.ext import commands

OneWord = commands.Bot(command_prefix=">")
WORD = ""
old_author = 0
list_of_reactions = ["🇼", "🇴", "🇷", "🇩"]
list_of_reactions_help = ["🇬", "🇦", "🇲", "🇪", "🇴", "🇳"]


@OneWord.event
async def on_ready():
    CHANNEL = OneWord.get_channel('Channel id as an int')
    game = discord.Game("OneWordGame channel | ~help")
    await OneWord.change_presence(status=discord.Status.online, activity=game)
    await CHANNEL.send("Game reset! It is now ready to go!")
    print("ready")


@OneWord.event
async def on_message(message):
    global WORD
    global old_author
    global list_of_reactions
    global list_of_reactions_help
    CHANNEL = OneWord.get_channel('Channel id as an int')

    #Purge command only accessible for a specifed user that goes by ~c int
    if message.author.id == 'user id as an int':
        if message.content.lower().startswith("~c"):
            try:
                clear = int(message.content.split()[1])
            except:
                return
            await message.channel.purge(limit=clear + 1)
            return

    if message.channel.id == 'Channel Id as an int':
        user_word = message.content.split()

        if message.author == OneWord.user:
            return

        #Makes sure that the user can't subit a gif
        if message.content.lower().startswith("http") or message.content.lower().startswith("https://"):
            return

        # Send help screen to user
        if message.content.lower().startswith("~help"):
            msg = await message.author.send(embed=BotHelp())
            for reactions in list_of_reactions_help:
                await msg.add_reaction(emoji=reactions)
            return

        # Resets the bot if the specifed user says so
        if message.content.lower().startswith("~r") and message.author.id == 'user id as an int':
            await asyncio.sleep(1)
            await message.delete()
            WORD = ""
            old_author = 0
            return

        # Paste the help screen in the channel if the user specified user types command
        if message.content.lower().startswith("~p") and message.author.id == 'user id as an int':
            await asyncio.sleep(1)
            await message.delete()
            msg = await CHANNEL.send(embed=BotHelp())
            for reactions in list_of_reactions_help:
                await msg.add_reaction(emoji=reactions)
            return

        # ~end will print the word built from the users
        # This is a process of cleaning up the sentence and sending it off. 
        if message.content.lower().startswith("~end"):
            await message.add_reaction(emoji='✅')
            proper_word = []
            temp_word = WORD.split()
            if len(temp_word) >= 1:
                for i in range(len(temp_word) - 1):
                    if temp_word[i] != temp_word[i + 1]:
                        proper_word.append(temp_word[i])
                proper_word.append(temp_word[len(temp_word) - 1])
                if proper_word[len(proper_word) - 1].endswith(".") or proper_word[len(proper_word) - 1].endswith("!") or proper_word[len(proper_word) - 1].endswith("?"):
                    pass
                else:
                    proper_word[len(proper_word) - 1] += "."
                WORD = proper_word[0].capitalize()
                for i in range(1, len(proper_word)):
                    WORD += " " + proper_word[i]
            msg = await CHANNEL.send(
                "----------------------------------------\n" + WORD + "\n----------------------------------------")
            WORD = ""
            old_author = 0
            for reactions in list_of_reactions:
                await msg.add_reaction(emoji=reactions)
            return

        # Ensures the same user type a word more than once until another goes after
        # Will delete words if the author is the same as the old author, and delete sentences
        if message.author.id != old_author:
            if len(user_word) == 1:
                if user_word[0] == "," or user_word[0] == "!" or user_word[0] == "?" or user_word[0] == ".":
                    WORD += user_word[0]
                elif WORD == "":
                    WORD += user_word[0].capitalize()
                else:
                    WORD += " " + user_word[0]
                old_author = message.author.id
                await message.add_reaction(emoji='✅')
                return
            else:
                await asyncio.sleep(1)
                await message.delete()
        else:
            await asyncio.sleep(1)
            await message.delete()

    await OneWord.process_commands(message)


def BotHelp():
    embed = Embed(
        title="One Word Game",
        description="Hello, I'm One Word,\nI'm a game that will create a random sentence or sentences through the words inputted amongst the people of this server.",
        colour=colour.Colour.blue()
    )
    embed.add_field(name="Command ~help", value="I will DM you the game description and the rules", inline=False)
    embed.add_field(name="Command ~end", value="I'll send out what the channel as made", inline=False)
    embed.add_field(name="Adding Words To The Game",
                    value="For me to take a word, you must only submit 1 word in the message box and it can be anything. \n However, each user can only add 1 word and wait until someone else inputs a word",
                    inline=False)
    embed.add_field(name="Duplicates",
                    value="When you submit using ~d, any two same words after another in a sentence like 'I I Will...' will be removed to make 'I will'",
                    inline=False)
    embed.add_field(name="HAVE FUN",
                    value="I hope this game was simple enough to understand. HAVE FUN",
                    inline=False)
    return embed

OneWord.run("Token")
