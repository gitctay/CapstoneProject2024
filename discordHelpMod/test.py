import discord
import subprocess
import sys
import asyncio
from pathlib import Path
import pathlib
from datetime import datetime, timedelta, timezone
from discord.ext import commands
from database.event_insertion import query_event_data
from database.parking_insertion import query_parking_data
from database.dining_insertion import query_food_hall_data
from database.scraping_date_insertion import insert_last_scraping_date_event, insert_last_scraping_date_dinning, \
    insert_last_scraping_date_parking, query_event_data_last_scrapped, query_parking_data_last_scraped, \
    query_dining_data_last_scrapped
from sys import argv

# Define bot with command prefix and intents
bot = commands.Bot(command_prefix='!', intents=discord.Intents.all(), help_command=None)
bot_key = argv[1]

async def event_last_scrapped_data(ctx):
    last_scrapped_data = query_event_data_last_scrapped()
    for data in last_scrapped_data:
        last_scrapped_time = datetime.fromisoformat(data["event_last_scraping_date"])
        current_time_plus_delta = datetime.now(timezone.utc) - timedelta(hours=7)

        if last_scrapped_time < current_time_plus_delta:
            # Data is outdated
            await ctx.send("Scraping new event data...")
            print("scraping new event data...")

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
                    # await ctx.send(f"Scraping Output: {decoded_line}")

                    # Check for the completion message
                    if "Scraping completed." in decoded_line:
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
        else:
            # await ctx.send("Event data is up-to-date.")
            return True

async def parking_last_scrapped_data(ctx):
    last_scrapped_data = query_parking_data_last_scraped()

    # Check if the last_scrapped_data is empty
    if not last_scrapped_data:
        await ctx.send("No parking data has been scraped yet. Scraping new parking data...")
        print("No last scrapped data found. Scraping new parking data...")

        success = await parking_empty_scrapping(ctx)
        if success:
            await ctx.send("Scraping complete. Please send command again to check new parking data.")

        return True

    for data in last_scrapped_data:
        last_scrapped_time = datetime.fromisoformat(data["parking_last_scraping_date"])
        current_time_plus_delta = datetime.now(timezone.utc) - timedelta(minutes=5)

        # Data is outdated
        if last_scrapped_time < current_time_plus_delta:
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
            return True

async def dining_last_scrapped_data(ctx):
    last_scrapped_data = query_dining_data_last_scrapped()
    for data in last_scrapped_data:
        last_scrapped_time = datetime.fromisoformat(data["dinning_last_scraping_date"])
        current_time_plus_delta = datetime.now(timezone.utc) - timedelta(minutes=30)

        # Data is outdated
        if last_scrapped_time < current_time_plus_delta:
            await ctx.send("Scraping new dining data...")
            print("Scraping new dining data...")

            # Define the path to the scraping script
            scraping_file_path = pathlib.Path("generalScrapingMod") / "Scripts" / "dining_availability.py"

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
                        insert_last_scraping_date_dinning()  # Update the last scraping date
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
            return True

async def event_empty_scrapping(ctx):
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
            # await ctx.send(f"Scraping Output: {decoded_line}")

            # Check for the completion message
            if "Scraping completed." in decoded_line:
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

async def parking_empty_scrapping(ctx):
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

        # Monitor the process output for "Parking collection completed."
        while True:
            line = await process.stdout.readline()
            if not line:  # End of output
                break

            decoded_line = line.decode().strip()
            print(decoded_line)  # Print each line to the terminal
            # await ctx.send(f"Scraping Output: {decoded_line}")

            # Check for the completion message
            if "Scraping completed." in decoded_line:
                insert_last_scraping_date_parking()
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

async def dining_empty_scrapping(ctx):
    # Define the path to the scraping script
    scraping_file_path = pathlib.Path("generalScrapingMod") / "Scripts" / "dining_availability.py"

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

        # Monitor the process output for "Dining collection completed."
        while True:
            line = await process.stdout.readline()
            if not line:  # End of output
                break

            decoded_line = line.decode().strip()
            print(decoded_line)  # Print each line to the terminal
            # await ctx.send(f"Scraping Output: {decoded_line}")

            # Check for the completion message
            if "Scraping completed." in decoded_line:
                insert_last_scraping_date_dinning()
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

