import json

import streamlit as st
from google.cloud import firestore
from google.oauth2 import service_account

key_dict = json.loads(st.secrets["textkey"])
creds = service_account.Credentials.from_service_account_info(key_dict)
db = firestore.Client(credentials=creds)

st.set_page_config(initial_sidebar_state="collapsed")


def showTournaments():
    posts_ref = db.collection("tournaments")

    for doc in posts_ref.stream():
        post = doc.to_dict()
        name = post["name"]
        url = post["url"]
        points = post["points"]

        st.subheader(f"Tournament: {name}")
        st.write(f":link: [{url}]({url})")
        st.write(f"Points: {points}")


showTournaments()
