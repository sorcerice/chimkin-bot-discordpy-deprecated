from datetime import datetime as d
from random import choice, randint
from typing import Optional
from itertools import cycle
from glob import glob

from aiohttp import request
from discord import Member, Embed
from discord import File
from discord.ext import commands, tasks
from discord.ext.commands import Cog, BucketType
from discord.ext.commands import BadArgument
from discord.ext.commands import command, cooldown


class Fun(Cog):
	def __init__(self, bot):
		self.bot = bot


	@command(name="henyo",
			 aliases=["hi", "hello"],
			 brief="Say henyo to Chimkin",
			 description="Say henyo to Chimkin")
	async def say_hello(self, ctx):
		await ctx.send(f"Henyo {ctx.author.mention}!")


	@command(name="ping",
			 aliases=["peng", "pingy"],
			 brief="Chimkin's ping",
			 description="Chimkin's ping")
	async def ping(self, ctx):
		start = d.timestamp(d.now()) #gets the timestamp of when the command was used

		msg = await ctx.send("Pinging")
		#grabs previous start and subtracts from current time to provide the ping
		await msg.edit(content=f"Pong! {round((d.timestamp(d.now()) - start)*1000)}ms")
		return


	@command(name="8ball",
			 aliases=["predict", "foresee", "noodleme"],
			 brief="Ask Chimkin yes or no questions",
			 description="Ask Chimkin yes or no questions")
	async def _8ball(self, ctx, *, question):
		responses = ['Awie council says yes.',
					 'Council of eggs says yes.',
					 'Yes, if you slap Lunch.',
					 'Yes, if you roast Lunch.',
					 'Yes, if you spank Lunch.',
					 'Donate 1000 MC to Amber and it will happen.',
					 'Spank, slap and roast Lunch 4x and it should pass.',
					 'If you wingman for Ry, it is certain.',
					 'Yes, and you will also get an MVP card today',
					 'Awies smile on you.',
					 "Foresight failed. Lunch's fat ass blocked the view.",
					 "An awie lost one of it's 9 lives, try again later.",
					 "Nick doesn't want you to ask that.",
					 'Ashe scummed your 8ball, try again later.',
					 'Failed. Liz wants it to be a secret.',
					 "The Awie Council has made a decision, it's no",
					 'Eggsassins will prevent it.',
					 'No, and you are never getting an MVP card.',
					 'It is highly unlikely because Lunch said so.',
					 'Nope, because Lunch is still a homophobe.']
		await ctx.send(f'{random.choice(responses)}')



	@command(name="dice",
			 aliases=["roll", "rngesus"],
			 brief="Rolls a dice and sums the output (useful if we ever want to play D&D)",
			 description=f'''Rolls a dice and sums the output
			 \nType the number of rolls followed by 'd' followed by the number of sides on the dice
			 \n<number of rolls>d<sides on dice>
			 \nExample: For rolling a 6 sided dice 4 times
			 \n.dice 4d6''')
	@cooldown(5, 30, BucketType.user)
	async def roll_dice(self, ctx, die_string: str):
		dice, value = (int(term) for term in die_string.split("d"))

		if dice <= 25:
			rolls = [randint(1, value) for i in range(dice)]

			await ctx.send(" + ".join([str(r) for r in rolls]) + f"= {sum(rolls)}")

		else:
			await ctx.send("You fucking nuts? Try a lower number, idiot!")


	@command(name="slap",
			 aliases=["hit"],
			 brief="Makes you slap someone",
			 description="Makes you slap someone")
	@cooldown(5, 10, BucketType.user)
	async def slap_member(self, ctx, member:Member, *, reason: Optional[str] = "for no reason"):
		await ctx.send(f"{ctx.author.display_name} slapped {member.mention} {reason}")

	@slap_member.error
	async def slap_member_error(self, ctx, exc):
		if isinstance(exc, BadArgument):
			await ctx.send("Umm, who are you even trying to slap, idiot?")



	@command(name="say",
			 aliases=["echo", "repeat"],
			 brief="Chimkin repeats anything you want to say",
			 description="Chimkin repeats anything you want to say")
	@cooldown(5, 60, BucketType.user)
	async def echo_message(self, ctx, *, message):
		await ctx.message.delete()
		await ctx.send(message)



	@command(name="fact",
			 aliases=["animal"],
			 brief='''Has random facts and images of cats, dogs, pandas, foxes, birds and koalas''',
			 description='''Has random facts and images of cats, dogs, pandas, foxes, birds and koalas''')
	@cooldown(5, 20, BucketType.user)
	async def animal_fact(self, ctx, animal: str):
		if (animal := animal.lower()) in ("dog", "cat", "panda", "fox", "bird", "koala"):
			fact_url = f"https://some-random-api.ml/facts/{animal}"
			image_url = f"https://some-random-api.ml/img/{'birb' if animal == 'bird' else animal}"

			async with request("GET", image_url, headers={}) as response:
				if response.status == 200:
					data = await response.json()
					image_link = data["link"]

				else:
					image_link = None

			async with request("GET", fact_url, headers={}) as response:
				if response.status == 200:
					data = await response.json()

					embed = Embed(title=f"{animal.title()} fact",
								  description=data["fact"],
								  colour=ctx.author.colour)
					if image_link is not None:
						embed.set_image(url=image_link)
					await ctx.send(embed=embed)

				else:
					await ctx.send(f"API returned a {response.status} status.")

		else:
			await ctx.send("No facts are available for that animal.")



	@command(name='meme',
			 brief='Shows a random meme Sora stole from somewhere',
			 description='Shows a random meme Sora stole from somewhere')
	@cooldown(2, 20, BucketType.user)
	async def pull_meme(self, ctx):
		img = choice(glob('./data/smemes/*.jpg'))
		await ctx.send(file=File(img))


	@Cog.listener()
	async def on_ready(self):
		if not self.bot.ready:
			self.bot.cogs_ready.ready_up("fun")


def setup(bot):
	bot.add_cog(Fun(bot))