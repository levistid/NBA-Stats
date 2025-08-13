import pandas as pd
import numpy as np
import tkinter as tk
import difflib
from nba_api.stats.static import players
from nba_api.stats.endpoints import playercareerstats
from nba_api.stats.static import teams
from nba_api.stats.endpoints import teamyearbyyearstats
from nba_api.stats.endpoints import teamgamelog
from nba_api.stats.endpoints import TeamYearByYearStats, leaguedashteamstats, leaguegamefinder


#Team names
all_team_names = [team['full_name'] for team in teams.get_teams()]
all_player_names = [player['full_name'] for player in players.get_players()]

#Fuzzy Match
def fuzzy_team_lookup(input_name):
    match = difflib.get_close_matches(input_name, all_team_names, n=1, cutoff=0.6)
    if match:
        return match[0]
    else:
        return None
    
def fuzzy_player_lookup(input):
    player_match = difflib.get_close_matches(input, all_player_names, n=1, cutoff=0.6)    
    if player_match:
        return player_match[0]
    else:
        return None
    

#Team head to head check
def matchup_history (team1, team2):
    #team 1
    team1_full = fuzzy_team_lookup(team1)
    if not team1_full:
        print(f"Unable to find team matching '{team1}. ")
        return
    team1 = teams.find_teams_by_full_name(team1_full)
    #team 2
    team2_full = fuzzy_team_lookup(team2)
    if not team2_full:
        print(f"Unable to find team matching '{team2}'. ")
        return
    
#########################################
#                                        #
#       GET STATS                        #
#                                        #
##########################################

#Single player stats    
def player_stats(name):
    name_match = fuzzy_player_lookup(name)
    if not name_match:
        return None, None
    search_results = players.find_players_by_full_name(name_match)
    if search_results:
        player = search_results[0]
        player_id = player['id']
        career = playercareerstats.PlayerCareerStats(player_id = player_id)
        df = career.get_data_frames()[0]
        return df, player['full_name']
    return None, None

# 2 player comparison
def player_comps(name1, name2):
    # 2 data frames and full names
    df1, name1 = player_stats(name1)
    df2, name2 = player_stats(name2)
    if df1 is not None and df2 is not None:
        return df1, df2, name1, name2
    return None, None, None, None