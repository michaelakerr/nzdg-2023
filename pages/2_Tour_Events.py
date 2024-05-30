import json

import streamlit as st

import json

from google.cloud import firestore
from google.oauth2 import service_account

from CONSTANTS import TOURNAMENT_TABLE_DB


key_dict = json.loads(st.secrets["textkey"])
creds = service_account.Credentials.from_service_account_info(key_dict)
db = firestore.Client(credentials=creds)

def showTournaments():

    posts_ref = db.collection(TOURNAMENT_TABLE_DB).order_by("order").stream()
    st.header("Tour Events")

    for doc in posts_ref:
        if doc is not None:
            post = doc.to_dict()
            name = post["name"]
            url = post["url"]
            points = post["points"]
            major = post["major"]

            st.subheader(f"{name.replace('_', ' ')}")
            st.write(f":link: [{url}]({url})")
            st.write(f"Points: {points}")
            if major:
                st.write(f"Major")
        else:
            st.write("No tournaments yet")
            return

    #export_players_to_csv()


showTournaments()
