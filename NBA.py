import pandas as pd
import numpy as np

from nba_api.stats.static import players
from nba_api.stats.endpoints import playercareerstats
from NBA_plots import plot_stat_single
from NBA_plots import plot_stat_comp


#Search for player
search_funct = input("Press 1 for individual player, press 2 to compare two players, press 3 for team season results: ")

#results
#search_results1 = players.find_players_by_full_name(player1)
#search_results2 = players.find_players_by_full_name(player2)

#Single player search function with stat plot
if search_funct == "1":
    player1 = input("Enter name of NBA player: ")
    search_results1 = players.find_players_by_full_name(player1)
    
    if search_results1:
        player1 = search_results1[0]
        player_id = player1['id']
        career = playercareerstats.PlayerCareerStats(player_id=player_id)
        df = career.get_data_frames()[0]
        print(df.head(30))
        stat = input("Would you like to plot a stat? Y/N:")
        if stat.upper() == "Y":
            to_plot = input("What stat would you like to plot?: ").strip().upper()
            plot_stat_single(df, to_plot, player1['full_name'])
    else:
        print("Player not found")
 
 # 2 player comparison option with plot       
if search_funct == "2":
    player1 = input("Enter name of first NBA player: ")
    player2 = input("Enter name of second NBA player: ")
    
    search_results1 = players.find_players_by_full_name(player1)
    search_results2 = players.find_players_by_full_name(player2)
    
    if search_results1 and search_results2 :
        player1 = search_results1[0]
        player2 = search_results2[0]
        player_id1 = player1['id']
        player_id2 = player2['id']
        career1 = playercareerstats.PlayerCareerStats(player_id=player_id1)
        career2 = playercareerstats.PlayerCareerStats(player_id=player_id2)
        df1 = career1.get_data_frames()[0]
        df2 = career2.get_data_frames()[0]
        
        print(f"\n{player1['full_name']} Career Stats: ")
        print(df1.head(30))
        print(f"\n{player2['full_name']} Career Stats: ")
        print(df2.head(30))
        
        stat_comp = input ("Would you like to compare a statistic between these players (Y/N): ").strip().upper()
        if stat_comp.upper() == "Y":
            comp_plot = input("What stat would you like to compare: ").strip().upper()
            plot_stat_comp(df1, df2, comp_plot, player1['full_name'], player2['full_name'])
    else:
        print("Player(s) not found")
        
    