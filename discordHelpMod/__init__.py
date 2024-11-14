from datetime import datetime

import discord
from discord.ext import commands
from Database.event_insertion import query_event_data # Import the function
from Database.scraping_date_insertion import insert_last_scraping_date_event, insert_last_scraping_date_dinning, insert_last_scraping_date_parking, query_event_data_last_scrapped
from sys import argv  # So we can get the runtime params

# Event Pages
class PaginatedEventsView(discord.ui.View):
    def __init__(self, events, items_per_page=5):
        super().__init__()
        self.events = events
        self.items_per_page = items_per_page
        self.current_page = 0
        self.max_page = (len(events) - 1) // items_per_page
        self.update_buttons()

    def update_buttons(self):
        # Disable buttons if on the first or last page
        self.children[0].disabled = self.current_page <= 0
        self.children[1].disabled = self.current_page >= self.max_page

    async def update_message(self, interaction):
        # Update the embed content based on the current page
        start = self.current_page * self.items_per_page
        end = start + self.items_per_page
        events_chunk = self.events[start:end]

        # Create a new embed with the current page of events
        embed = discord.Embed(title="Upcoming Events", description=f"Page {self.current_page + 1} of {self.max_page + 1}", color=0x00ff00)
        for event in events_chunk:
            event_title = f"[{event['title']}]\n({event['link']})"
            event_description = f"{event['date']} at {event['meeting']}"
            embed.add_field(name=event_title, value=event_description, inline=False)

        await interaction.response.edit_message(embed=embed, view=self)

    @discord.ui.button(label="Previous", style=discord.ButtonStyle.primary)
    async def previous_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.current_page -= 1
        self.update_buttons()
        await self.update_message(interaction)

    @discord.ui.button(label="Next", style=discord.ButtonStyle.primary)
    async def next_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.current_page += 1
        self.update_buttons()
        await self.update_message(interaction)

# Dining Dropdown
class DiningDropdown(discord.ui.Select):
    def __init__(self, dining_status, capacity_indicator_func):
        options = [
            discord.SelectOption(
                label=f"{name}",
                description=f"{capacity_indicator_func(info['capacity'])} {info['capacity']} capacity"
            ) for name, info in dining_status.items()
        ]
        super().__init__(placeholder="Choose a dining hall...", options=options)
        self.dining_status = dining_status
        self.capacity_indicator_func = capacity_indicator_func

    async def callback(self, interaction: discord.Interaction):
        # Directly get the selected dining hall info using the exact label
        hall = self.values[0]
        info = self.dining_status[hall]

        # Create the response message with capacity indicator emoji
        capacity_emoji = self.capacity_indicator_func(info['capacity'])
        response = (
            f"{capacity_emoji} **{hall}**\n"
            f"Status: {info['status']}\n"
            f"Capacity: {info['capacity']}\n"
            f"Hours: {info['hours']}\n"
            f"Menu: {info['menu']}"
        )
        await interaction.response.edit_message(content=response, view=None)  # Update message with info

class DiningView(discord.ui.View):
    def __init__(self, dining_status, capacity_indicator_func):
        super().__init__()
        self.add_item(DiningDropdown(dining_status, capacity_indicator_func))

class MyClient(discord.Client):
    bot_key = argv[1]  # Zero is the name of the script

    # Mock Data
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
        "Crown Commons": {"status": "Open", "capacity": "80%", "menu": "Pizza, Salad, Burgers","hours": "7 AM - 10 PM"},
        "SoVi Dining": {"status": "Closed", "capacity": "N/A", "menu": "Sushi, Ramen, Stir Fry","hours": "11 AM - 9 PM"},
        "Prospector": {"status": "Open", "capacity": "70%", "menu": "Pasta, Sandwiches, Grill", "hours": "8 AM - 8 PM"},
        "Bistro 49": {"status": "Open", "capacity": "50%", "menu": "Steak, Seafood, Vegan", "hours": "5 PM - 11 PM"}
    }

    # Checks capacity to determine emoji
    def capacity_indicator(self, capacity):
        if capacity == "N/A":
            return "❌"
        cap_int = int(capacity.strip('%'))
        if cap_int >= 90:
            return "🟥"
        elif 70 <= cap_int < 90:
            return "🟨"
        else:
            return "🟩"

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
            #await message.channel.send('Hello! I am your bot.')
            last_scrapped_data = query_event_data_last_scrapped()
            # for dc in data:
            #
            #     await message.channel.send(dc.values())
            for data in last_scrapped_data:
                last_scrapped_time = datetime.fromisoformat(data["event_last_scraping_date"])
                current_time = datetime.now()
                if (last_scrapped_time < current_time):
                    insert_last_scraping_date_event()
                    await message.channel.send("before")
                else:
                    await message.channel.send("after")


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
            view = DiningView(self.dining_status, self.capacity_indicator)
            await message.channel.send("Select a dining hall from the dropdown below:", view=view)
        # Event Command - COMPLETE
        elif message.content == '!events':
            events = query_event_data()  # Fetch event data from the database

            if not events:
                await message.channel.send("No upcoming events found.")
                return

            # Embed Events View
            view = PaginatedEventsView(events)
            embed = discord.Embed(title="Upcoming Events", description="Page 1", color=0x00ff00)
            for event in events[:view.items_per_page]:
                event_title = f"[{event['title']}]\n({event['link']})"
                event_description = f"{event['date']} at {event['meeting']}"
                embed.add_field(name=event_title, value=event_description, inline=False)

            await message.channel.send(embed=embed, view=view)
        # Help Command
        elif message.content == '!help':
            await message.channel.send(
                '***__Command Help__***\n'
                '***!gym*** - Check gym status\n'
                '***!parking*** - Check parking status\n'
                '***!dining*** - Check dining status\n'
                '***!events*** - List upcoming events')

# Enable message content intent to read message
intents = discord.Intents.default()
intents.message_content = True
client = MyClient(intents=intents)
client.run(MyClient.bot_key)
