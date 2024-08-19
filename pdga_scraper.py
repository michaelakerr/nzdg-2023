import json
from io import StringIO
import pandas as pd
import requests
from bs4 import BeautifulSoup
from google.cloud.firestore_v1 import FieldFilter
from streamlit_sortables import sort_items
import streamlit as st
from google.cloud import firestore
from google.oauth2 import service_account

from CONSTANTS import PLAYER_TABLE_DB, TOURNAMENT_TABLE_DB

# key_dict = json.loads(st.secrets["textkey"])
# creds = service_account.Credentials.from_service_account_info(key_dict)
# db = firestore.Client(credentials=creds)

# Player contains these fields

map_tour_divisions = {
    "MPO": "Open - Mixed",
    "MP40": "Pro Masters - Mixed",
    "MP50": "Pro Masters - Mixed",
    "MA1": "Advanced - Mixed",
    "MA2": "Intermediate - Mixed",
    "MA3": "Intermediate - Mixed",
    "MA4": "Intermediate - Mixed",
    "MA40": "Amateur Masters - Mixed",
    "MA50": "Amateur Grand Masters - Mixed",
    "MA60": "Senior Grand Masters - Mixed",
    "MP60": "Senior Grand Masters - Mixed",
    "MP70": "Legends - Mixed",
    "MA70": "Legends - Mixed",
    "MJ18": "Juniors - Mixed",
    "MJ15": "Juniors - Mixed",
    "MJ12": "Juniors - Mixed",
    "MJ10": "Juniors - Mixed",
    "MJ08": "Juniors - Mixed",
    "MJ06": "Juniors - Mixed",
    "FPO": "Open - Women",
    "FP40": "Masters - Women",
    "FP50": "Grand Masters - Women",
    "FA1": "Advanced - Women",
    "FA2": "Advanced - Women",
    "FA3": "Advanced - Women",
    "FA4": "Advanced - Women",
    "FA40": "Masters - Women",
    "FA50": "Grand Masters - Women",
    "FA60": "Senior Grand Masters - Women",
    "FP60": "Senior Grand Masters - Women",
    "FP70": "Legends - Women",
    "FA70": "Legends - Women",
    "FJ18": "Juniors - Women",
    "FJ15": "Juniors - Women",
    "FJ12": "Juniors - Women",
    "FJ10": "Juniors - Women",
    "FJ08": "Juniors - Women",
    "FJ06": "Juniors - Women",
}


def get_all_tournaments(db):
    tournaments = db.collection(TOURNAMENT_TABLE_DB).order_by("order").stream()
    return tournaments

def get_total_points(db, player):
    majors = db.collection_group(TOURNAMENT_TABLE_DB).where(
    filter=FieldFilter("major", "==", True)
    ).stream()

    minors = db.collection_group(TOURNAMENT_TABLE_DB).where(
    filter=FieldFilter("major", "==", False)
    ).stream()
    total = 0
    major_points_list = []
    minor_points_list = []

    if majors.count() > 0:
        for m in majors:
            if str(m.id) in player:
                major_points_list.append(player[m.id])

        # sort and take top 2 of major scores
        major_points_list = sorted(major_points_list, key = lambda x:float(x), reverse=True)

        if len(major_points_list) >= 2:
            major_points_list = major_points_list[:2]
        elif len(major_points_list) >= 1:
            major_points_list = major_points_list[:1]

        # remove null and 0 values from majors
        major_points_list = [x for x in major_points_list if x != 0]
        major_points_list = [x for x in major_points_list if x != None]

    if minors.count() > 0:
        for m in minors:
            if str(m.id) in player:
                minor_points_list.append(player[m.id])

    # combine major and minor lists
    total_points = major_points_list + minor_points_list
    # get top 6 points
    total_points = sorted(total_points, key = lambda x:float(x), reverse = True)
    if (len(total_points) > 6):
        total_points = total_points[:6]

    # add total points together
    total = sum(total_points)

    return total


