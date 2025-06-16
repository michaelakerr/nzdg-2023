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


pages = {
    "Current Tour Year (25/26)": [
        st.Page("my_pages/1_Tour_Results.py", title="Tour Results"),
        st.Page("my_pages/2_Tour_Events.py", title="Tour Events"),
    ],
    "Previous Tour Years": [
        # another nested breakpoint
        st.Page("my_pages/5_23_24_Tour_Results.py", title="Tour Results 23/24"),
        st.Page("my_pages/6_23_24_Tour_Events.py", title="Tour Events 23/24"),
        st.Page("my_pages/7_24_25_Tour_Results.py", title="Tour Results 24/25"),
        st.Page("my_pages/8_24_25_Tour_Events.py", title="Tour Events 24/25"),
    ],
    "More Information": [
        st.Page("my_pages/3_About_the_tour_points.py", title="About the Tour Points"),
    ],
    "Admin": [
        st.Page("my_pages/4_Admin.py", title="Admin"),
    ],
}


# SCORING GROUP 1
pg = st.navigation(pages)
pg.run()
