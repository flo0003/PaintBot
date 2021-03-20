import discord
import os
import logging
import json
from discord.ext import commands

logging.basicConfig(level=logging.INFO)
client = commands.Bot(command_prefix="p.",intents=discord.Intents.all())
client.remove_command("help")

@client.event
async def on_ready():
  print('Bot is online.')
  game = discord.Game("painting roles.")
  await client.change_presence(status=discord.Status.online, activity=game)

@client.event
async def on_raw_reaction_add(payload):

  if payload.member.bot:
    pass
  
  else:

    with open('reactrole.json') as react_file:

      data = json.load(react_file)
      for x in data:
        if x['emoji'] == payload.emoji.name and x['message_id'] == payload.message_id:
          role = discord.utils.get(client.get_guild(payload.guild_id).roles, id=x['role_id'])

          await payload.member.add_roles(role)

@client.event
async def on_raw_reaction_remove(payload):

  if payload.member.bot:
    pass
  
  else:

    with open('reactrole.json') as react_file:

      data = json.load(react_file)
      for x in data:
        if x['emoji'] == payload.emoji.name and x['message_id'] == payload.message_id:
          role = discord.utils.get(client.get_guild(payload.guild_id).roles, id=x['role_id'])

          await client.get_guild(payload.guild_id).get_member(payload.user_id).remove_roles(role)


@client.command()
async def ping(ctx):
  await ctx.channel.send(f"Pong! - {round(client.latency*1000)} ms")

@client.command(aliases=['rr', 'reactrole'])
async def reactionrole(ctx, emoji, role: discord.Role,*,message):

  emb = discord.Embed(description=message, color = 0x303434)
  msg = await ctx.channel.send(embed=emb)
  await msg.add_reaction(emoji)

  with open('reactrole.json') as json_file:
    data = json.load(json_file)

    new_react_role = {
      'role_name':role.name,
      'role_id':role.id,
      'emoji':emoji,
      'message_id':msg.id
    }

    data.append(new_react_role)


  with open('reactrole.json','w') as j:
    json.dump(data,j,indent=4)

client.run(os.getenv('TOKEN'))