class PaginatedEventsView(discord.ui.View):
    def __init__(self, events, items_per_page=5):
        super().__init__()
        self.events = events
        self.items_per_page = items_per_page
        self.current_page = 0
        self.max_page = (len(events) - 1) // items_per_page

    def initialize_buttons(self):
        self.update_buttons()

    def update_buttons(self):
        if len(self.children) >= 2:  # Ensure buttons exist before accessing them
            self.children[0].disabled = self.current_page <= 0
            self.children[1].disabled = self.current_page >= self.max_page

    async def update_message(self, interaction):
        start = self.current_page * self.items_per_page
        end = start + self.items_per_page
        events_chunk = self.events[start:end]

        embed = discord.Embed(
            title="Upcoming Events",
            description=f"Page {self.current_page + 1} of {self.max_page + 1}",
            color=0x00ff00
        )
        for event in events_chunk:
            recurring_note = " (This event is recurring)" if event.get("is_recurring") else ""
            event_title = f"[{event['title']}]\n({event['link']})"
            event_description = f"{event['date']} at {event['meeting']}\n{recurring_note}"
            embed.add_field(name=event_title, value=event_description, inline=False)

        await interaction.response.edit_message(embed=embed, view=self)

    @discord.ui.button(label="Previous", style=discord.ButtonStyle.primary)
    async def previous_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.current_page > 0:
            self.current_page -= 1
            self.update_buttons()
            await self.update_message(interaction)

    @discord.ui.button(label="Next", style=discord.ButtonStyle.primary)
    async def next_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.current_page < self.max_page:
            self.current_page += 1
            self.update_buttons()
            await self.update_message(interaction)

class DiningDropdown(discord.ui.Select):
    def __init__(self, dining_status):
        # Options for the current page
        options = [
            discord.SelectOption(
                label=f"{name}",
                description=f"{'🟩 Open' if info['status'] == 'Open' else '❌ Closed'}"
            )
            for name, info in dining_status.items()
        ]
        super().__init__(placeholder="Choose a dining hall...", options=options)
        self.dining_status = dining_status

    async def callback(self, interaction: discord.Interaction):
        # Retrieve data for the selected dining hall
        hall = self.values[0]
        info = self.dining_status[hall]

        # DEBUG: Log selected dining area data
        print(f"Selected hall: {hall}")
        print(f"Dining info: {info}")

        # Use emoji based on the status
        status_emoji = "🟩" if info["status"] == "Open" else "❌"
        response = (
            f"{status_emoji} **{hall}**\n"
            f"Status: {info['status']}\n"
            f"Info: {info['capacity']}\n"
        )
        await interaction.response.edit_message(content=response, view=None)

