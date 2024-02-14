"""
File: nba.py
------------------
NBA interface to interface with the program. 
"""


import re 
import pdb
from nba_api.stats.endpoints import playergamelog, commonallplayers
import pandas as pd
import json
import praw
import datetime
import sys 



class NBAInterface:
    """
    NBA interface. 
    """

    def __init__(self):

        self.all_players = commonallplayers.CommonAllPlayers().get_data_frames()[0]
        self.all_players_list_nba = self.all_players['DISPLAY_FIRST_LAST'].tolist()

        self.reddit_client_id = 'Xj8_ZM8C5fS-P-rrqhQtvA'
        self.reddit_client_secret = '28lrVo4MkYysk8Z9EwlqDl2DL-SusA'

        assert self.all_players is not None
        assert self.all_players_list_nba is not None
    

    
    def get_nba_stats(self, player_name, n_rows=10):
        all_players = commonallplayers.CommonAllPlayers().get_data_frames()[0]
        all_players_list = all_players['DISPLAY_FIRST_LAST'].tolist()
        player_id = all_players.loc[all_players['DISPLAY_FIRST_LAST'] == player_name]['PERSON_ID'].tolist()[0]
        stats = playergamelog.PlayerGameLog(player_id=player_id)
        df = stats.get_data_frames()[0]
        first_n_rows = df.head(n_rows).to_dict(orient='records')
        keys_to_remove = ['SEASON_ID', 'Game_ID', 'Player_ID', 'VIDEO_AVAILABLE']
        stats_string = '\n'
        stats_string += f'---------- Recent Stats for {player_name} ----------\n'
        for elem in first_n_rows:
            for key in keys_to_remove:
                elem.pop(key, None)
            stats_string += json.dumps(elem)
            stats_string += '\n'
        
        stats_string += '-----------------------------------------------\n'
        
        return stats_string
    

    def find_player_name(self, user_prompt_text):
        pattern = r'\b(?:' + '|'.join(re.escape(name) for name in self.all_players_list_nba) + r')\b'
        # Search for names in the prompt using the regex pattern, ignoring case
        matches = re.findall(pattern, user_prompt_text, flags=re.IGNORECASE)
        
        # Return names as they originally appear in the names list
        return [name for name in self.all_players_list_nba if any(re.match(re.escape(name), match, re.IGNORECASE) for match in matches)]



    def scrape_reddit(self, player_name, n_rows=10):
        player_name = player_name.lower()
        
        user_agent = 'praw_scraper_1.0'

        reddit = praw.Reddit(client_id=self.reddit_client_id,
                            client_secret=self.reddit_client_secret,
                            user_agent=user_agent)

        subreddit_name = 'nba'

        res = ""
        res += f'---------- Recent news from reddit for {player_name} ----------\n'
        for submission in reddit.subreddit(subreddit_name).search(player_name, sort='top', time_filter='week', limit=n_rows):
            temp_res = " "
            temp_res += f"Title: {submission.title}\n"
            # TODO: get content 
            # temp_res += f"Content: {submission.selftext}\n"  # too unfiltered 
            temp_res += f"Comments: {submission.num_comments}\n"
            temp_res += f"Date: {datetime.datetime.fromtimestamp(submission.created)}\n"
            temp_res += "\n-----------------\n"

            if player_name in temp_res.lower():
                res += temp_res

        
        res += '-----------------------------------------------\n'
        
        return res


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
        stats_res = self.get_nba_stats(player_name=player_name, n_rows=10)
        build_prompt += stats_res
        reddit_res = self.scrape_reddit(player_name=player_name, n_rows=10)
        build_prompt += reddit_res
        
        if verbose:
            print(build_prompt)

        return build_prompt
    

    def test_interface(self):
        example_prompt = "Will Kevin Durant score more than 30 points next game?"
        res = self.build_prompt(example_prompt, verbose=False)
        print(res) 
    

