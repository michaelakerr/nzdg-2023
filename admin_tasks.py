# from google.cloud.firestore_v1.base_query import FieldFilter
from google.cloud import firestore
import streamlit as st
from CONSTANTS import PLAYER_TABLE_DB, TOURNAMENT_TABLE_DB
from non_pdga_tournaments import create_players_and_points_non_pdga_faultline
from pdga_scraper import create_player, create_players_and_points, get_total_points
import re
from firebase_admin.firestore import FieldFilter
from firebase_admin import firestore


def remove_tournament_and_player_points(db, remove_tournament):
    """Removes a tournament from all players and recalculates total points."""
    db.collection(TOURNAMENT_TABLE_DB).document(remove_tournament).delete()

    # Query players who have this tournament field
    players = (
        db.collection(PLAYER_TABLE_DB)
        .where(filter=FieldFilter(remove_tournament, ">", 0))  # Correct FieldPath usage
        .stream()
    )

    for player in players:
        player_dict = player.to_dict()

        if remove_tournament in player_dict:
            # Remove tournament field from Firestore
            player.reference.update({remove_tournament: firestore.DELETE_FIELD})

            # Remove from local dictionary
            player_dict.pop(remove_tournament, None)

            # Recalculate total points
            total_points = get_total_points(db, player_dict)

            # Update the total points field
            player.reference.set({"total": total_points}, merge=True)
            st.write(
                f"Removed player and points {player_dict['name']} from {remove_tournament}"
            )


def add_tournament_and_players(db, name, url, points, major, order):
    name = name.replace(" ", "_")
    name = name.replace("-", "_")
    name = re.sub(r"[^a-zA-Z0-9_]", "", name)
    doc_ref = db.collection(TOURNAMENT_TABLE_DB).document(name)
    doc_ref.set(
        {"name": name, "url": url, "points": points, "major": major, "order": order}
    )
    # generate player info
    df = create_players_and_points(name, url, points)

    for index, player in df.iterrows():
        create_player(db, name, player)
    st.dataframe(df)


def add_tournament_and_players_non_pdga(db):
    name = "Faultline_Fury"
    doc_ref = db.collection(TOURNAMENT_TABLE_DB).document(name)
    doc_ref.set({"name": name, "url": "", "points": 40, "major": False, "order": 13})

    df = create_players_and_points_non_pdga_faultline()
    # generate player info

    for index, player in df.iterrows():
        create_player(db, name, player)
    st.dataframe(df)


def rearrange_tournament_order(db, sorted_items):
    for index, item in enumerate(sorted_items):
        db.collection(TOURNAMENT_TABLE_DB).document(item).update({"order": index})

    st.write(f"Rearranged tournaments: {sorted_items}")
