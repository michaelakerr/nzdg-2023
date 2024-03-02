#Read in Players into a dataframe from csv
import json
import pandas as pd
import streamlit

from pdga_scraper import create_player


# get players
# create players and points
def create_players_and_points_non_pdga_faultline():
    results = pd.read_csv('faultline_results.csv')
    # read csv
    tournament_name = "Faultline_Fury"
    tour_points = 40
    group1 = ['MPO']
    group2 = ['MP40', 'MP50']
    group3 = ['FPO', 'MA1']
    group4 = ['MA40', 'MA50']
    group5 = ['MA2']
    group6 = ['MA3', 'MA60', 'FA1', 'FA40', 'FA50', 'FA60',
              'FA3', 'MA4', 'FA2', 'FA4', 'MJ18', 'MJ12', 'MA70']
    
    # ADd a column to dataframe based on division called group
    results['Group'] = ''

    for index, row in results.iterrows():
        if row['Div'] in group1:
            results.loc[index, 'Group'] = 1
        elif row['Div'] in group2:
            results.loc[index, 'Group'] = 2
        elif row['Div'] in group3:
            results.loc[index, 'Group'] = 3
        elif row['Div'] in group4:
            results.loc[index, 'Group'] = 4
        elif row['Div'] in group5:
            results.loc[index, 'Group'] = 5
        else:
            results.loc[index, 'Group'] = 6

    print(results)


    results['Rank'] = results.groupby(['Group'])['Par'].rank(
        method='max', ascending=True)
    
    count_players_in_divs = results.groupby(['Group'])['Par'].count()

    # points
    #tour_points == 1+ (maxtourpoints-1) x (scoring group player count - ranking) / (scoring group player count-1)
    results['Points'] = results.apply(lambda x: 1+(tour_points-1)*(count_players_in_divs[x['Group']
                                                                               ]-x['Rank'])/(count_players_in_divs[x['Group']]-1), axis=1)

    # rearrange columns
    results = results[['PDGA#', 'Name', 'Div', 'Par', 'Group', 'Rank', 'Points']]

    results.to_csv(tournament_name + '.csv', index=False)
    return results


# calculate points
create_players_and_points_non_pdga_faultline()

#get players

# update database