class PaginatedDiningView(discord.ui.View):
    def __init__(self, dining_status, items_per_page=5):
        super().__init__()
        self.dining_status = dining_status
        self.items_per_page = items_per_page
        self.current_page = 0

        # Split dining status into chunks
        self.dining_chunks = [
            dict(list(dining_status.items())[i:i + items_per_page])
            for i in range(0, len(dining_status), items_per_page)
        ]
        self.max_page = len(self.dining_chunks) - 1

        # Add dropdown and buttons
        self.update_dropdown()
        self.update_buttons()

    def update_dropdown(self):
        # Clear and add the dropdown for the current page
        for child in self.children:
            if isinstance(child, DiningDropdown):
                self.remove_item(child)

        current_chunk = self.dining_chunks[self.current_page]
        self.add_item(DiningDropdown(current_chunk))

    def update_buttons(self):
        # Enable/disable buttons based on the current page
        for child in self.children:
            if isinstance(child, discord.ui.Button):
                if child.label == "Previous":
                    child.disabled = self.current_page == 0
                elif child.label == "Next":
                    child.disabled = self.current_page == self.max_page

    @discord.ui.button(label="Previous", style=discord.ButtonStyle.primary)
    async def previous_page(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.current_page -= 1
        self.update_dropdown()
        self.update_buttons()
        await interaction.response.edit_message(view=self)

    @discord.ui.button(label="Next", style=discord.ButtonStyle.primary)
    async def next_page(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.current_page += 1
        self.update_dropdown()
        self.update_buttons()
        await interaction.response.edit_message(view=self)

class DiningView(discord.ui.View):
    def __init__(self, dining_status):
        super().__init__()
        self.add_item(DiningDropdown(dining_status))

class MyBot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def capacity_indicator(self, capacity):
        if not capacity or capacity == "N/A":
            return "❌"  # Default emoji for unavailable data
        try:
            cap_int = int(capacity.strip('%'))
            if cap_int >= 90:
                return "🟥"
            elif 70 <= cap_int < 90:
                return "🟨"
            else:
                return "🟩"
        except ValueError:
            return "❌"  # Default for non-numeric or invalid data

    def parking_capacity_indicator(self, capacity):
        if capacity == "N/A":
            return "❌"
        cap_int = int(capacity.strip('%'))
        if cap_int <= 10:
            return "🟥"
        elif 11 <= cap_int <= 35:
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
        # # Check last scrapped
        # success = await parking_last_scrapped_data(ctx)
        # if not success:
        #     await ctx.send("Could not complete parking data scraping. Please try again later.")
        #     return  # Exit the command if scraping fails

        # Main logic for parking
        parking_data = query_parking_data()
        if not parking_data:
            await ctx.send("No parking data found. Rescraping...")
            success = await parking_empty_scrapping(ctx)
            if success:
                await ctx.send("Scraping complete. Please send command again to check new parking data.")
            return

        # Prepare the parking status message
        parking_status_message = "***__Parking Status__***:\n"
        for parking in parking_data:
            parking_name = parking.get("parking_name", "Unknown")
            availability = parking.get("availability", "N/A")
            availability_emoji = self.parking_capacity_indicator(availability + "%")
            parking_status_message += f"{availability_emoji} {parking_name}: {availability}\n"

        await ctx.send(parking_status_message)

    @commands.command()
    async def dining(self, ctx):
        # Check last scrapped
        # success = await dining_last_scrapped_data(ctx)
        # if not success:
        #     await ctx.send("Could not complete dining data scraping. Please try again later.")
        #     return  # Exit the command if scraping fails

        #Main logic for dining
        dining_data = query_food_hall_data()
        if not dining_data:
            await ctx.send("No dining data found. Rescraping...")
            success = await dining_empty_scrapping(ctx)
            if success:
                await ctx.send("Scraping complete. Please send command again to check new dining data.")
            return

        # Map dining data into a structured dictionary
        dining_status = {
            dining["food_hall_name"]: {
                "status": dining.get("status", "Unknown"),
                "capacity": dining.get("availability", "N/A"),
                "hours": dining.get("hours", "No hours available")
            }
            for dining in dining_data
        }

        # Create paginated view
        view = PaginatedDiningView(dining_status)
        await ctx.send("Select a dining hall from the dropdown below:", view=view)

    @commands.command()
    async def events(self, ctx):
        # Check last scrapped
        success = await event_last_scrapped_data(ctx)
        if not success:
            await ctx.send("Last scrape event time is empty, rescraping....")
            scrape = await event_empty_scrapping(ctx)
            if scrape:
                await ctx.send("Scraping complete. Please send command again to check new events.")
            return  # Exit the command if scraping fails

        # Main logic for events
        events = query_event_data()
        if not events:
            await ctx.send("No event data found. Rescraping...")
            success = await event_empty_scrapping(ctx)
            if success:
                await ctx.send("Scraping complete. Please send command again to check new events.")
            return

        view = PaginatedEventsView(events)
        view.initialize_buttons()  # Initialize buttons after View is set up

        embed = discord.Embed(title="Upcoming Events", description="Page 1", color=0x00ff00)
        for event in events[:view.items_per_page]:
            recurring_note = " (This event is recurring)" if event.get("is_recurring") else ""
            event_title = f"[{event['title']}]\n({event['link']})"
            event_description = f"{event['date']} at {event['meeting']}\n{recurring_note}"
            embed.add_field(name=event_title, value=event_description, inline=False)

        await ctx.send(embed=embed, view=view)

    @commands.command(name="help")
    async def custom_help(self, ctx):
        """Custom help command to override the default one."""
        embed = discord.Embed(title="Help", description="Available Commands:", color=0x00ff00)

        # Add command descriptions
        embed.add_field(
            name="!dining",
            value="Displays the dining hall status, including capacity, menu, and hours.",
            inline=False
        )
        embed.add_field(
            name="!parking",
            value="Shows the current parking deck capacities and availability.",
            inline=False
        )
        embed.add_field(
            name="!events",
            value="Lists upcoming events with pagination to navigate through them.",
            inline=False
        )

        # Send the embed
        await ctx.send(embed=embed)

bot.add_cog(MyBot(bot))

@bot.event
async def on_ready():
    print(f'Logged on as {bot.user}!')
    await bot.add_cog(MyBot(bot))

bot.run(argv[1])