def create_player(db, tournament, player):
    key = str(player["PDGA#"]).strip(".0") + "_" + \
        player['Name'].replace(" ", "") + "_"+str(player['Player_Group'])
    doc_ref = db.collection(PLAYER_TABLE_DB).document(key)
    doc = doc_ref.get()
    if doc.exists:
        player_info = doc.to_dict()
        player_info[str(tournament)] = player["Points"]
        total_points = get_total_points(db, player_info)
        doc_ref.set({
            str(tournament): player["Points"],
            "total": total_points
        }, merge=True)
        print(f'Player data: {doc.to_dict()}')
    else:
        print('No such Player!')
        doc_ref = db.collection(PLAYER_TABLE_DB).document(key)
        doc_ref.set({
            "name": player['Name'],
            "pdga_number": player['PDGA#'],
            "key": key,
            'Player_Group': player['Player_Group'],
            "tour_division": map_tour_divisions[player['Div']],
            "scoring_group": player['Player_Group'],
            "total": player["Points"],
            str(tournament).replace(" ", "_"): player["Points"]
        }, merge=True)

# Define a custom ranking function
def custom_rank(group):
    # First rank by 'par', then by 'place'
    group = group.sort_values(by=['Par', 'Place']).reset_index(drop=True)

    # Add a 'rank' column
    group['Rank'] = group.index + 1

    return group

def create_players_and_points(tournament_name, url, tour_points):
    response = requests.get(url)

    group1 = ['MPO']
    group2 = ['MP40', 'MP50']
    group3 = ['MA1', 'FPO']
    group4 = ['MA2']
    group5 = ['MA40', 'MA50']
    group6 = ['MA3', 'MA60',  'MA4', 'MJ18', 'MJ12', 'MA70']
    group7 = ['FA1',  'FA40']
    group8 = ['FA50', 'FA60', 'FA2', 'FA3', 'FA4', 'FJ18' , 'FJ12']

    soup = BeautifulSoup(response.text, 'html.parser')

    # Get divs in tournament
    divisions = soup.find_all('h3', {'class': "division"})
    list_of_divs = []

    for row in divisions:
        list_of_divs.append(row.get_text().split(' · ')[0])

    # Get players
    page = soup.find_all('details')
    players = pd.read_html(StringIO(str(page)))

    for index, div in enumerate(players):
        div['Div'] = list_of_divs[index]
        if list_of_divs[index] in group1:
            div['Player_Group'] = 1
        elif list_of_divs[index] in group2:
            div['Player_Group'] = 2
        elif list_of_divs[index] in group3:
            div['Player_Group'] = 3
        elif list_of_divs[index] in group4:
            div['Player_Group'] = 4
        elif list_of_divs[index] in group5:
            div['Player_Group'] = 5
        elif list_of_divs[index] in group6:
            div['Player_Group'] = 6
        elif list_of_divs[index] in group7:
            div['Player_Group'] = 7
        elif list_of_divs[index] in group8:
            div['Player_Group'] = 8
        else:
            div['Player_Group'] = 0

    # consolidate all the divs
    df = pd.concat(players)
    df = df[df.Total != "DNF"]

    df = df.drop(['Points', 'Rating', 'Rd1', 'Rd2', 'Rd3',
                 'Rd4', 'Total', 'Prize (USD)'], axis=1, errors='ignore')
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

    df['Par'] = pd.to_numeric(
        df['Par'], errors='coerce', downcast='integer').fillna(0)
    # Drop if DNF in par
    df = df.dropna(subset=['Par'])
    df = df.groupby('Player_Group', group_keys=False).apply(custom_rank)

    # calculate points
    count_players_in_divs = df.groupby(['Player_Group'])['Par'].count()

    # points
    #tour_points == 1+ (maxtourpoints-1) x (scoring group player count - ranking) / (scoring group player count-1)
    df['Points'] = df.apply(lambda x: 1+(tour_points-1)*(count_players_in_divs[x['Player_Group']
                                                                               ]-x['Rank'])/(count_players_in_divs[x['Player_Group']]-1), axis=1)

    # rearrange columns
    df = df[['PDGA#', 'Name', 'Div', 'Par', 'Player_Group', 'Rank', 'Points']]

    df.to_csv(tournament_name + '.csv', index=False)
    return df
