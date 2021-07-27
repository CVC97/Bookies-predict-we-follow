import numpy as np
import pandas as pd
import random as rd
import holoviews as hv
from bokeh.io import curdoc
hv.extension('bokeh')
from bokeh.layouts import layout
from bokeh.plotting import show, figure, ColumnDataSource, output_file
from bokeh.models import Slider, Button, Toggle

#curdoc().theme = 'dark_minimal'

#betting odds to win percentage
def odds_to_p(odd_player, odd_opp):
    return 1 / (odd_player / odd_opp + 1)


#rating formula, always put 1 unit on player, always 1 unit on opponent (negative score, positive performance)
def rat_score(score, odd_player, odd_opp, result):
    if result == 'w':
        return score - (1 - odds_to_p(odd_player, odd_opp))
    elif result == 'l':
        return score + odds_to_p(odd_player, odd_opp)

def pay_p(score, odd_player, odd_opp, result):
    if result == 'w':
        return score - (odd_player / odd_opp)
    elif result == 'l':
        return score + 1

def pay_opp(score, odd_player, odd_opp, result):
    if result == 'w':
        return score - 1
    elif result == 'l':
        return score + (odd_opp / odd_player)


#return dictionary of 3 ratings in tupel for each KW and given filename potentially for each KW
def filename_to_dictionary(filename):
    player_data = pd.read_csv(f'csv_players/{filename}', sep = ',', header=0, skipinitialspace=True)
    temp_rating = (0, 0, 0)
    dicktionary = {0: temp_rating}
    for i in range(player_data.shape[0]):
        temp_rat_score = rat_score(temp_rating[0], player_data['o_own'].loc[i], player_data['o_opp'].loc[i], player_data['result'].loc[i])
        temp_pay_p = pay_p(temp_rating[1], player_data['o_own'].loc[i], player_data['o_opp'].loc[i], player_data['result'].loc[i])
        temp_pay_opp = pay_opp(temp_rating[2], player_data['o_own'].loc[i], player_data['o_opp'].loc[i], player_data['result'].loc[i])
        temp_rating = (temp_rat_score, temp_pay_p, temp_pay_opp)
        dicktionary[player_data['KW'].loc[i]] =  temp_rating
#potentially extends dictionary to all KWs 
    for i in range(player_data['KW'].loc[player_data.shape[0] - 1]):
       if i not in dicktionary:
           dicktionary[i] = dicktionary[i - 1]
    return dicktionary


#filename to playername
def csv_to_string(stringcsv):
    firstname = stringcsv[0:stringcsv.find('_')]
    secondname = stringcsv[stringcsv.find('_')+1:stringcsv.find('_2021')]
    return f'{firstname} {secondname}'


#returns curves for all given players and 3 methods
def curve_rat(list_of_players):
    for item in list_of_players:
        player_dict = filename_to_dictionary(item)
        plot_count = np.arange(len(player_dict)) 
        data = ColumnDataSource(data=dict(
            x = plot_count,
            y = [player_dict[x][0] for x in plot_count],
        ))
        p.line(
            line_color = dick_with_colors[item], 
            legend_label = csv_to_string(item), 
            line_width = 2, 
            source = data, 
            name = csv_to_string(item)
            )

def curve_pay_p(list_of_players):
    for item in list_of_players:
        player_dict = filename_to_dictionary(item)
        plot_count = np.arange(len(player_dict))
        data = ColumnDataSource(data=dict(
            x = plot_count,
            y = [player_dict[x][1] for x in plot_count],
        )) 
        p.line(
            source = data, 
            line_dash = 'dashed',
            line_color = dick_with_colors[item], 
            legend_label = csv_to_string(item), 
            line_width = 1, 
            name = f'{csv_to_string(item)} (Bet-on-Player)'
            )

def curve_pay_opp(list_of_players):
    for item in list_of_players:
        player_dict = filename_to_dictionary(item)
        plot_count = np.arange(len(player_dict)) 
        data = ColumnDataSource(data=dict(
            x = plot_count,
            y = [player_dict[x][2] for x in plot_count],
        ))
        p.line(
            source = data, 
            line_dash = 'dashed',
            line_color = dick_with_colors[item], 
            legend_label = csv_to_string(item), 
            line_width = 1, 
            name = f'{csv_to_string(item)} (Bet-on-Opponent)'
            )


#make plot
def make_plot(list_of_players):
    curve_rat(list_of_players)
    curve_pay_p(list_of_players)
    curve_pay_opp(list_of_players)
    show(p)


#glyphs and stuff
TOOLTIPS = [
    ("Player", "$name"),
    ("Week", "$index"),
    ("Rating", "@y"),
]

p = figure(
    title = 'Bookies predict - we follow: Rating Over Time', 
    plot_width = 800, 
    plot_height = 600, 
    x_axis_label= 'calendar week', 
    y_axis_label = 'rating', 
    tooltips = TOOLTIPS,
    )


#players 
list_of_players = [
    'Alex_Zverev_2021.csv',
    'Dominic_Thiem_2021.csv',
    'Novak_Djokovic_2021.csv',
    
]


#creates random color for each player
dick_with_colors = {}
for item in list_of_players:
    dick_with_colors[item] = (rd.randint(0, 255), rd.randint(0, 255), rd.randint(0, 255))


make_plot(list_of_players)

