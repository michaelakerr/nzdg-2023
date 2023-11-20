import json

import streamlit as st
import pandas as pd
import streamlit_authenticator as stauth
import yaml
from streamlit_sortables import sort_items
from google.cloud import firestore
from google.oauth2 import service_account
from yaml.loader import SafeLoader
from admin_tasks import add_tournament_and_players, rearrange_tournament_order, remove_tournament_and_player_points
from pdga_scraper import get_all_tournaments

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
        tournaments = get_all_tournaments(db)
        tournaments_list = list(map(lambda x: x.to_dict(), tournaments))
        tournament_df = pd.DataFrame(tournaments_list)
        max_value = 1
        
        # sort df by order column
        if len(tournaments_list) > 0:
            default_order = tournament_df.sort_values(by="order")
            max_value = default_order['order'].max() +1

        st.write(f'Welcome *{name}*')
        st.title('Add a Tournament')

        name = st.text_input("Tournament Name")
        url = st.text_input("Tournament Url")
        points = st.number_input("Points")
        major = st.checkbox("Is this a major tournament?")
        tournament_order = st.number_input("Tournament order", value=max_value)

        submit = st.button("Submit tournament")

        st.divider()

        st.title("Remove a tournament")
        tournaments = get_all_tournaments(db)

        names = []

        #setup tournament names
        for tournament in tournaments:
            names.append(tournament.id)

        remove_tournament = st.selectbox("Select which tournament to remove", names)
        remove = st.button("Remove tournament")

        st.divider()
        st.title('Rearrange Tournaments')

        tournament_sorter = get_all_tournaments(db)

        names_in_order = []

        #setup tournament names
        for tournament in tournament_sorter:
            names_in_order.append(tournament.id)

        sorted_items = sort_items(names_in_order)

        rearrange_tournaments = st.button("Rearrange tournaments")

        #Remove tournaments
        if remove_tournament and remove:
            remove_tournament_and_player_points(db, remove_tournament)

        # Once the user has submitted, upload it to the database
        if name and url and points and submit:
            add_tournament_and_players(db, name, url, points, major, tournament_order)

        if rearrange_tournaments and sorted_items: 
            rearrange_tournament_order(db, sorted_items)

elif authentication_status == False:
    st.error('Username/password is incorrect')
elif authentication_status == None:
    st.warning('Please enter your username and password')

