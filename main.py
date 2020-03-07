import discord
from random import randint
from os import environ

TOKEN = environ["TOKEN"]
client = discord.Client()

extendable = 685923213162577920

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
	if after.channel != None and after.channel.category_id == extendable and after.channel.name.lower() == "+":
		extended = await after.channel.clone(name=f"{member.nick}'s lobby")
		print(f"Created new temporary channel {extended}")
		await member.move_to(extended)
		await extended.set_permissions(member, manage_channels=True, stream=True, deafen_members=True)

	if before.channel != None and before.channel.category_id == extendable and before.channel.name.lower() != "+":
		extended = before.channel
		if extended.members == []:
			await extended.delete()
			print(f"Deleted temporary channel {extended} because there was no users")



client.run(TOKEN)