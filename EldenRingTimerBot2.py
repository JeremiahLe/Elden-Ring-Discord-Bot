# EldenRingTimerBot.py
import datetime
import os
import random

import discord

from datetime import date
import pytz
import tzlocal

from discord import Client
from discord.ext import tasks
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
CHANNEL_ID = os.getenv('DISCORD_CHANNEL_ID')

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
        local_timezone = datetime.datetime.utcnow()
        tz = pytz.timezone('America/Chicago')
        new_timezone = local_timezone.replace(tzinfo=pytz.utc).astimezone(tz)
        return str(new_timezone)

    def get_appended_date(self):
        # current_date = pytz.utc.localize(datetime.datetime.utcnow())
        # new_date = current_date.astimezone(pytz.timezone("America/Chicago"))
        local_timezone = datetime.datetime.utcnow()
        tz = pytz.timezone('America/Chicago')
        new_timezone = local_timezone.replace(tzinfo=pytz.utc).astimezone(tz)

        date_format = new_timezone.strftime("%B %d, %Y")
        appended_date = "\nToday's date is: " + date_format + " (Timezone: " + str(tzlocal.get_localzone()) + ")"
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
               f'%d days, %d hours, %d minutes.\n' \
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
        return abs(days), hours, minutes
    
    def return_imgur_link(self, img):
        if img == 'Onward':
            return "https://imgur.com/BjYD2bA"
        elif img == 'Rest':
            return "https://imgur.com/ZnmePCA"
        elif img == 'Dead':
            return "https://imgur.com/a/f6KvDGk"

    @tasks.loop(seconds=3600)
    async def send_repeat_message(self):
        channel_to_send = self.get_channel(CHANNEL_ID)
        await channel_to_send.send(self.elden_ring_message())
     
    # Final Event - Manually triggered #
    
    # async def send_repeat_message(self):
    #    channel_to_send = self.get_channel(CHANNEL_ID)
    #    await channel_to_send.send(
    #        "Haven't you heard? Elden Ring has released. Onward to the lands between, Fair Tarnished! For Catarina!",
    #        delete_after=6)
    #    await channel_to_send.send(self.return_imgur_link('Onward'), delete_after=6)
    #    time.sleep(8)

    #   await channel_to_send.send(
    #        "Me, on the other hand, I need a rest. Oh, don't worry, it's a the best thing after showing one's heroic valour! Hahahahaha....",
    #        delete_after=8)
    #    await channel_to_send.send(self.return_imgur_link('Rest'), delete_after=8)
    #    time.sleep(10)

    #    await channel_to_send.send(self.return_imgur_link('Dead'))
        

client = CustomClient()
client.run(TOKEN)
