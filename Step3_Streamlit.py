import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
from gspread_dataframe import set_with_dataframe
import json

# スプレッドシートからデータを読み込む関数
def load_data_from_spreadsheet():
    scopes = [
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive'
    ]

    # secrets.tomlから認証情報を取得
    google_credentials = {
        "type": st.secrets["GOOGLE_CREDENTIALS"]["type"],
        "project_id": st.secrets["GOOGLE_CREDENTIALS"]["project_id"],
        "private_key_id": st.secrets["GOOGLE_CREDENTIALS"]["private_key_id"],
        "private_key": st.secrets["GOOGLE_CREDENTIALS"]["private_key"],
        "client_email": st.secrets["GOOGLE_CREDENTIALS"]["client_email"],
        "client_id": st.secrets["GOOGLE_CREDENTIALS"]["client_id"],
        "auth_uri": st.secrets["GOOGLE_CREDENTIALS"]["auth_uri"],
        "token_uri": st.secrets["GOOGLE_CREDENTIALS"]["token_uri"],
        "auth_provider_x509_cert_url": st.secrets["GOOGLE_CREDENTIALS"]["auth_provider_x509_cert_url"],
        "client_x509_cert_url": st.secrets["GOOGLE_CREDENTIALS"]["client_x509_cert_url"]
    }

    credentials = Credentials.from_service_account_info(
        google_credentials, scopes=scopes
    )
    gc = gspread.authorize(credentials)
    SP_SHEET_KEY = st.secrets["SP_SHEET_KEY"]
    sh = gc.open_by_key(SP_SHEET_KEY)

    # 不動産データの取得
    worksheet = sh.worksheet("TL_240221door_model_ver2")
    pre_data = worksheet.get_all_values()
    col_name = pre_data[0][:]
    df = pd.DataFrame(pre_data[1:], columns=col_name)

    return df

# メインのアプリケーション
def main():
    df = load_data_from_spreadsheet()
    st.dataframe(df)

# アプリケーションの実行
if __name__ == "__main__":
    main()
