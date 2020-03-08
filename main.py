import discord
from random import randint
from os import environ

TOKEN = environ["TOKEN"]
client = discord.Client()

extendable = 685923213162577920
places = ["lounge", "lodge", "voice channel", "room"]

def randstr(list):
	return list[randint(0, len(list) - 1)]

@client.event
async def on_ready():
	print(f"We have logged in as {client.user}")



@client.event
async def on_message(message):
	if message.author == client.user:
		return

	if message.content.startswith(f'{client.user}'):
		await message.channel.send("*Runs away*")



@client.event
async def on_voice_state_update(member, before, after):
	if after.channel != None and after.channel.category_id == extendable and after.channel.name.lower() == "+":
		extended = await after.channel.clone(name=f"{member.name}'s {randstr(places)}")
		print(f"Created new temporary channel {extended}")
		await member.move_to(extended)
		await extended.set_permissions(member, manage_channels=True, stream=True, move_members=True)

	if before.channel != None and before.channel.category_id == extendable and before.channel.name.lower() != "+":
		extended = before.channel
		if extended.members == []:
			await extended.delete()
			print(f"Deleted temporary channel {extended} because there was no users")



client.run(TOKEN)