#Read in Players into a dataframe from csv

import pandas as pd

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
    results['Player_Group'] = ''

    for index, row in results.iterrows():
        if row['Div'] in group1:
            results.loc[index, 'Player_Group'] = 1
        elif row['Div'] in group2:
            results.loc[index, 'Player_Group'] = 2
        elif row['Div'] in group3:
            results.loc[index, 'Player_Group'] = 3
        elif row['Div'] in group4:
            results.loc[index, 'Player_Group'] = 4
        elif row['Div'] in group5:
            results.loc[index, 'Player_Group'] = 5
        else:
            results.loc[index, 'Player_Group'] = 6



    results['Rank'] = results.groupby(['Player_Group'])['Par'].rank(
        method='max', ascending=True)
    
    count_players_in_divs = results.groupby(['Player_Group'])['Par'].count()

    # points
    #tour_points == 1+ (maxtourpoints-1) x (scoring group player count - ranking) / (scoring group player count-1)
    results['Points'] = results.apply(lambda x: 1+(tour_points-1)*(count_players_in_divs[x['Player_Group']
                                                                               ]-x['Rank'])/(count_players_in_divs[x['Player_Group']]-1), axis=1)

    # rearrange columns
    results = results[['PDGA#', 'Name', 'Div', 'Par', 'Player_Group', 'Rank', 'Points']]

    results.to_csv(tournament_name + '.csv', index=False)
    return results



#get players

# update database