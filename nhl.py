"""
File: nhl.py
------------------
NHL interface to interface with the program. 
"""


import re 
import pdb
import praw
import datetime
import sys 
from nhlpy import NHLClient
import pdb
import json
import pprint




class NHLInterface:
    """
    NHL interface. 
    """

    def __init__(self):

        player_dict_path = 'data/nhl_player_dict.json'
        all_path = 'data/nhl_all_players_list.json'

        with open(player_dict_path, 'r') as f:
            self.player_dict = json.load(f)

        with open(all_path, 'r') as f:
            self.all_players_list = json.load(f)


        self.client = NHLClient()



    def get_nhl_stats(self, player_name):
        assert player_name in self.all_players_list
        
        player_id = self.player_dict[player_name]
        player_stats = self.client.stats.player_career_stats(player_id=player_id)
        last_5_games = player_stats['last5Games']
        featured_stats = player_stats['featuredStats']
        career_totals = featured_stats['regularSeason']['career']
        season_totals = featured_stats['regularSeason']['subSeason']


        stats_string = '\n'
        stats_string += f'---------- Recent (last 5 games) Stats for {player_name} ----------\n'
        stats_string += pprint.pformat(last_5_games)
        stats_string += '\n'
        stats_string += f'---------- Season Stats for {player_name} ----------\n'
        stats_string += pprint.pformat(season_totals)
        stats_string += '\n'
        stats_string += f'---------- Career Stats for {player_name} ----------\n'
        stats_string += pprint.pformat(career_totals)
        stats_string += '\n'
        stats_string += '-----------------------------------------------\n'

        return stats_string
    

    def find_player_name(self, user_prompt_text):
        # TODO: handle complex scandanavian names with accents  
        pattern = r'\b(?:' + '|'.join(re.escape(name) for name in self.all_players_list) + r')\b'
        # Search for names in the prompt using the regex pattern, ignoring case
        matches = re.findall(pattern, user_prompt_text, flags=re.IGNORECASE)
        
        # Return names as they originally appear in the names list
        return [name for name in self.all_players_list if any(re.match(re.escape(name), match, re.IGNORECASE) for match in matches)]

        

    def build_prompt(self, user_input, verbose=False):   

        
        names_found = self.find_player_name(user_input)

        if len(names_found) > 1:
            raise Exception("Multiple player names found. Please be more specific")
        elif len(names_found) < 1:
            raise Exception("Invalid player name. Please try again.")
        
        player_name = names_found[0]
    

        build_prompt = ""

        build_prompt += f"User question: {user_input}\n"
        build_prompt += f"Player name: {player_name}\n"
        build_prompt += f"context given: \n \n"
        stats_res = self.get_nhl_stats(player_name=player_name)
        build_prompt += stats_res
        
        if verbose:
            print(build_prompt)

        return build_prompt
    

    def test_interface(self):
        example_prompt = "Will Sidney Crosby score more than 2 goals next game?"
        res = self.build_prompt(example_prompt, verbose=False)
        print(res) 
