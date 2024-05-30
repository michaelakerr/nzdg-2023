from google.cloud.firestore_v1.base_query import FieldFilter
from google.cloud import firestore
import streamlit as st
from CONSTANTS import PLAYER_TABLE_DB, TOURNAMENT_TABLE_DB
from non_pdga_tournaments import create_players_and_points_non_pdga_faultline
from pdga_scraper import create_player, create_players_and_points, get_total_points

def remove_tournament_and_player_points(db, remove_tournament):
    db.collection(TOURNAMENT_TABLE_DB).document(remove_tournament).delete()
            # remove from all players too 
    players = db.collection(PLAYER_TABLE_DB).where(
        filter=FieldFilter(str(remove_tournament), ">", 0)).stream()
    
    for player in players:
        if(remove_tournament in player.to_dict()):
            player.reference.update({f"{remove_tournament}": firestore.DELETE_FIELD})
            player_dict = player.to_dict()

            # remove tournament from dict
            player_dict.pop(remove_tournament)

            #recalculate total points
            total_points = get_total_points(db, player_dict)
            player.reference.set({
                "total": total_points
            }, merge=True)
            st.write(f"Removed player and points {player_dict['name']} from {remove_tournament}")

def add_tournament_and_players(db, name, url, points, major, order):
    name = name.replace(" ", "_")
    doc_ref = db.collection(TOURNAMENT_TABLE_DB).document(name)
    doc_ref.set({
        "name": name,
        "url": url,
        "points": points,
        "major": major,
        "order": order
    })
    # generate player info
    df = create_players_and_points(name, url, points)

    for index, player in df.iterrows():
        create_player(db, name, player)
    st.dataframe(df)

def add_tournament_and_players_non_pdga(db):
    name = "Faultline_Fury"
    doc_ref = db.collection(TOURNAMENT_TABLE_DB).document(name)
    doc_ref.set({
        "name": name,
        "url": "",
        "points": 40,
        "major": False,
        "order": 13
    })

    df = create_players_and_points_non_pdga_faultline()
    # generate player info

    for index, player in df.iterrows():
        create_player(db, name, player)
    st.dataframe(df)


def rearrange_tournament_order(db, sorted_items):
    for index, item in enumerate(sorted_items):
        db.collection(TOURNAMENT_TABLE_DB).document(item).update({"order": index})

    st.write(f"Rearranged tournaments: {sorted_items}")