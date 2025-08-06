from sqlalchemy import create_engine
import pandas as pd
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

def load_to_postgresql(df, table_name='product'):
    try:
        username = 'developer'
        password = '1234'
        host = 'localhost'
        port = '5432'
        database = 'productdb'

        engine = create_engine(f'postgresql+psycopg2://{username}:{password}@{host}:{port}/{database}')

        with engine.begin() as conn:
            df.to_sql(table_name, conn, if_exists='replace', index=False)

        print(f"Data berhasil disimpan ke PostgreSQL table '{table_name}'.")

    except Exception as e:
        print(f"Gagal menyimpan ke PostgreSQL: {e}")
        
def load_to_csv(df, filename):
    df.to_csv(filename, index=False)

def load_to_google_sheets(
    df,
    range_name,
    spreadsheet_id='1oIxZtCuPFbzuYMxkOWabo4xSjc5FTdrJ5erN122FZY4',
    service_account_file='client_secret.json'
):
    try:
        SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
        creds = Credentials.from_service_account_file(service_account_file, scopes=SCOPES)
        service = build('sheets', 'v4', credentials=creds)
        sheet = service.spreadsheets()

        values = [df.columns.values.tolist()] + df.values.tolist()

        body = {
            'values': values
        }

        sheet.values().update(
            spreadsheetId=spreadsheet_id,
            range=range_name,
            valueInputOption='RAW',
            body=body
        ).execute()

        print("Data berhasil disimpan ke Google Sheets.")

    except Exception as e:
        print(f"Gagal menyimpan ke Google Sheets: {e}")