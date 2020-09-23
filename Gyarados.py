import discord
import asyncio
import datetime
from discord.ext import commands, tasks # extensions

client = commands.Bot(command_prefix = '.') # . is a string that represents the command

# what is an event? code that runs when the bot detects that a specific activity has happened
# first event
@client.event
# when the bot is ready and has all the info from discord
async def on_ready():
    print('Bot is ready.')
    
scheduled_message_time = datetime.time(minute=30, hour = 3) # UTC time, 12:30 pm MST

def get_next_weekday(current,desired):
    days_ahead = desired - current.weekday()
    if days_ahead <= 0:
        days_ahead += 7
    return current + datetime.timedelta(days_ahead)

# testing dates
#print(datetime.date.today())
#today_weekday = datetime.date.today()
#next_weekday = get_next_weekday(today_weekday,2)
#print(get_next_weekday(today_weekday,1)) # 1 = Tuesday
#print(datetime.datetime.combine(next_weekday, scheduled_message_time))

@tasks.loop(hours=24*7)
async def send_weekly_reminder():
    await client.wait_until_ready()
    channel = client.get_channel(750941709013352538)
    await channel.send("@everyone 24 hours until the weekly meeting starts! See you there.")
    
@send_weekly_reminder.before_loop
async def weekly_reminder_calculate():
    today_weekday = datetime.datetime.utcnow().date()
    next_weekday = get_next_weekday(today_weekday,2) # 2 = Wednesday, 3:30am next day, Thursday is 9:30pm here Wednesday
    then = datetime.datetime.combine(next_weekday, scheduled_message_time)
    #print("current weekday is " + str(today_weekday))
    #print("next weekday is " + str(next_weekday))
    #print("then is " + str(then))
    print("The next announcement will be on " + str(next_weekday.weekday()) + " at " + str(then))
    await discord.utils.sleep_until(then)
    print("24 hours until the weekly meeting starts!")
    
send_weekly_reminder.start()
    

# this is bot being run, contains the token
# import config file with the token
if __name__ == '__main__':
    import config
    client.run(config.token)



#  looking at that code, what's done in the weekly_reminder would be done in your task.loop's before_loop (without the while loop)
# and inside the loop itself, you'd just send a message
# you need the @tasks.loop decorator, loop.start() somewhere (not in on_ready)
# if you want it at a specific time on a specific day, you'll need to use some datetime methods, a before_loop for the task, and utils.sleep_until