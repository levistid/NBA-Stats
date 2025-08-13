import matplotlib.pyplot as plt
from nba_api.stats.static import players
from nba_api.stats.endpoints import playercareerstats
from nba_api.stats.static import teams
from nba_api.stats.endpoints import teamyearbyyearstats
from nba_api.stats.endpoints import teamgamelog
from nba_api.stats.endpoints import TeamYearByYearStats, leaguedashteamstats

def plot_stat_single(df, stat, player_name):
    seasons = df['SEASON_ID']
    values = df[stat]
    plt.figure(figsize =(10 , 5))
    plt.plot(seasons, values, marker='o')
    plt.title(f"{player_name} - {stat} over career:")
    plt.xlabel("Season")
    plt.ylabel(stat)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.grid(True)
    plt.show()

def plot_stat_comp(df1, df2, stat, player_name1, player_name2):
    p1_seasons = df1['SEASON_ID']
    p2_seasons = df2['SEASON_ID']
    p1_values = df1[stat]
    p2_values = df2[stat]
    plt.figure(figsize =(10 , 5))
    plt.plot(p1_seasons, p1_values, marker='o', label = player_name1)
    plt.plot(p2_seasons, p2_values, marker = 's', label = player_name2)
    plt.title(f"{player_name1} vs {player_name2} - {stat} career comparison:")
    plt.xlabel("Season")
    plt.ylabel(stat)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.grid(True)
    plt.legend()
    plt.show()

def plot_stat_team(df, stat, player_name):
    seasons_year = df['YEAR']
    values = df[stat]
    plt.figure(figsize =(10 , 5))
    plt.plot(seasons_year, values, marker='o')
    plt.title(f"{player_name} - {stat} over franchise history:")
    plt.xlabel("Season")
    plt.ylabel(stat)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.grid(True)
    plt.show()