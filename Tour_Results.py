import json

import pandas as pd
import streamlit as st
from google.cloud import firestore
from google.oauth2 import service_account

key_dict = json.loads(st.secrets["textkey"])
creds = service_account.Credentials.from_service_account_info(key_dict)
db = firestore.Client(credentials=creds)

config = {
    "pdga_number": st.column_config.TextColumn(
        "PDGA #",
    ),
    "name": st.column_config.TextColumn(
        "Player",
    ),
    "total": st.column_config.NumberColumn(
        "Total Points",
        format="%.2f",
    )
}

map_tour_groups = {
    "Open - Mixed": ['MPO'],
    "Pro Masters - Mixed": ['MP40', 'MP50'],
    "Advanced - Mixed": ['MA1'],
    "Intermediate - Mixed": ['MA2', 'MA3', 'MA4'],
    "Amateur Masters - Mixed": ['MA40'],
    "Amateur Grand Masters - Mixed": ['MA50'],
    "Senior Grand Masters - Mixed": ['MA60', "MP60"],
    "Legends - Mixed": ['MA70', "MP70"],
    "Juniors - Mixed": ["MJ18", "MJ15", "MJ12", "MJ10", "MJ08", "MJ06"],
    "Open - Women": ['FPO'],
    "Advanced - Women": ['FA1', "FA2", "FA3", "FA4"],
    "Masters - Women": ['FP40', "FA40"],
    "Grand Masters - Women": ["FA50", "FP50"],
    "Senior Grand Masters - Women": ["FA60", "FP60"],
    "Legends - Women": ["FA70", "FP70"],
    "Juniors - Women": ["FJ18", "FJ15", "FJ12", "FJ10", "FJ08", "FJ06"],
}


def display_results(scoring_group):
    users_dict = list(map(lambda x: x.to_dict(), scoring_group))
    df = pd.DataFrame(users_dict)
    df = df.drop(['key', 'scoring_group',
                 'group', 'tour_division'], axis=1)

    df = df.sort_values(by="total", ascending=False)
    df['Place'] = df['total'].rank(ascending=False, method="min")

    cols = ['Place', 'pdga_number', 'name', 'total']
    df = df[cols + [c for c in df.columns if c not in cols]]
    return df


# SCORING GROUP 1
for group in map_tour_groups:
    score_list = list(db.collection('players').where(
        'tour_division', '==', group).stream())
    if len(score_list) > 0:
        df6 = display_results(score_list)
        st.subheader(group)
        st.caption(', '.join(map_tour_groups[group]))
        st.dataframe(df6, hide_index=True, column_config=config)
