# Draw some charts and stats based on uniqueness of players

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

import plotly.graph_objects as go

import json
from google.cloud import firestore
from google.oauth2 import service_account

key_dict = json.loads(st.secrets["textkey"])
creds = service_account.Credentials.from_service_account_info(key_dict)
db = firestore.Client(credentials=creds)

@st.cache_data(persist="disk")
def get_all_players():
    players = db.collection(u'players').stream()
    unique_players = {}
    for player in players:
        unique_players[player.id] = player.to_dict()
    return unique_players

def get_all_tournaments():
    tournaments = db.collection(u'tournaments').stream()
    unique_tournaments = {}
    for tournament in tournaments:
        unique_tournaments[tournament.id] = tournament.to_dict()
    return unique_tournaments

def draw_unique_player_chart():
    #unique_players = {}
    unique_players = get_all_players()

    tourn = get_all_tournaments()

    tournaments_player = []
    tt = [0, 649, 206, 96, 84, 32, 27, 19, 15, 4, 6, 3, 0, 2]


    # for each player in unique players, count the number of tournaments
    for player in unique_players:
        player_tournaments = len(unique_players[player].keys()) - 6
        tournaments_player.append(player_tournaments)
    
    
    unique_tournaments = np.unique(tournaments_player, return_counts=True)
    
    header1, header2 = st.columns(2)
    header1.subheader("Players on Tour")
    header2.subheader("Tournaments on Tour")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric(label="2024", value=len(unique_players), delta=len(unique_players)-sum(tt))
    col2.metric(label="2023", value=sum(tt))

    col3.metric(label="2024", value=len(tourn), delta=len(tourn)-24)
    col4.metric(label="2023", value=24)

    tournaments_played = list(range(0, len(unique_tournaments[1])))
    

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=tournaments_played,
        y=unique_tournaments[1],
        name='2023/24 Season',
        marker_color='indianred'
    ))
    fig.add_trace(go.Bar(
        x=tournaments_played,
        y=tt,
        name='2022/23 Season',
        marker_color='lightsalmon'
    ))


    # Here we modify the tickangle of the xaxis, resulting in rotated labels.
    fig.update_layout(barmode='group', xaxis_tickangle=-45)
    st.plotly_chart(fig, use_container_width=True)


def showStats():
    st.header("Stats")

    draw_unique_player_chart()

   
        
showStats()
