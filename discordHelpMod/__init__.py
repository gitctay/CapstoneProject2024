import os
from dotenv import load_dotenv
import discord
from sys import argv  # So we can get the runtime params

# Load the environment variables from the .env file
load_dotenv()

class MyClient(discord.Client):
    bot_key = os.getenv("Discord_Bot_Token")  # Fetch the token from the environment

    gym_status = {
        "urec status": "open",
        "hours": "6 AM - 10 PM",
        "capacity": "65%",
        "belk status": "open",
        "hours": "7 AM - 8 PM",
        "capacity": "55%"
    }

    parking_status = {
        "East Deck": "75% full",
        "Union Deck": "50% full",
        "West Deck": "90% full",
        "CRI Deck": "60% full"
    }

    dining_status = {
        "Crown Commons": {"status": "Open", "capacity": "80%"},
        "SoVi Dining": {"status": "Closed", "capacity": "N/A"},
        "Prospector": {"status": "Open", "capacity": "70%"},
        "Bistro 49": {"status": "Open", "capacity": "50%"}
    }

    # Helper function to determine emoji based on capacity
    def capacity_indicator(self, capacity):
        if capacity == "N/A":
            return ""
        cap_int = int(capacity.strip('%'))  # Remove the '%' and convert to int
        if cap_int >= 90:
            return "🟥"  # Red square for 90% or more
        elif 70 <= cap_int < 90:
            return "🟨"  # Yellow square for 70-89%
        else:
            return "🟩"  # Green square for less than 70%

    # Helper function to format lines with proper emoji alignment
    def format_status_with_emoji(self, status_dict, include_capacity=True):
        # Extract and calculate the longest string for capacity
        longest_capacity_length = max(
            len(status) for status in status_dict.values()
        ) if include_capacity else 0

        formatted_lines = []
        for key, status in status_dict.items():
            capacity_percentage = status.split()[0] if include_capacity else ""
            capacity_emoji = self.capacity_indicator(capacity_percentage)
            padded_status = status + " " * (longest_capacity_length - len(status))
            formatted_lines.append(f"{key}: {padded_status} {capacity_emoji}")

        return "\n".join(formatted_lines)

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

        elif message.content == '!gym':
            capacity_emoji = self.capacity_indicator(self.gym_status['capacity'])
            gym_status_message = (
                f"The gym is currently {self.gym_status['status']}!\n"
                f"Hours: {self.gym_status['hours']}\n"
                f"Current Capacity: {self.gym_status['capacity']} {capacity_emoji}"
            )
            await message.channel.send(gym_status_message)


        elif message.content == '!parking':
            parking_status_message = "***__Parking Status__***:\n"
            parking_status_message += self.format_status_with_emoji(self.parking_status)
            await message.channel.send(parking_status_message)

        elif message.content == '!dining':
            dining_status_message = "***__Dining Halls__***:\n"
            for hall, info in self.dining_status.items():
                capacity_emoji = self.capacity_indicator(info['capacity'])
                dining_status_message += f"{hall}: {info['status']}, {info['capacity']} capacity {capacity_emoji}\n"
            await message.channel.send(dining_status_message)

        elif message.content == '!help':
            await message.channel.send('***__Command Help__***'
                                           '\n***!gym*** - Check gym status'
                                           '\n***!parking*** - Check parking status'
                                           '\n***!dining*** - Check dining status')

# Enable message content intent to read messages (required by Discord's API)
intents = discord.Intents.default()
intents.message_content = True  # This must be enabled to process message content

# Create the bot client with the intents
client = MyClient(intents=intents)

# Run the bot using the bot token from the command-line arguments
client.run(MyClient.bot_key)
