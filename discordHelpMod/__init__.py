import discord
import subprocess
import sys
import asyncio
from pathlib import Path
import pathlib
from datetime import datetime, timedelta
from discord.ext import commands
from database.event_insertion import query_event_data
from database.parking_insertion import query_parking_data
from database.scraping_date_insertion import insert_last_scraping_date_event, insert_last_scraping_date_dinning, \
    insert_last_scraping_date_parking, query_event_data_last_scrapped, query_parking_data_last_scraped, \
    query_dining_data_last_scrapped
from sys import argv

# Define bot with command prefix and intents
bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())
bot_key = argv[1]


async def event_last_scrapped_data(ctx):
    last_scrapped_data = query_event_data_last_scrapped()
    for data in last_scrapped_data:
        print("loop")
        last_scrapped_time = datetime.fromisoformat(data["event_last_scraping_date"])
        current_time_plus_delta = datetime.now() + timedelta(hours=7)

        if last_scrapped_time > current_time_plus_delta:
            # Data is outdated
            await ctx.send("Scraping new data...")
            print("scraping new data...")

            # Define the path to the scraping script
            scraping_file_path = pathlib.Path("generalScrapingMod") / "Scripts" / "uncc_event_collection.py"

            if not scraping_file_path.exists():
                await ctx.send(f"Scraping script not found: {scraping_file_path}")
                return False  # Signal failure to the caller

            try:
                # Resolve the absolute path and set the working directory
                script_abs_path = scraping_file_path.resolve()
                working_dir = script_abs_path.parent

                # Run the subprocess asynchronously
                process = await asyncio.create_subprocess_exec(
                    sys.executable,
                    str(script_abs_path),
                    cwd=str(working_dir),
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE,
                )

                # Monitor the process output for "Event collection completed."
                while True:
                    line = await process.stdout.readline()
                    if not line:  # End of output
                        break

                    decoded_line = line.decode().strip()
                    print(decoded_line)  # Print each line to the terminal
                    await ctx.send(f"Scraping Output: {decoded_line}")

                    # Check for the completion message
                    if "Event collection completed." in decoded_line:
                        insert_last_scraping_date_event()
                        print("Scraping script signaled completion.")
                        return True  # Signal success immediately after completion

                # If process completes without "Event collection completed."
                print("Scraping script exited without signaling completion.")
                stderr = await process.stderr.read()
                if stderr:
                    print(f"Scraping Errors:\n{stderr.decode()}")
                    await ctx.send(f"Scraping Errors:\n{stderr.decode()}")
                return False

            except Exception as e:
                await ctx.send(f"Error running the scraping script: {e}")
                print(f"Error running the scraping script: {e}")
                return False  # Signal failure to the caller

    # If scraping was not needed, return success
    return True


async def parking_last_scrapped_data(ctx):
    print("parking_last_scrapped_data called!")
    last_scrapped_data = query_parking_data_last_scraped()
    for data in last_scrapped_data:
        last_scrapped_time = datetime.fromisoformat(data["parking_last_scraping_date"])
        current_time = datetime.now() + timedelta(minutes=5)

        # Data is outdated
        if last_scrapped_time > current_time:
            await ctx.send("Scraping new parking data...")
            print("Scraping new parking data...")

            # Define the path to the scraping script
            scraping_file_path = pathlib.Path("generalScrapingMod") / "Scripts" / "parking_availability.py"

            if not scraping_file_path.exists():
                await ctx.send(f"Scraping script not found: {scraping_file_path}")
                return False  # Signal failure to the caller

            try:
                # Resolve the absolute path and set the working directory
                script_abs_path = scraping_file_path.resolve()
                working_dir = script_abs_path.parent

                # Run the subprocess asynchronously
                process = await asyncio.create_subprocess_exec(
                    sys.executable,
                    str(script_abs_path),
                    cwd=str(working_dir),
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE,
                )

                # Monitor the process output for a completion signal
                while True:
                    line = await process.stdout.readline()
                    if not line:  # End of output
                        break

                    decoded_line = line.decode().strip()
                    print(decoded_line)  # Print each line to the terminal
                    # await ctx.send(f"Scraping Output: {decoded_line}")

                    # Check for the completion message
                    if "Scraping completed." in decoded_line:
                        print("Scraping script signaled completion.")
                        insert_last_scraping_date_parking()  # Update the last scraping date
                        return True  # Signal success to the caller

                # If process completes without signaling completion
                print("Scraping script exited without signaling completion.")
                stderr = await process.stderr.read()
                if stderr:
                    print(f"Scraping Errors:\n{stderr.decode()}")
                    await ctx.send(f"Scraping Errors:\n{stderr.decode()}")
                return False

            except Exception as e:
                await ctx.send(f"Error running the scraping script: {e}")
                print(f"Error running the scraping script: {e}")
                return False  # Signal failure to the caller
        else:
            await ctx.send("Parking data is up-to-date.")
            return True

