import discord
from Database.event_insertion import query_event_data # Import the function
from sys import argv  # So we can get the runtime params

class MyClient(discord.Client):
    bot_key = argv[1]  # Zero is the name of the script

    gym_status = {
        "status": "open",
        "hours": "6 AM - 10 PM",
        "capacity": "65%"
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

    events_data = [
        {"name": "Tech Talk", "date": "2024-10-15", "time": "3 PM", "location": "Student Union"},
        {"name": "Career Fair", "date": "2024-10-18", "time": "10 AM", "location": "Halton Arena"},
        {"name": "Study Session", "date": "2024-10-20", "time": "5 PM", "location": "Atkins Library"}
    ]

    def capacity_indicator(self, capacity):
        if capacity == "N/A":
            return ":x:"
        cap_int = int(capacity.strip('%'))
        if cap_int >= 90:
            return ":red_square:"
        elif 70 <= cap_int < 90:
            return ":yellow_square:"
        else:
            return ":green_square:"

    # Function to format lines with emoji before text
    def format_status_with_emoji(self, status_dict, include_capacity=True):
        longest_capacity_length = max(
            len(status) for status in status_dict.values()
        ) if include_capacity else 0

        formatted_lines = []
        for key, status in status_dict.items():
            capacity_percentage = status.split()[0] if include_capacity else ""
            capacity_emoji = self.capacity_indicator(capacity_percentage)
            padded_status = status + " " * (longest_capacity_length - len(status))
            formatted_lines.append(f"{capacity_emoji} {key}: {padded_status}")

        return "\n".join(formatted_lines)

    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    async def on_message(self, message):
        if message.author == self.user:
            return

        print(f'Message from {message.author}: {message.content}')

        # Hello Command
        if message.content == '!hello':
            await message.channel.send('Hello! I am your bot.')

        # Gym Command
        elif message.content == '!gym':
            capacity_emoji = self.capacity_indicator(self.gym_status['capacity'])
            gym_status_message = (
                f"{capacity_emoji} The gym is currently {self.gym_status['status']}!\n"
                f"Hours: {self.gym_status['hours']}\n"
                f"Current Capacity: {self.gym_status['capacity']}"
            )
            await message.channel.send(gym_status_message)

        # Parking Command
        elif message.content == '!parking':
            parking_status_message = "***__Parking Status__***:\n" + self.format_status_with_emoji(self.parking_status)
            await message.channel.send(parking_status_message)

        # Dining Command
        elif message.content == '!dining':
            dining_status_message = "***__Dining Halls__***:\n"
            for hall, info in self.dining_status.items():
                capacity_emoji = self.capacity_indicator(info['capacity'])
                dining_status_message += f"{capacity_emoji} {hall}: {info['status']}, {info['capacity']} capacity\n"
            await message.channel.send(dining_status_message)

        # Event Command - COMPLETE
        elif message.content == '!events':
            events = query_event_data()  # Fetch event data from the database

            if not events:
                await message.channel.send("No upcoming events found.")
                return

            # Create the embed message
            embed = discord.Embed(title="Upcoming Events", description="Here are the latest events:", color=0x00ff00)

            for event in events:
                # Each event title becomes a clickable link
                event_title = f"[{event['title']}]\n({event['link']})"
                event_description = f"{event['date']} at {event['meeting']}"

                # Add the event as a field in the embed
                embed.add_field(name=event_title, value=event_description, inline=False)

            await message.channel.send(embed=embed)

        # Help Command
        elif message.content == '!help':
            await message.channel.send(
                '***__Command Help__***\n'
                '***!gym*** - Check gym status\n'
                '***!parking*** - Check parking status\n'
                '***!dining*** - Check dining status\n'
                '***!events*** - List upcoming events')

# Enable message content intent to read messages
intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
client.run(MyClient.bot_key)
