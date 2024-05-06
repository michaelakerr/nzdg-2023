import json
import pandas as pd
import streamlit as st
from google.cloud import firestore
from google.oauth2 import service_account

key_dict = json.loads(st.secrets["textkey"])
creds = service_account.Credentials.from_service_account_info(key_dict)
db = firestore.Client(credentials=creds)

# def get_all_players():
#     players = db.collection(u'players').stream()
#     return players

# def export_players_to_csv():
#     players = db.collection(u'players')

#     df = pd.DataFrame(columns=['name', 'email', 'tour_division', 'total', 'points', 'pdga_number', 'url'])

#     for doc in players.stream():
#         player = doc.to_dict()

#         player['pdga_number'] = player['pdga_number']

#         player['name'] = str(player['name'])
#         df = pd.concat([df, pd.DataFrame([player])], ignore_index=True)
        


#     df.to_csv('players.csv', index=False)

#     return df


def read__players_csv():
    df = pd.read_csv('players.csv')
    return df

def get_name_and_pdga():
    df = read__players_csv()
    df = df[['name', 'pdga_number']]

    # remove .0 from pdga number
    df['pdga_number'] = df['pdga_number'].astype(str).str.replace('.0', '')

    #remove duplicate rows based on PDGA number 
    df.drop_duplicates(subset=['pdga_number'], inplace=True)



    df.to_csv('players_with_pdga.csv', index=False)

    return df[['name', 'pdga_number']]


def read_players_with_emails():
    df = pd.read_csv('NZDG_2024.csv')
    df = df[['name', 'pdga_number']]
    print(df)
    df_nzdg = pd.read_csv('tepohue.csv')

    df_nzdg['Name'] = df_nzdg['Firstname'] + ' ' + df_nzdg['Lastname']

    df_nzdg = df_nzdg[['Name', 'PDGA#','Email']]

    #df_nzdg.to_csv('nzdg_2020.csv', index=False)
   # df_Nationals = pd.read_csv('auckland_champs.csv')
    # join first name and last name on df_nationals
   # df_Nationals['name'] = df_Nationals['First name'] + ' ' + df_Nationals['Last name']
    # remove from df_nationals columns that are not needed
   # df_Nationals = df_Nationals[['PDGA#', 'Name', 'Email']]
    #rename Pdga# to pdga_number
    df_nzdg.rename(columns={'PDGA#': 'pdga_number'}, inplace=True)
    df_nzdg.rename(columns={'Name': 'name'}, inplace=True)
    #df_nzdg['pdga_number'] = df_nzdg['pdga_number'].astype(str, errors='ignore')
   # df_Nationals.rename(columns={'Name': 'name'}, inplace=True)
   # df.rename(columns={'Combined_Email_1', 'Email'}, inplace=True)
    
    print(df_nzdg)

    #combine email_x, email_y and email in df 
    #df['Email_'] = df.apply(lambda row: row['Email'] if pd.notnull(row['Email']) else row['Combined_Email_1'], axis=1)
    #df['Combined_Email_1'] = df.apply(lambda row: row['Combined_Email'] if pd.notnull(row['Combined_Email']) else row['Email'], axis=1)

    # # Drop the empty column if needed
   # df.drop(columns=['Email', "Combined_Email_1"], inplace=True, errors='ignore')

    # # Optionally, you can drop the individual email columns if they are no longer needed
    # df.drop(columns=['Email_x', 'Email_y', "Combined_Email", "Email"], inplace=True)
    # print(df)
   # df = pd.merge(df, df_nzdg, how='left', on=['pdga_number'])
    df = pd.merge(df, df_nzdg, how='left', on=['name'])
   # df['Email'] = df.apply(lambda row: row['Email_'] if pd.notnull(row['Email_']) else row['email'], axis=1)

    # Drop the empty column if needed
    #df.drop(columns=['Email_', 'email'], inplace=True, errors='ignore')


    df.to_csv('players_with_emails_qt.csv', index=False)

    return df

read_players_with_emails()