async def dining_last_scrapped_data(ctx):
    last_scrapped_data = query_dining_data_last_scrapped()
    for data in last_scrapped_data:
        last_scrapped_time = datetime.fromisoformat(data["dining_last_scraping_date"])
        current_time = datetime.now() + timedelta(minutes=30)
        if last_scrapped_time > current_time:
            insert_last_scraping_date_dinning()
            await ctx.send("Scraping new data...")
        else:
            await ctx.send("Data is up-to-date.")

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
        self.children[0].disabled = self.current_page <= 0
        self.children[1].disabled = self.current_page >= self.max_page

    async def update_message(self, interaction):
        start = self.current_page * self.items_per_page
        end = start + self.items_per_page
        events_chunk = self.events[start:end]

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
        hall = self.values[0]
        info = self.dining_status[hall]

        capacity_emoji = self.capacity_indicator_func(info['capacity'])
        response = (
            f"{capacity_emoji} **{hall}**\n"
            f"Status: {info['status']}\n"
            f"Capacity: {info['capacity']}\n"
            f"Hours: {info['hours']}\n"
            f"Menu: {info['menu']}"
        )
        await interaction.response.edit_message(content=response, view=None)

class DiningView(discord.ui.View):
    def __init__(self, dining_status, capacity_indicator_func):
        super().__init__()
        self.add_item(DiningDropdown(dining_status, capacity_indicator_func))

class MyBot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.gym_status = {
            "status": "open",
            "hours": "6 AM - 10 PM",
            "capacity": "65%"
        }
        self.parking_status = {
            "East Deck": "75% full",
            "Union Deck": "50% full",
            "West Deck": "90% full",
            "CRI Deck": "60% full"
        }
        self.dining_status = {
            "Crown Commons": {"status": "Open", "capacity": "80%", "menu": "Pizza, Salad, Burgers","hours": "7 AM - 10 PM"},
            "SoVi Dining": {"status": "Closed", "capacity": "N/A", "menu": "Sushi, Ramen, Stir Fry","hours": "11 AM - 9 PM"},
            "Prospector": {"status": "Open", "capacity": "70%", "menu": "Pasta, Sandwiches, Grill", "hours": "8 AM - 8 PM"},
            "Bistro 49": {"status": "Open", "capacity": "50%", "menu": "Steak, Seafood, Vegan", "hours": "5 PM - 11 PM"}
        }

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

    def parking_capacity_indicator(self, capacity):
        if capacity == "N/A":
            return "❌"
        cap_int = int(capacity.strip('%'))
        if cap_int <= 10:
            return "🟥"
        elif 11 <= cap_int <= 30:
            return "🟨"
        else:
            return "🟩"

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

    @commands.command()
    async def hello(self, ctx):
        await ctx.send('Hello! I am your bot.')

    @commands.command()
    async def parking(self, ctx):
        # Check last scrapped
        success = await parking_last_scrapped_data(ctx)
        if not success:
            await ctx.send("Could not complete parking data scraping. Please try again later.")
            return  # Exit the command if scraping fails

        # Main logic for parking
        parking_data = query_parking_data()
        if not parking_data:
            await ctx.send('There are no parking data available!')
            return

        # Prepare the parking status message
        parking_status_message = "***__Parking Status__***:\n"
        for parking in parking_data:
            parking_name = parking.get("parking_name", "Unknown")
            availability = parking.get("availability", "N/A")
            availability_emoji = self.parking_capacity_indicator(availability + "%")
            parking_status_message += f"{availability_emoji} {parking_name}: {availability}%\n"

        await ctx.send(parking_status_message)

    @commands.command()
    async def dining(self, ctx):
        # Check last scrapped
        # await dining_last_scrapped_data(ctx)

        #Main logic for dining
        view = DiningView(self.dining_status, self.capacity_indicator)
        await ctx.send("Select a dining hall from the dropdown below:", view=view)

    @commands.command()
    async def events(self, ctx):
        # Check last scrapped
        success = await event_last_scrapped_data(ctx)
        if not success:
            await ctx.send("Could not complete event scraping. Please try again later.")
            return  # Exit the command if scraping fails

        # Main logic for events
        events = query_event_data()
        if not events:
            await ctx.send("No upcoming events found.")
            return
        view = PaginatedEventsView(events)
        embed = discord.Embed(title="Upcoming Events", description="Page 1", color=0x00ff00)
        for event in events[:view.items_per_page]:
            event_title = f"[{event['title']}]\n({event['link']})"
            event_description = f"{event['date']} at {event['meeting']}"
            embed.add_field(name=event_title, value=event_description, inline=False)

        await ctx.send(embed=embed, view=view)

bot.add_cog(MyBot(bot))

@bot.event
async def on_ready():
    print(f'Logged on as {bot.user}!')
    await bot.add_cog(MyBot(bot))

bot.run(argv[1])
