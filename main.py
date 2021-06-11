import discord
import json
import os
from discord.ext import commands

bot = commands.Bot(command_prefix = "!", case_insensitive = True, description = "BobbyBot", strip_after_prefix = True)
os.chdir(r"D:\Cours\Hitema\Python\.vscode\BobbyBot") # Dossier contenant le fichier users.json

listTargetChannels = [851830119819771944, 811911038035034156]

def target_channels(ctx):
  return ctx.message.channel.id in listTargetChannels
  

@bot.event
async def on_ready():
  print(f"Bot {bot.user.name} (id {bot.user.id}) prêt ! :D")
  # await bot.change_presence(activity = discord.Game('))

@bot.event
async def on_command_error(ctx, error):
  if(ctx.channel.id in listTargetChannels):
    if isinstance(error, commands.CommandNotFound):
      await ctx.send(f"{ctx.author.name}, cette commande n'existe pas.")
    if isinstance(error, commands.MissingRequiredArgument):
      await ctx.send(f"Il manque un argument pour cette commande, {ctx.author.name}.")
    elif isinstance(error, commands.MissingPermissions):
      await ctx.send(f"Désolé, {ctx.author.name}, mais tu n'as pas les droits pour cela.")
    elif isinstance(error, commands.CheckFailure):
      print ("Pas le bon salon.")

    elif hasattr(error, "original"):
      if isinstance(error.original, discord.Forbidden):
        await ctx.send(f"{ctx.author.name}, je n'ai pas les droits pour faire ça.")
        
    else:
      print(error)


@bot.command()
@commands.check(target_channels)
async def serverInfo(ctx): # nom de la fonction == nom de la commande ; paramètre ctx : context
  server = ctx.guild
  numberOfTextChannels = len(server.text_channels)
  numberOfVoiceChannels = len(server.voice_channels)
  serverName = server.name
  numberOfPersons = server.member_count
  message = f"Ce serveur (**{serverName}**) contient **{numberOfPersons}** personnes.\nCe serveur possède {numberOfTextChannels} salons écrits et {numberOfVoiceChannels} salons vocaux."
  await ctx.send(message) # await car appel réseau


@bot.command()
@commands.check(target_channels)
async def sayTo(ctx, user, *texte): # argument avec * = nombre de paramètres infini (doit être le dernier paramètre)
  messages = await ctx.channel.history(limit = 1).flatten() # flatten change l'objet en liste
  await messages[0].delete() # Cache le dernier message
  await ctx.send(f"{user} {' '.join(texte)}") # join change le tableau en string

@bot.command()
@commands.check(target_channels)
@commands.has_permissions(manage_messages = True)
async def clear(ctx, nombre : int):
  messages = await ctx.channel.history(limit = nombre + 1).flatten()
  for message in messages:
    await message.delete()
  await ctx.send(f"{nombre} messages supprimés, {ctx.author.name}.")

@bot.command()
@commands.check(target_channels)
@commands.has_permissions(manage_messages = True)
async def clearAll(ctx):
  messages = await ctx.channel.history(limit = None).flatten()
  for message in messages:
    await message.delete()
  await ctx.send(f"Tous les messages ont été supprimés, {ctx.author.name}.")


# Système de leveling :

@bot.event
async def on_member_join(member):
  with open("users.json", "r") as file:
    users_json = json.load(file)

  await update_data(users_json, member)
    
  with open("users.json", "w") as file:
    json.dump(users_json, file)

@bot.event
async def on_message(message):
  with open("users.json", "r") as file:
    users_json = json.load(file)

  await update_data(users_json, message.author)
  await add_experience(users_json, message.author, 20, message.channel)
    
  with open("users.json", "w") as file:
    json.dump(users_json, file)

  await bot.process_commands(message) # N'éxécute pas les commandes sans ça


async def update_data(users_json, user):
  print(users_json)

  if not user.id in users_json:
    users_json[user.id] = {} # Création du user dans le fichier .json
    users_json[user.id]['xp'] = 0
    users_json[user.id]['level'] = 1

async def add_experience(users_json, user, xp_amount, channel):
  users_json[user.id]['xp'] = xp_amount

  lvl_start = users_json[user.id]['level']
  lvl_end = int( users_json[user.id]['xp'] ** (1/4) )
  if lvl_start > lvl_end:
    users_json[user.id]['level'] = lvl_end
    await channel.send(f"{user.mention} est monté au niveau {lvl_end} !")


bot.run("ODUxODIyODYzNjQ0MDk4NTgw.YL933A.KzP-M1aNQCmSdaEy7xxTapO-vF8") # Connexion avec le Token

# Afficher les informations dans des embed

# Demander à Fabien pour le rpg
# librairie pypokedex 1.6.0


# Gain d'xp en envoyant des messages et en réussissant des actions
# Montée de niveau une fois que l'xp est suffisante
# Stats d'atk / def / pv montant avec le niveau
# Pouvoir combattre des mobs et d'autres joueurs !