import os
from typing import List
from discord import Intents, Client, Message, Role
from dotenv import load_dotenv
from Racquetball import Meet

# GET BOT TOKEN (SAFELY)
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# SET UP BOT INTENTS
intents = Intents.default();
intents.message_content = True
intents.guilds = True
intents.members = True
client = Client(intents=intents)

#SET UP SERVER VARIABLES
current_meet:Meet = Meet(4)

# HANDLE MESSAGES SENT ON SERVER

@client.event
async def on_message(message: Message):
    # Base case for checking messages
    if message.author == client.user or message.channel.name != "game-assignment" or message.content[0] != '!':
        return
    
    command = message.content[1:len(message.content)]
    print(f'Command found from [{message.author.name}]: {command}')

    await parse_game_command(command.lower(), has_role("officers", message.author.roles), message)

def has_role(role:str, role_list:List[Role])->bool:
    for idx in range(0,len(role_list)):
        if role_list[idx].name == role:
            return True
    return False

async def parse_game_command(comm:str, is_officer:bool, mess:Message):
    if comm == "create" and not current_meet.meet_started and is_officer:
        current_meet.start_meet()
        await mess.channel.send("Meet Instance Created!")
        await mess.author.send(f'You cretaed a meet instance, the code to join is {current_meet.join_code}')
    elif "join" in comm and current_meet.meet_started:
        await handle_join(mess, comm)
    elif comm == "end" and current_meet.meet_started and is_officer:
        current_meet.end_meet()
    elif "assign" in comm and current_meet.meet_started and is_officer:
        current_meet.assign_players_singles()
        await mess.channel.send("Singles Matches assigned!")
    elif comm == "shuffle" and current_meet.meet_started and is_officer:
        pass
    elif "manual" in comm and current_meet.meet_started and is_officer:
        new_player_name = comm.split("-")[1]
        current_meet.add_player(new_player_name, new_player_name)
        await mess.channel.send(f"Player \"{new_player_name}\" added Manually!")
    elif comm == "show":        
        await mess.channel.send(current_meet)
    elif comm == "help":
        await show_commands(mess)
    else:
        print("Command not recognized")

async def handle_join(mess:Message, comm:str):
    join_code = comm.split('-')[1]

    if join_code == current_meet.join_code and not current_meet.in_meet(mess.author.name):
        current_meet.add_player(mess.author.name, mess.author.display_name)
        await mess.channel.send(f'{mess.author.mention} has successfully joined the meet!')
    elif join_code != current_meet.join_code:
        await mess.channel.send(f'{mess.author.mention} has entered the wrong join code...')
    else:
        await mess.channel.send(f'{mess.author.mention} is already in the meet...')

async def show_commands(mess:Message):
    commands_file = open("command_list.txt")

    file_lines = commands_file.readlines()

    info = "Here's a list of my commands!: \n"

    for st in file_lines:
        info += st

    await mess.channel.send(info)

    commands_file.close()

# CONNECT BOT TO DISCORD SERVER 
@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

def main():
    client.run(TOKEN)

if __name__ == '__main__':
    main()