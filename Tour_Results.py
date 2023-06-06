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


def display_results(scoring_group):
    users_dict = list(map(lambda x: x.to_dict(), scoring_group))
    df = pd.DataFrame(users_dict)
    df = df.drop(['key', 'scoring_group'], axis=1)

    cols = ['pdga_number', 'name', 'total']
    df = df[cols + [c for c in df.columns if c not in cols]]

    df = df.sort_values(by="total", ascending=False)
    return df


# SCORING GROUP 1
st.subheader("Scoring Group 1: MPO")
scoring_group_1 = list(db.collection('players').where(
    'scoring_group', '==', 1).stream())

df1 = display_results(scoring_group_1)
st.dataframe(df1, hide_index=True, column_config=config)

st.subheader("Scoring Group 2: MP40, MP50")
scoring_group_2 = list(db.collection('players').where(
    'scoring_group', '==', 2).stream())

df2 = display_results(scoring_group_2)
st.dataframe(df2, hide_index=True, column_config=config)

st.subheader("Scoring Group 3: FPO, MA1")
scoring_group_3 = list(db.collection('players').where(
    'scoring_group', '==', 3).stream())

df3 = display_results(scoring_group_3)
st.dataframe(df3, hide_index=True, column_config=config)

st.subheader("Scoring Group 4: MA40, MA50")
scoring_group_4 = list(db.collection('players').where(
    'scoring_group', '==', 4).stream())

df4 = display_results(scoring_group_4)
st.dataframe(df4, hide_index=True, column_config=config)

st.subheader("Scoring Group 5: MA2")
scoring_group_5 = list(db.collection('players').where(
    'scoring_group', '==', 5).stream())

df5 = display_results(scoring_group_5)
st.dataframe(df5, hide_index=True, column_config=config)

st.subheader("Scoring Group 6: All Other Divisions")
scoring_group_6 = list(db.collection('players').where(
    'scoring_group', '==', 6).stream())

df6 = display_results(scoring_group_6)
st.dataframe(df6, hide_index=True, column_config=config)
