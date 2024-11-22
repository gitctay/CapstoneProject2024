import unittest
from unittest.mock import AsyncMock, patch
import discord
from discord.ext.commands import Context
from discordHelpMod import bot

class TestDiscordBot(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        # Mock a Discord context
        self.ctx = AsyncMock(spec=Context)
        self.ctx.guild = AsyncMock()
        self.ctx.author = AsyncMock()
        self.ctx.send = AsyncMock()

    async def test_hello_command(self):
        await bot.get_command('hello').callback(self.ctx)
        self.ctx.send.assert_called_once_with('Hello! I am your bot.')

    @patch("discordHelpMod.query_parking_data")
    async def test_parking_command(self, mock_query_parking_data):
        # Mock parking data response
        mock_query_parking_data.return_value = [
            {"parking_name": "Deck A", "availability": "80"},
            {"parking_name": "Deck B", "availability": "20"},
        ]

        await bot.get_command('parking').callback(self.ctx)
        self.ctx.send.assert_called()  # Ensure the bot sends a response
        self.assertIn("Deck A", self.ctx.send.call_args[0][0])  # Check if "Deck A" is in the response

    @patch("discordHelpMod.query_food_hall_data")
    async def test_dining_command(self, mock_query_food_hall_data):
        # Mock dining data response
        mock_query_food_hall_data.return_value = [
            {"food_hall_name": "Crown Commons", "status": "Open", "availability": "80%", "hours": "7 AM - 10 PM"},
            {"food_hall_name": "SoVi Dining", "status": "Closed", "availability": "N/A", "hours": "11 AM - 9 PM"},
        ]

        await bot.get_command('dining').callback(self.ctx)
        self.ctx.send.assert_called()  # Ensure the bot sends a response
        self.assertIn("Crown Commons", self.ctx.send.call_args[0][0])  # Check if "Crown Commons" is in the response

    @patch("discordHelpMod.query_event_data")
    async def test_events_command(self, mock_query_event_data):
        # Mock event data response
        mock_query_event_data.return_value = [
            {"title": "Event 1", "link": "http://example.com", "date": "Fri, Nov 22, 2024", "meeting": "Hall A"},
            {"title": "Event 2", "link": "http://example.com", "date": "Sat, Nov 23, 2024", "meeting": "Hall B"},
        ]

        await bot.get_command('events').callback(self.ctx)
        self.ctx.send.assert_called()  # Ensure the bot sends a response
        self.assertIn("Event 1", self.ctx.send.call_args[0][0])  # Check if "Event 1" is in the response

if __name__ == "__main__":
    unittest.main()
