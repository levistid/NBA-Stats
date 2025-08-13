import tkinter as tk
from tkinter import messagebox
from nba_api.stats.static import players
from nba_api.stats.endpoints import playercareerstats
from nba_logic import player_stats
from NBA_plots import plot_stat_single

# Function to get stat categories from NBA API
def get_stat_categories():
    sample_player = players.find_players_by_full_name("Rik Smits")[0]
    player_id = sample_player['id']
    career = playercareerstats.PlayerCareerStats(player_id=player_id)
    df = career.get_data_frames()[0]
    excluded = {"TEAM_ID", "LEAGUE_ID", "PLAYER_ID", "SEASON_ID", "TEAM_ABBREVIATION", "PLAYER_AGE"}
    return [col for col in df.columns if col not in excluded]

def show_stats_in_window(df, season_filter=None, team_filter=None):
    if season_filter:
        df = df[df['SEASON_ID'] == season_filter]
    if team_filter:
        df = df[df['TEAM_ABBREVIATION'] == team_filter]

    stats_window = tk.Toplevel()
    stats_window.title("Player Stats")
    stats_window.geometry("1200x600")

    text_widget = tk.Text(stats_window, wrap="none", width=190, height=30)
    text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    scroll_y = tk.Scrollbar(stats_window, orient="vertical", command=text_widget.yview)
    scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
    text_widget.configure(yscrollcommand=scroll_y.set)

    scroll_x = tk.Scrollbar(stats_window, orient="horizontal", command=text_widget.xview)
    scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
    text_widget.configure(xscrollcommand=scroll_x.set)

    df_display = df.copy().round(2)
    text_widget.insert(tk.END, df_display.to_string(index=False))

def setup_individual_player_ui(root):
    from nba_logic import player_stats
    from NBA_plots import plot_stat_single

    # Clear the window
    for widget in root.winfo_children():
        widget.destroy()

    selected_stat = tk.StringVar(root)
    selected_stat.set("Select a stat")

    # Get initial stat categories
    initial_stats = get_stat_categories()

    tk.Label(root, text="Enter NBA Player Name:").pack(pady=5)
    entry = tk.Entry(root, width=40)
    entry.pack(pady=5)

    stat_frame = tk.Frame(root)
    stat_frame.pack(pady=5)
    tk.Label(stat_frame, text="Stat to Plot:").pack(side=tk.LEFT, padx=5)
    stat_menu = tk.OptionMenu(stat_frame, selected_stat, *initial_stats)
    stat_menu.pack(side=tk.LEFT)

    tk.Label(root, text="Filter by Season (e.g., 2003-04):").pack(pady=5)
    season_entry = tk.Entry(root, width=40)
    season_entry.pack(pady=5)

    tk.Label(root, text="Filter by Team Abbreviation (e.g., CLE):").pack(pady=5)
    team_entry = tk.Entry(root, width=40)
    team_entry.pack(pady=5)

    def on_search():
        name = entry.get().strip()
        season = season_entry.get().strip()
        team = team_entry.get().strip().upper()

        if not name:
            messagebox.showerror("Input Error", "Please enter a player name.")
            return

        df, full_name = player_stats(name)
        if df is not None:
            stat_menu['menu'].delete(0, 'end')
            for col in df.columns:
                if col not in {"TEAM_ID", "LEAGUE_ID", "PLAYER_ID", "SEASON_ID", "TEAM_ABBREVIATION", "PLAYER_AGE"}:
                    stat_menu['menu'].add_command(label=col, command=tk._setit(selected_stat, col))
            selected_stat.set("Select a stat")

            show_stats_in_window(df, season_filter=season if season else None,
                                      team_filter=team if team else None)

            stat = selected_stat.get().strip()
            if stat and stat != "Select a stat":
                filtered_df = df.copy()
                if season:
                    filtered_df = filtered_df[filtered_df['SEASON_ID'] == season]
                if team:
                    filtered_df = filtered_df[filtered_df['TEAM_ABBREVIATION'] == team]
                if not filtered_df.empty and stat in filtered_df.columns:
                    plot_stat_single(filtered_df, stat, full_name)
                else:
                    messagebox.showinfo("No Data", "No data available for the selected filters.")
        else:
            messagebox.showerror("Not Found", "Player not found.")

    tk.Button(root, text="Search & Plot", command=on_search).pack(pady=10)

