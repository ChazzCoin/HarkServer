import discord
from FSON import DICT
# from harkConfig import config
from CLI import Commands
from DiscordSays import Say
from fairNLP import Regex
from FLog.LOGGER import Log
import harkDB
from Jarticle import jArticleProvider as jap
Log = Log("TiffanyBot")
client = discord.Client()
arts_db = harkDB.collectionArticles
Say = Say()

@client.event
async def on_ready():
    print( 'We have logged in as {0.user}'.format( client ) )

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    mess = message.content
    chan = message.channel
    user = message.author
    Log.i(f"\n---------\nChannel: {chan}\nUser: {user}\nMessage: {mess}\n---------\n")

    mess = str(mess).lower()

    if mess == "tiffany?":
        await message.channel.send("Yes?")

    if mess == "is michael gay?":
        await message.channel.send("Without a doubt.")

    if mess == "article count!":
        count = jap.get_article_count()
        await message.channel.send(f"Article Count: [ {count} ] ")

    if mess.startswith("--"):
        parse_command = Commands.parse_commands(mess)
        await handle_commands(message, parse_command)
    # -> [ BITCH ]
    # if mess.startswith("--bitch"):
    #     if str(mess).__contains__("pdf"):
    #         await message.channel.send(file=discord.File('/Users/chazzromeo/ChazzCoin/export/programming.pdf'))

async def handle_commands(message, commands: dict):
    for directory_command in commands.keys():
        directory_phrase = commands[directory_command]
        if directory_command == '--search':
            filter_commands = get_filters(directory_command, commands)
            q = Commands.build_query(directory_phrase, filter_commands)
            results = base_search(q)
            return await return_results(message, results)
        elif directory_command == "--info" or directory_command == "--help" or directory_command == "?":
            filter_commands = get_filters(directory_command, commands)
            if Regex.contains("article count", directory_phrase):
                return await send(message, arts_db.get_document_count())
            commands = Commands.get_search_commands()
            return await message.channel.send(commands)

def get_filters(directory_command, commands):
    return DICT.remove_key_value(directory_command, commands)

def base_search(query):
    return arts_db.Find.base_query(kwargs=query)

async def search(message, search_term):
    if search_term.startswith("?") or search_term.startswith("--help"):
        commands = Commands.get_search_commands()
        await send(message, commands)
    await run_search(message, search_term, arts_db)

async def send(mess, sendMess):
    await mess.channel.send(sendMess)

async def run_search(message, search_term, db):
    await message.channel.send_article(f"Searching for: {search_term}")
    results = db.Find.search_all(search_term, limit=500)
    await return_results(message, results)

async def return_results(message, results):
    if not results:
        await message.channel.send_article("No Results Found!")
    else:
        formatted_message = Commands.package_results(results)
        await message.channel.send(formatted_message)
        await message.channel.send(f"Done! Thanks for searching with Tiffany!")

@client.event
async def send_message(message):
    await message.channel.send(message)


client.run("OTMyNTI5MDEzMjgzNTIwNTQz.G6pT7x.6PGmCOCNXMT9bc38HUmz8vlNCzXNFIyF5xMd2A")
