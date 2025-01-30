#Imoprtant definitions for matches and functions for handling matchmaking
from typing import List
from random import randint

class Player:
    name = ""
    nickname = ""
    court = 0
    opponent = None

    def __init__(self, name:str, nickname:str):
        self.name = name
        self.nickname = nickname

    def assign_Match(self, court:int, opponent):
        self.court = court
        self.opponent = opponent

class MatchUp:
    player_one:Player = None
    player_two:Player = None
    court = 0

    def __init__(self, player_one:Player, player_two:Player, court:int):
        self.player_one = player_one
        self.player_two = player_two
        self.court = court

class DoublesMatchUp:
    match_one:MatchUp = None
    match_two:MatchUp = None

    def __init__(self, match_one:MatchUp, match_two:MatchUp):
        self.match_one = match_one
        self.match_two = match_two
        

class Meet:
    players:List[Player] = []
    courts = 0
    singles_matches:List[MatchUp] = []
    doubles_matches:List[DoublesMatchUp] = []
    join_code:str = ""
    meet_started:bool = False
    is_singles:bool = True
    matches_assigned = False

    
    def __init__(self, courts:int):
        self.courts = courts

    def add_player(self, name:str, nickname:str):
        n_player:Player = Player(name, nickname)
        self.players.append(n_player)

    def in_meet(self, name:str):
        for idx in range(len(self.players)):
            if self.players[idx].name == name:
                return True
        return False
    
    def assign_players_singles(self):
        self.is_singles = True
        self.matches_assigned = True
        assigned_players:List[List[Player]] = [[]*self.courts]

        # Assign a court to each player
        for idx in range(len(self.players)):
            try:
                assigned_players[(idx%4)].append(self.players[idx])
            except IndexError:
                print(f"Code exited with index of {idx%4} and court size {self.courts}")
                return
            self.players[idx].court = (idx % 4)

        # Go through each court and make matches (account for odd # of players)
        for idx in range(self.courts):
            for jdx in range(len(0,assigned_players[idx],2)):
                try:
                    self.singles_matches.append(MatchUp(assigned_players[idx][jdx], assigned_players[idx][jdx+1], idx))
                except IndexError:
                    print("Only one person assigned to court")

        
    def assign_players_doubles(self):
        self.is_singles = False

    def generate_code(self):
        self.join_code = ""
        for idx in range(1, 5):
            self.join_code += str(randint(0,9))

    def start_meet(self):
        self.generate_code()
        self.meet_started = True
    
    def end_meet(self):
        self.join_code = ""
        self.meet_started = False
        self.players = []
        self.singles_matches = []
        self.doubles_matches = []
        self.matches_assigned = False

    def __str__(self)->str:
        if self.meet_started:
            info:str = ""

            # Add each player name
            if len(self.players) > 0:
                info += "Player List:\n"
                for idx in range(len(self.players)):
                    info+=f'{idx+1}. {self.players[idx].nickname}\n'
            else:
                info += "No players to Display"
                return info
            
            # Add matchups
            if len(self.singles_matches) > 0:
                info += "Singles Matches:\n"

                for idx in range(len(self.singles_matches)):
                    info += f'\tCourt {self.singles_matches[idx].court+1} {self.singles_matches[idx].player_one.nickname} vs {self.singles_matches[idx].player_two.nickname}\n'
            elif len(self.doubles_matches) > 0:
                info += "Doubles Matches:\n"

                for idx in range(len(self.singles_matches)):
                    pass
            else:
                info += "No Matchups yet :)"
            
            return info
        else:
            return "No instance of a meet currently exists..."