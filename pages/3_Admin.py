import json

import streamlit as st
import streamlit_authenticator as stauth
import yaml
from google.cloud import firestore
from google.oauth2 import service_account
from yaml.loader import SafeLoader

from pdga_scraper import create_player, create_players_and_points

with open('credentials.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

key_dict = json.loads(st.secrets["textkey"])
creds = service_account.Credentials.from_service_account_info(key_dict)
db = firestore.Client(credentials=creds)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
)

name, authentication_status, username = authenticator.login(
    'Login', 'main')

if authentication_status:
    authenticator.logout('Logout', 'main')
    if username == 'admin':
        st.write(f'Welcome *{name}*')
        st.title('Add a Tournament')

        name = st.text_input("Tournament Name")
        url = st.text_input("Tournament Url")
        points = st.number_input("Points")
        submit = st.button("Submit tournament")

# Once the user has submitted, upload it to the database
        if name and url and points and submit:
            doc_ref = db.collection("tournaments").document(name)
            doc_ref.set({
                "name": name,
                "url": url,
                "points": points
            })
            # generate player info
            df = create_players_and_points(name, url, points)
            for index, player in df.iterrows():
                create_player(db, name, player)
            st.dataframe(df)


elif authentication_status == False:
    st.error('Username/password is incorrect')
elif authentication_status == None:
    st.warning('Please enter your username and password')
