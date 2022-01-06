# EldenRingTimerBot.py
import datetime
import os
import random

import discord

from datetime import date

from discord import Client
from discord.ext import tasks
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
CHANNEL_ID = 617825580116606988

client: Client = discord.Client()


class CustomClient(discord.Client):
    async def on_ready(self):
        print(f'{self.user} has connected to {self.guilds[0]}')
        channel_to_send = self.get_channel(CHANNEL_ID)
        print(f'{channel_to_send} is current channel.')
        print(f'{self.elden_ring_message()}')
        self.send_repeat_message.start()

    async def on_error(self, event, *args, **kwargs):
        with open('err.log', 'a') as f:
            if event == 'on_message':
                f.write(f'Unhandled message: {args[0]}\n')
            else:
                raise

    def get_random_quip(self):
        responses = ['Let the sun shine upon this Lord of Cinder!\n',
                     'Hmmmmmmmmmmmmmmmmm\n',
                     'Zzzzzzzzzzzzzzzzzz\n',
                     'Hail Tarnished!\n',
                     "Damn that blasted Patches. I'd fancy kicking him into a well one of these days.\n",
                     ]
        return str(random.choice(responses))

    def get_current_date(self):
        return str(date.today())

    def get_appended_date(self):
        current_date = date.today()
        date_format = current_date.strftime("%B %d, %Y")
        appended_date = "\nToday's date is: " + date_format
        return appended_date

    def get_elden_ring_release_date(self):
        return '\nElden Ring releases on: February 25, 2022\n'

    def get_days_until_release(self):
        # elden_ring_release_date = datetime.datetime(2022, 0o2, 25)
        # days_until_elden_ring_releases = elden_ring_release_date - datetime.datetime.now()
        # return f'\nElden Ring drops in {days_until_elden_ring_releases.days} days'

        # Specified date
        date1 = datetime.datetime.strptime('2022-02-25 00:00:00', '%Y-%m-%d %H:%M:%S')

        # Current date
        date2 = datetime.datetime.now()

        return f'\nElden Ring drops in ' \
               f'%d days, %d hours.\n' \
               % self.dhms_from_seconds(self.date_diff_in_seconds(date2, date1))

    def elden_ring_message(self):
        initial_quip = self.get_random_quip()
        appended_date = self.get_appended_date()
        release_date = self.get_elden_ring_release_date()
        days_until_release = self.get_days_until_release()
        final_message = f'{initial_quip}{appended_date}{release_date}{days_until_release}'
        return final_message

    def date_diff_in_seconds(self, dt2, dt1):
        timedelta = dt1 - dt2
        return timedelta.days * 24 * 3600 + timedelta.seconds

    def dhms_from_seconds(self, seconds):
        minutes, seconds = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)
        days, hours = divmod(hours, 24)
        return abs(days), hours + 6

    @tasks.loop(seconds=3600)
    async def send_repeat_message(self):
        channel_to_send = self.get_channel(CHANNEL_ID)
        await channel_to_send.send(self.elden_ring_message())


client = CustomClient()
client.run(TOKEN)
