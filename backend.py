"""
File: backend.py
------------------
Backend program that orchestrates the entire pipeline. 
"""


import pdb
import sys 
import json
import nhl 
import nba
from openai import OpenAI
import streamlit as st






class BackendInterface:
    """
    Backend interface. 
    """

    def __init__(self):

        self.nba = nba.NBAInterface()
        self.nhl = nhl.NHLInterface()

        self.openai_api_key = st.secrets["openai_key"]


    def openai_response(self, prompt):
        
        client = OpenAI(api_key=self.openai_api_key)

        final_prompt = f"Given the user question and player below, answer the users question based on the context given: \n \n {prompt}"


        completion = client.chat.completions.create(
            model="gpt-4-0125-preview",
            messages=[
                {"role": "system", "content": "You are a bot that understands natural language and will be given queries regarding sports analytics and betting questions. Your job is to use the context given by the user and assist them in deciding if the bets proposed are good or not based on the context given. If they provide stats in the context, make sure to include the relevant portions of the stats, in a well formatted manner in your analysis. Additional context, such as news from reddit may also be given. Finally, your response should be concluded with a conclusion that gives the user a yes or no answer if they asked a yes or no type question."},
                {"role": "user", "content": final_prompt}
            ]
        )

        return completion.choices[0].message.content.strip()
    

    def get_result(self, user_input, verbose=False):
        # handles user input 

        sport_determined = None 

        nhl_res = self.nhl.find_player_name(user_input)
        nba_res = self.nba.find_player_name(user_input)

        if len(nhl_res) > 0:
            sport_determined = 'nhl'

        if len(nba_res) > 0:
            sport_determined = 'nba'

        if sport_determined is None:
            return "Invalid player name. Please try again. We support NHL and NBA players currently."
        
        if sport_determined == 'nba':
            prompt_constructed = self.nba.build_prompt(user_input, verbose=False)
        elif sport_determined == 'nhl':
            prompt_constructed = self.nhl.build_prompt(user_input, verbose=False)
        else:
            raise Exception("Invalid sport determined")
        
        if verbose:
            print(prompt_constructed)
    
        openai_res = self.openai_response(prompt_constructed)

        return openai_res
    

        


