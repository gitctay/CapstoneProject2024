import discord
from sys import argv  # So we can get the runtime params


class MyClient(discord.Client):
    bot_key = argv[1]  # Zero is the name of the script
    print(f'Bot token: {bot_key}')  # To confirm the token was passed correctly

    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    async def on_message(self, message):
        # Ignore messages from the bot itself to avoid an infinite loop
        if message.author == self.user:
            return

        # Print out the message for debugging purposes
        print(f'Message from {message.author}: {message.content}')

        # Check if the message content is the command "!hello"
        if message.content == '!hello':
            # Send a message back to the same channel
            await message.channel.send('Hello! I am your bot.')

# Enable message content intent to read messages (required by Discord's API)
intents = discord.Intents.default()
intents.message_content = True  # This must be enabled to process message content

# Create the bot client with the intents
client = MyClient(intents=intents)

# Run the bot using the bot token from the command-line arguments
client.run(MyClient.bot_key)
