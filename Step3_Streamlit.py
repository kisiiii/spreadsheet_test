import os
import streamlit as st
import pandas as pd
import numpy as np
import gspread
from google.oauth2.service_account import Credentials
from gspread_dataframe import set_with_dataframe
from dotenv import load_dotenv
from geopy.geocoders import Nominatim
import folium
from streamlit_folium import folium_static

# 環境変数の読み込み
load_dotenv()

# 環境変数から認証情報を取得
SPREADSHEET_ID = os.getenv("SPREADSHEET_ID")
PRIVATE_KEY_PATH = os.getenv("PRIVATE_KEY_PATH")
SP_SHEET     = 'tech0_01' # sheet名


# スプレッドシートからデータを読み込む関数
def load_data_from_spreadsheet():
    # googleスプレッドシートの認証 jsonファイル読み込み(key値はGCPから取得)
    SP_CREDENTIAL_FILE = PRIVATE_KEY_PATH

    scopes = [
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive'
    ]

    credentials = Credentials.from_service_account_file(
        SP_CREDENTIAL_FILE,
        scopes=scopes
    )
    gc = gspread.authorize(credentials)

    SP_SHEET_KEY = SPREADSHEET_ID # d/〇〇/edit の〇〇部分
    sh  = gc.open_by_key(SP_SHEET_KEY)

    # 不動産データの取得
    worksheet = sh.worksheet("TL_240221door_model_ver2") # シートのデータ取得
    pre_data  = worksheet.get_all_values()
    col_name = pre_data[0][:]
    df = pd.DataFrame(pre_data[1:], columns=col_name) # 一段目をカラム、以下データフレームで取得

    return df

# メインのアプリケーション
def main():
    df = load_data_from_spreadsheet()
    st.dataframe(df)


# アプリケーションの実行
if __name__ == "__main__":
    if 'search_clicked' not in st.session_state:
        st.session_state['search_clicked'] = False
    if 'show_all' not in st.session_state:
        st.session_state['show_all'] = False
    main()