def setup_player_comparison_ui(root):
    from nba_logic import player_stats
    from NBA_plots import plot_stat_comp

    # Clear the window
    for widget in root.winfo_children():
        widget.destroy()

    selected_stat = tk.StringVar(root)
    selected_stat.set("Select a stat")

    initial_stats = get_stat_categories()

    tk.Label(root, text="Enter First NBA Player Name:").pack(pady=5)
    entry1 = tk.Entry(root, width=40)
    entry1.pack(pady=5)

    tk.Label(root, text="Enter Second NBA Player Name:").pack(pady=5)
    entry2 = tk.Entry(root, width=40)
    entry2.pack(pady=5)

    stat_frame = tk.Frame(root)
    stat_frame.pack(pady=5)
    tk.Label(stat_frame, text="Stat to Compare:").pack(side=tk.LEFT, padx=5)
    stat_menu = tk.OptionMenu(stat_frame, selected_stat, *initial_stats)
    stat_menu.pack(side=tk.LEFT)

    def on_compare():
        name1 = entry1.get().strip()
        name2 = entry2.get().strip()
        stat = selected_stat.get().strip()

        if not name1 or not name2:
            messagebox.showerror("Input Error", "Please enter both player names.")
            return

        df1, full_name1 = player_stats(name1)
        df2, full_name2 = player_stats(name2)

        if df1 is None or df2 is None:
            messagebox.showerror("Not Found", "One or both players not found.")
            return

        if stat not in df1.columns or stat not in df2.columns:
            messagebox.showerror("Stat Error", f"'{stat}' not found in one or both player data sets.")
            return

        plot_stat_comp(df1, df2, stat, full_name1, full_name2)

    tk.Button(root, text="Compare & Plot", command=on_compare).pack(pady=10)

"""
def launch_gui():
    root = tk.Tk()
    root.title("NBA Stats Explorer")
    root.geometry("600x500")

    selected_stat = tk.StringVar(root)
    selected_stat.set("Select a stat")

    # Get initial stat categories
    initial_stats = get_stat_categories()

    tk.Label(root, text="Enter NBA Player Name:").pack(pady=5)
    entry = tk.Entry(root, width=40)
    entry.pack(pady=5)

    # Stat to Plot dropdown (now placed below player name)
    stat_frame = tk.Frame(root)
    stat_frame.pack(pady=5)
    tk.Label(stat_frame, text="Stat to Plot:").pack(side=tk.LEFT, padx=5)
    stat_menu = tk.OptionMenu(stat_frame, selected_stat, *initial_stats)
    stat_menu.pack(side=tk.LEFT)

    tk.Label(root, text="Filter by Season (e.g., 2003-04):").pack(pady=5)
    season_entry = tk.Entry(root, width=40)
    season_entry.pack(pady=5)

    tk.Label(root, text="Filter by Team Abbreviation (e.g., CLE):").pack(pady=5)
    team_entry = tk.Entry(root, width=40)
    team_entry.pack(pady=5)

    def on_search():
        name = entry.get().strip()
        season = season_entry.get().strip()
        team = team_entry.get().strip().upper()

        if not name:
            messagebox.showerror("Input Error", "Please enter a player name.")
            return

        df, full_name = player_stats(name)
        if df is not None:
            # Update dropdown with stat columns from actual player data
            stat_menu['menu'].delete(0, 'end')
            for col in df.columns:
                if col not in {"TEAM_ID", "LEAGUE_ID", "PLAYER_ID"}:
                    stat_menu['menu'].add_command(label=col, command=tk._setit(selected_stat, col))
            selected_stat.set("Select a stat")

            show_stats_in_window(df, season_filter=season if season else None,
                                      team_filter=team if team else None)

            stat = selected_stat.get().strip().upper()
            if stat and stat != "Select a stat":
                plot_stat_single(df, stat, full_name)
        else:
            messagebox.showerror("Not Found", "Player not found.")

    tk.Button(root, text="Search & Plot", command=on_search).pack(pady=10)

    root.mainloop()
"""

def launch_gui():
    root = tk.Tk()
    root.title("NBA Stats Explorer")
    root.geometry("600x500")

    def show_player_options():
        # Clear the window
        for widget in root.winfo_children():
            widget.destroy()

        tk.Label(root, text="Choose Player Lookup Type:").pack(pady=10)

        
        tk.Button(root, text="Individual Player", command=lambda: setup_individual_player_ui(root)).pack(pady=5)
        tk.Button(root, text="Player Comparison", command=lambda: setup_player_comparison_ui(root)).pack(pady=5)


    def show_team_options():
        # Placeholder for team lookup UI
        messagebox.showinfo("Coming Soon", "Team lookup functionality is under development.")

    # Main menu
    tk.Label(root, text="Welcome to NBA Stats Explorer").pack(pady=20)
    tk.Button(root, text="Player Lookup", command=show_player_options).pack(pady=10)
    tk.Button(root, text="Team Lookup", command=show_team_options).pack(pady=10)