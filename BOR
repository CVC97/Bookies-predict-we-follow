import numpy as np
import pandas as pd
import random as rd
import holoviews as hv
from bokeh.io import curdoc
hv.extension('bokeh')
from bokeh.layouts import layout
from bokeh.plotting import show, figure, ColumnDataSource, output_file
from bokeh.models import Slider, Button, Toggle


list_of_players = [
    'Alex_Zverev_2021.csv',
    'Dominic_Thiem_2021.csv',
    'Novak_Djokovic_2021.csv',
    
]

#betting odds to win percentage
def odds_to_p(odd_player, odd_opp):
    return 1 / (odd_player / odd_opp + 1)


#rating formula, always put 1 unit on player, always 1 unit on opponent (negative score, positive performance)
def rat_score(score, odd_player, odd_opp, result):
    if result == 'w':
        return score - (1 - odds_to_p(odd_player, odd_opp))
    elif result == 'l':
        return score + odds_to_p(odd_player, odd_opp)


#filename to playername
def csv_to_string(stringcsv):
    firstname = stringcsv[0:stringcsv.find('_')]
    secondname = stringcsv[stringcsv.find('_')+1:stringcsv.find('_2021')]
    return f'{firstname} {secondname}'


#filename to final rating
def player_to_frating(filename):
    player_data = pd.read_csv(f'csv_players/{filename}', sep = ',', header=0, skipinitialspace=True)
    name = csv_to_string(filename)
    players_rating = 0
    for i in range(player_data.shape[0]):
        players_rating = rat_score(players_rating, player_data['o_own'].loc[i], player_data['o_opp'].loc[i], player_data['result'].loc[i])
    return players_rating


#all players dick with rating as key
def all_players_dick(list_of_players):
    dick_all_players = {}
    for item in list_of_players:
        dick_all_players[player_to_frating(item)] = item
    return dick_all_players


#all players list
def all_players_list(list_of_players):
    list_all_players = []
    for item in list_of_players:
        list_all_players.append(player_to_frating(item))
    return list_all_players

rating_player_false = sorted(all_players_list(list_of_players))
print(rating_player_false)
rating_player = rating_player_false[::-1]
print(rating_player)
dick = all_players_dick(list_of_players)
name_player = [csv_to_string(dick[x]) for x in rating_player]
print(f'Name: {name_player}')

data = ColumnDataSource(data=dict(
            right = name_player,
            y = rating_player,
        )) 

TOOLTIPS = [
    ("Player", "$name_player"),
    ("Rating", "@rating_player"),
]

p = figure(
    title = 'Bookies predict - we follow: Bookies Odds Rated', 
    y_range = name_player,
    plot_width = 800, 
    plot_height = 600,
    x_axis_label = 'rating',  
    tooltips = TOOLTIPS,
    )

p.hbar(
    y = name_player,
    right = rating_player,
    height = 0.4,
    #left = rating_player,
    #fill_color = factor_cmap(name_player, palette = Blues8, factors = name_player),
    fill_alpha = 0.5,
    #source = data,
)

def print_list():
    place = 1
    for x in rating_player_false:
        print(f'{place}. {csv_to_string(dick[x]) }: {round(x, 2)}')
        place += 1


print_list()
#show(p)
