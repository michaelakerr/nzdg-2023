import pandas as pd
import requests
from bs4 import BeautifulSoup

# Player contains these fields
# df = df[['PDGA#', 'Name', 'Div', 'Par', "Group", 'Rank', 'Points']]


def create_player(db, tournament, player):
    key = str(player["PDGA#"]) + "_" + \
        player['Name'].strip(" ") + "_"+str(player["Group"])
    doc_ref = db.collection('players').document(key)

    doc = doc_ref.get()
    if doc.exists:
        player_info = doc.to_dict()
        doc_ref.set({
            "total": float(player_info["total"]) + float(player["Points"]),
            str(tournament): player["Points"]
        }, merge=True)
        print(f'Player data: {doc.to_dict()}')
    else:
        print('No such Player!')
        doc_ref = db.collection("players").document(key)
        doc_ref.set({
            "name": player['Name'],
            "pdga_number": player['PDGA#'],
            "key": key,
            "scoring_group": player["Group"],
            "total": player["Points"],
            str(tournament): player["Points"]
        }, merge=True)


def create_players_and_points(tournament_name, url, tour_points):
    response = requests.get(url)

    group1 = ['MPO']
    group2 = ['MP40', 'MP50']
    group3 = ['FPO', 'MA1']
    group4 = ['MA40', 'MA50']
    group5 = ['MA2']
    group6 = ['MA3', 'MA60', 'FA1', 'FA40', 'FA50', 'FA60',
              'FA3', 'MA4', 'FA2', 'FA4', 'MJ18', 'MJ12', 'MA70']

    soup = BeautifulSoup(response.text, 'html.parser')

    # Get divs in tournament
    divisions = soup.find_all('h3', {'class': "division"})
    list_of_divs = []

    for row in divisions:
        list_of_divs.append(row.get_text().split(' · ')[0])

    # Get players
    page = soup.find_all('details')
    players = pd.read_html(str(page))

    for index, div in enumerate(players):
        div['Div'] = list_of_divs[index]
        if list_of_divs[index] in group1:
            div['Group'] = 1
        elif list_of_divs[index] in group2:
            div['Group'] = 2
        elif list_of_divs[index] in group3:
            div['Group'] = 3
        elif list_of_divs[index] in group4:
            div['Group'] = 4
        elif list_of_divs[index] in group5:
            div['Group'] = 5
        else:
            div['Group'] = 6

    # consolidate all the divs
    df = pd.concat(players)
    df = df[df.Total != "DNF"]
    df = df.drop(['Place', 'Points', 'Rating', 'Rd1', 'Rd2', 'Rd3',
                 'Rd4', 'Total', 'Prize (USD)'], axis=1, errors='ignore')
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    df['Par'] = pd.to_numeric(
        df['Par'], errors='coerce').fillna(0, downcast="infer")
    # Drop if DNF in par
    df = df.dropna(subset=['Par'])
    df['Rank'] = df.groupby(['Group'])['Par'].rank(
        method='first', ascending=True)

    # calculate points
    count_players_in_divs = df.groupby(['Group'])['Par'].count()

    df['Points'] = df.apply(lambda x: 1+(tour_points-1)*(count_players_in_divs[x['Group']
                                                                               ]-x['Rank'])/(count_players_in_divs[x['Group']]-1), axis=1)
    print(df)

    # rearrange columns
    df = df[['PDGA#', 'Name', 'Div', 'Par', 'Group', 'Rank', 'Points']]

    df.to_csv(tournament_name + '.csv', index=False)
    return df
