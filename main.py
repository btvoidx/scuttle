import discord
from random import randint
from os import environ

TOKEN = environ["TOKEN"]
client = discord.Client()

extend_alias = ["create channel", "create temp channel", "создать канал", "создать временный канал"]

@client.event
async def on_ready():
	print(f"We have logged in as {client.user}\n")



@client.event
async def on_message(message):
	if message.author == client.user:
		return

	if message.content.startswith('!hello'):
		await message.channel.send('Hello!')



@client.event
async def on_voice_state_update(member, before, after):
	if after.channel != None and after.channel.name.lower() in "create channel":
		extended = await after.channel.clone(name=f"t{randint(100000000000, 999999999999)}", reason="Extend")
		print(f"Created new temporary channel {extended}")
		await member.move_to(extended)
		print(f"Moved {member} to channel {extended}")

	if before.channel != None and before.channel.name[0] == "t":
		extended = before.channel
		if extended.members == []:
			await extended.delete(reason="Everyone left temporary channel")
			print(f"Deleted temporary channel {extended} because there was no users")



client.run(TOKEN)