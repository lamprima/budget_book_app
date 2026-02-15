# -*- coding: utf-8 -*-

import sys
import pandas as pd
import glob
import os
import datetime
import streamlit as st
import json
#import matplotlib
import plotly.express as px
from PIL import Image
from consts import *
from data_process import *

if __name__ == '__main__':

    # 開始終了年月日を設定
    start_year:int = 2018
    end_year:int = datetime.datetime.today().year + 1
    asset_end_year:int = 1993 + 120 + 1

    # 読み込むシート名を作成（家計簿）
    sheet_names:list = make_sheet_names(start_year, end_year)

    # 読み込むシート名を作成（資産管理）
    excel_read_setting_file = '..\\setting\\excel_read_setting.json'
    sheet_name_list, usecols_list, header_list = get_excel_read_setting(excel_read_setting_file)

    # 資産運用データをグラフ化するための時系列データフレームを作成（年、年月、日）
    year_df, yearmon_df, daily_df = make_df_for_asset(start_year, asset_end_year)
    
    # アプリのアイコン読み込み
    im = Image.open("..\\ico\\app.ico")
    #im = Image.open("app.ico")

    set_config(im)
    st.markdown(CSS, unsafe_allow_html=True)
    st.markdown(HIDE_ST_STYLE, unsafe_allow_html=True)

    #uploaded_file:str = st.file_uploader("家計簿ファイルを選択してください")
    uploaded_file = ""
    progress_bar = st.progress(0)

    # プログレスバーの分母
    progress_number = len(sheet_names) + len(sheet_name_list)
    # プログレスバーの分子
    progress_count = 0

    if not uploaded_file is None:
        
        # 家計簿データの辞書を作成
        budget_book = {}
        asset_book = {}
        # 諸元データを読み込むのは初回のみ
        if not SESSION.BUDGET_BOOK in st.session_state:
            st.write('家計簿管理ツール')
            for sheet_name in sheet_names:
                df = pd.read_excel("C:\\Temp\\日本株分析\\家計簿管理ツール.xlsm", sheet_name=sheet_name, index_col=None, usecols=[0,2,3,7,10,11])
                #df = pd.read_excel(uploaded_file, sheet_name=sheet_name, index_col=None, usecols=[0,2,3,7,10,11])
                df = add_YYYYMMDD_data(df, CONST.DATE)
                df = df.iloc[:, [0,6,7,8,1,2,4,5,3]]
                budget_book[sheet_name] = df
                progress_count += 1
                progress_bar.progress(progress_count / progress_number, \
                                      text=make_progress_message(progress_count, progress_number, '家計簿管理ツール', sheet_name))
                st.write(make_progress_complete_message(sheet_name))
            st.session_state[SESSION.BUDGET_BOOK] = budget_book
        else:
            budget_book = st.session_state[SESSION.BUDGET_BOOK]
            #progress_bar.close()
        if not SESSION.ASSET_BOOK in st.session_state:
            st.write('資産管理ツール')
            for sheet_name, usecols, header in zip(sheet_name_list, usecols_list, header_list):
                df = pd.read_excel("C:\\Temp\\日本株分析\\資産運用ツール.xlsm", sheet_name=sheet_name, index_col=None, usecols=usecols, header=header)
                #df = pd.read_excel(uploaded_file, sheet_name=sheet_name, index_col=None, usecols=[0,2,3,7,10,11])
                #asset_book[sheet_name] = preprocess_asset_data(df)
                asset_book[sheet_name] = df
                progress_count += 1
                progress_bar.progress(progress_count / progress_number, \
                                      text=make_progress_message(progress_count, progress_number, '資産管理ツール', sheet_name))
                st.write(make_progress_complete_message(sheet_name))
                progress_bar.empty()
            st.session_state[SESSION.ASSET_BOOK] = asset_book

            # 各ページで利用する集計済みデータを作成
            jpx_divide_df = make_jpx_divide_df(asset_book['銘柄マスタ'], asset_book['日本資産配当'])
        else:
            asset_book = st.session_state[SESSION.ASSET_BOOK]
            jpx_divide_df = make_jpx_divide_df(asset_book['銘柄マスタ'], asset_book['日本資産配当'])
        
        # 各ページに共有する変数を設定
        st.session_state[SESSION.IM] = im
        st.session_state[SESSION.YEAR_DF] = year_df
        st.session_state[SESSION.YEARMON_DF] = yearmon_df
        st.session_state[SESSION.DAILY_DF] = daily_df
        st.session_state[SESSION.START_YEAR] = start_year
        st.session_state[SESSION.END_YEAR] = end_year
        st.session_state[SESSION.ASSET_END_YEAR] = asset_end_year
        st.session_state['jpx_divide_df'] = jpx_divide_df

        st.write('データ読み込み完了')

    else:
        st.sidebar.write("ファイルを選択するとメニューが表示されます。")

