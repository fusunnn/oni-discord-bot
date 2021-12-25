import os
import discord
from decouple import config


token = os.environ['TOKEN']
intents = discord.Intents.default()
intents.members = True
intents.presences = True
client = discord.Client(intents=intents)
server = None
member_count_channel = None
online_member_count_channel = None
welcome_channel = None


async def send_welcome_message(member, channel):
  return await channel.send(f"Welcome to the Gaki Oni Gang, {member.display_name}!") 

async def update_member_count(server, channel):
  new_name = f'{server.member_count} members'
  print(new_name)
  await channel.edit(name=new_name)


async def update_online_member_count(server, channel):
  member_list = server.members
  online_count = 0

  for member in member_list:
    if member.status == discord.Status.online:
      online_count += 1

  new_name = f'{online_count} online members'
  print(new_name)
  await channel.edit(name=new_name)


@client.event 
async def on_ready():
  global server, member_count_channel, online_member_count_channel, welcome_channel

  server = client.get_guild(923872841307406377)
  member_count_channel = client.get_channel(id=924090115763085324)
  online_member_count_channel = client.get_channel(id=924090115763085326)
  welcome_channel = client.get_channel(id=923884486658256906)  

  print(f'Ready, running as {client.user}')

  #update server member count every 5 minutes (to avoid exceeding discord.py requests rate limit)

  await update_member_count(server, member_count_channel)
  await update_online_member_count(server, online_member_count_channel)



@client.event
async def on_member_join(member):
  await send_welcome_message(member, welcome_channel)
  await update_member_count(server, member_count_channel)
  await update_online_member_count(server, online_member_count_channel)

@client.event
async def on_member_remove(member):
  await update_member_count(server, member_count_channel)
  await update_online_member_count(server, online_member_count_channel)

@client.event
async def on_member_update(before, after):
  await update_member_count(server, member_count_channel)
  await update_online_member_count(server, online_member_count_channel)

client.run(token)
