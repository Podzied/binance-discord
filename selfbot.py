import json, discord
from binance.client import Client
from discord.ext import commands

with open("config.json", "r") as config_file: # Read the json file
	config = json.load(config_file) # Load the contents of the json file


binance_api_key = config["api"] # Get binance api key
binance_security_key = config["security"] # Get binance security key
discord_token = config["token"] # Get discord token
discord_prefix = config["prefix"] # Get discord prefix


bot = commands.Bot(command_prefix=discord_prefix, self_bot=True) # Initialize discord bot
bot.remove_command("help") # Remove the default help command


client = Client(binance_api_key, binance_security_key) # Initialize Binance Client


@bot.event
async def on_ready():
	print("Bot is online!") # When the bot is online. Print that it is


@bot.command()
async def help(ctx):
	await ctx.send("```Commands:\naddress | Get crypto address thats linked to binance\nrecents | Get recent trades\naverage | Get average price of a crypto```") # Sends help command


@bot.command()
async def address(ctx, crypto=None):
	if not crypto == None: # If the crypto is not empty

		address = client.get_deposit_address(asset=crypto.upper()) # Get the address from the binance client

		if address["success"] == True: # Checks if binance returned a successful response

			await ctx.send(f"```Asset: {address['asset']}\nAddress: {address['address']}\nURL: {address['url']}```") # Send the message

		else:
			await ctx.send(f"There was an error in getting your {crypto} address") # Send message saying there was an error

	else:
		await ctx.send("Please enter a crypto!") # Sends error message


@bot.command()
async def recents(ctx, symbol=None):
	if not symbol == None: # Checks if there is no symbol

		try:
			trades = client.get_recent_trades(symbol=symbol.upper()) # Gets the recent trades
			counted_trades = [] # List for counted trades
			for i, trade in zip(range(7), trades): # for I in range and "i" in trades loop

				counted_trades.append(f"ID: {trade['id']} | Amount: {trade['qty']} | Price: {trade['price']}") # Adds trade to the list

			await ctx.send("\n".join(counted_trades)) # Send the list of trades
			counted_trades.clear() # Clear the list 

		except:
			await ctx.send("Invalid Symbol") # Invalid symbol message

	else:
		await ctx.send("Please provide a symbol") # No symbol message


@bot.command()
async def average(ctx, crypto=None):
	if not crypto == None: # Checks if crypto is None

		try:
			avg_price = client.get_avg_price(symbol=crypto.upper()) # Get average price from binance client
			await ctx.send(f"Current Average Price for {crypto} is: {avg_price['price']}") # Send average price

		except:
			await ctx.send("Invalid Symbol!") # Invalid Symbol message

	else:
		await ctx.send("Please Enter in a symbol!") # No symbol message


if __name__ == "__main__":
	bot.run(discord_token, bot=False) # Run bot
