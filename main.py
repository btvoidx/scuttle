#
#	Sorry for 0 comments on code.
#
import discord
from discord import utils
from random import choice
from config import config

class bot(discord.Client):
	async def on_ready(self):
		print(f'Started bot: {client.user}')

	async def on_voice_state_update(self, member, before, after):
		if (channel := after.channel) and channel.category_id in config.get('extendables') and channel.name.lower() == "+":
			extended = await channel.clone(name=f"{member.name}'s {choice(config.get('extended_names'))}")
			await member.move_to(extended)
			await extended.set_permissions(member, manage_channels = True)
			print(f"Created new temporary channel {extended}")

		if (channel := before.channel) and channel.category_id in config.get('extendables') and channel.name.lower() != "+":
			if channel.members == []:
				await channel.delete()
				print(f"Deleted temporary channel {channel} because there was no users")

	async def on_raw_reaction_add(self, payload):
		if payload.message_id in config.get('reaction_role_sync'):
			guild = self.get_guild(payload.guild_id)
			member = guild.get_member(payload.user_id)

			if (role_id := config.get('reaction_role_sync')[payload.message_id].get(str(payload.emoji))):
				role = utils.get(guild.roles, id = role_id)
				await member.add_roles(role)
				print(f"Gave {role} to {member}")

	async def on_raw_reaction_remove(self, payload):
		if payload.message_id in config.get('reaction_role_sync'):
			guild = self.get_guild(payload.guild_id)
			member = guild.get_member(payload.user_id)

			if (role_id := config.get('reaction_role_sync')[payload.message_id].get(str(payload.emoji))):
				role = utils.get(guild.roles, id = role_id)
				await member.remove_roles(role)
				print(f"Took {role} from {member}")

client = bot()
client.run(config.get('token'))