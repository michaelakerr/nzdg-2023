import json

import pandas as pd
import streamlit as st
from google.cloud import firestore
from google.cloud.firestore_v1.base_query import FieldFilter
from google.oauth2 import service_account
from CONSTANTS import PLAYER_TABLE_DB

from pdga_scraper import get_all_tournaments

key_dict = json.loads(st.secrets["textkey2"])
creds = service_account.Credentials.from_service_account_info(key_dict)
db = firestore.Client(credentials=creds)

config = {
    "pdga number": st.column_config.TextColumn(
        "PDGA #",
    ),
    "name": st.column_config.TextColumn(
        "Player",
    ),
    "total": st.column_config.NumberColumn(
        "Total Points",
        format="%.2f",
    ),
}


map_tour_groups = {
    "Open - Mixed": ["MPO"],
    "Open - Women": ["FPO"],
    "Pro Masters - Mixed": ["MP40", "MP50"],
    "Advanced - Mixed": ["MA1"],
    "Advanced - Women": ["FA1", "FA2", "FA3", "FA4"],
    "Intermediate - Mixed": ["MA2"],
    "Amateur - Mixed": ["MA3", "MA4"],
    "Amateur Masters - Mixed": ["MA40"],
    "Masters - Women": ["FP40", "FA40"],
    "Amateur Grand Masters - Mixed": ["MA50"],
    "Grand Masters - Women": ["FA50", "FP50"],
    "Senior Grand Masters - Mixed": ["MA60", "MP60"],
    "Senior Grand Masters - Women": ["FA60", "FP60"],
    "Legends - Mixed": ["MA70", "MP70"],
    "Legends - Women": ["FA70", "FP70"],
    "Juniors - Mixed": ["MJ18", "MJ15", "MJ12", "MJ10", "MJ08", "MJ06"],
    "Juniors - Women": ["FJ18", "FJ15", "FJ12", "FJ10", "FJ08", "FJ06"],
}


def display_results(scoring_group):
    users_dict = list(map(lambda x: x.to_dict(), scoring_group))
    df = pd.DataFrame(users_dict)
    df = df.drop(["key", "scoring_group", "Player_Group", "tour_division"], axis=1)

    tournaments_stream = get_all_tournaments(db)
    tournaments = []
    for t in tournaments_stream:
        if t.exists:
            tournaments.append(t.to_dict())

    if len(tournaments) == 0:
        st.write("No tournaments entered yet")
        return None

    tournament_df = pd.DataFrame(tournaments)
    if len(tournament_df) > 0:
        # sort df by order column
        tournament_df = tournament_df.sort_values(by="order")
        player_tour_names = df.columns.values.tolist()
        all_tour_names = list(tournament_df["name"])

        # find tournaments in dataset that exist to order by
        matcher = []
        for a in all_tour_names:
            if a in player_tour_names:
                matcher.append(a)

        df = df.sort_values(by="total", ascending=False)
        df["Place"] = df["total"].rank(ascending=False, method="min")
        cols = ["Place", "pdga_number", "name", "total"] + matcher
        df = df[cols]
        return df
    else:
        return None


def display_group_results(group):
    score_list = list(
        db.collection(PLAYER_TABLE_DB)
        .where(filter=FieldFilter("tour_division", "==", group))
        .stream()
    )
    if len(score_list) > 0:
        df6 = display_results(score_list)
        st.subheader(group)
        st.caption(", ".join(map_tour_groups[group]))
        if df6 is not None:
            # remove underscores from headers in dataframe
            df6.columns = df6.columns.str.replace("_", " ")
            st.dataframe(df6, hide_index=True, column_config=config)
        else:
            st.write("No results yet")


for group in map_tour_groups:
    if st.button(group, key=group):
        display_group_results(group)
