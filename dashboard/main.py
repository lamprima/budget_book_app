# -*- coding: utf-8 -*-

import sys
import pandas as pd
import glob
import os
import datetime
import streamlit as st
#import matplotlib
import plotly.express as px
#from streamlit.runtime.scriptrunner import add_script_run_ctx,get_script_run_ctx
#from subprocess import Popen
from PIL import Image

from consts import *
from data_process import *


def set_config(im):
    
    st.set_page_config(
        page_title="家計簿アプリ",
        #page_icon="🧊",
        page_icon=im,
        layout="wide",
        initial_sidebar_state="expanded",
    )

if __name__ == '__main__':

    # 開始終了年月日を設定
    start_year:int = 2019
    end_year:int = datetime.datetime.today().year + 1

    # 読み込むシート名を作成
    sheet_names:list = make_sheet_names(start_year, end_year)
    
    # アプリのアイコン読み込み
    #im = Image.open("..\\ico\\app.ico")
    #im = Image.open("app.ico")

    #set_config(im)
    css = f'''
    <style>
        .stApp {{
            background-size: cover;
            background-position: center;
            background-color: black;
            color: rgb(0, 206, 209);
        }}
        .stApp > header {{
            background-color: black;
            color: rgb(0, 206, 209);
        }}
       [data-testid=stSidebar] {{
           background-color: rgb(47,79,79);
           color: rgb(0, 206, 209);
       }}
       [data-testid=stSelectbox] {{
           color: rgb(0, 206, 209);
       }}
       [data-testid=stMarkdownContainer] {{
           color: rgb(0, 206, 209);
       }}
    </style>
    '''
    st.markdown(css, unsafe_allow_html=True)

    st.markdown(HIDE_ST_STYLE, unsafe_allow_html=True)

    st.title('家計簿アプリ')
    
    st.sidebar.title("メニュー")
 
    uploaded_file:str = st.file_uploader("家計簿ファイルを選択してください")

    if not uploaded_file is None:
        
        # 家計簿データの辞書を作成
        budget_book = {}
        for sheet_name in sheet_names:
            #df = pd.read_excel("..\\input\\家計簿管理ツール.xlsm", sheet_name=sheet_name, index_col=None, usecols=[0,2,3,7,10,11])
            df = pd.read_excel(uploaded_file, sheet_name=sheet_name, index_col=None, usecols=[0,2,3,7,10,11])
            budget_book[sheet_name] = preprocess_budget_data(df)
        
        # サイドバーに表示する選択肢の初期化
        year_list:list = list(range(start_year, end_year))
        year_count:int = len(year_list)
        category_list = make_unique_value_list(budget_book, col_name=CONST.CATEGORY)
        category_count:int = len(category_list)
        category_detail_list = make_unique_value_list(budget_book,col_name=CONST.CATEGORY_DETAIL)
        category_detail_count:int = len(category_detail_list) 

        # サイドバーにアイテムを設置
        target_year:int = st.sidebar.selectbox('対象年', year_list, index=year_count - 1)
        compare_year:int = st.sidebar.selectbox('比較年', year_list, index=year_count - 2)
        analyze_time:str = st.sidebar.selectbox('分析断面', [CONST.YEAR, CONST.MONTH, CONST.DAY], index=0) 
        analyze_category_str:str = st.sidebar.selectbox('カテゴリーを使用', ['する', 'しない'], index=0) 
        analyze_category:bool = True if analyze_category_str == 'する' else False

        if analyze_category:
            category:str = st.sidebar.selectbox('カテゴリー', category_list, index=len(category_list) - 1)                          # 初期値を空欄とする
            category_detail:str = st.sidebar.selectbox('カテゴリー内訳', category_detail_list, index=len(category_detail_list) - 1)  # 初期値を空欄とする


        # アイテムの選択に応じて対象年、比較年のデータを並行に表示
        target_col, compare_col = st.columns(2)
        target_df = budget_book[make_sheet_name(target_year)]
        compare_df = budget_book[make_sheet_name(compare_year)]
        time_sum_target_df = time_sum_budget_data(target_df, analyze_time, analyze_category)
        target_y_dtick = round(time_sum_target_df[CONST.EXPENCE].max() / 4, -3)
        time_sum_compare_df = time_sum_budget_data(compare_df, analyze_time, analyze_category)
        compare_y_dtick = round(time_sum_compare_df[CONST.EXPENCE].max() / 4, -3)

        with target_col:
            st.write(str(target_year) + '年' )
            st.write('レコード数：' + str(len(target_df)))
            st.dataframe(target_df)
            st.write(analyze_time + '単位集計')
            st.dataframe(time_sum_target_df)
            #st.write(time_sum_budget_data(target_df, analyze_time).plot( y=['収入', '支出'], figsize=(16,4), alpha=0.5))
            #fig = px.line(time_sum_target_df, x=analyze_time, y=CONST.EXPENCE)
            if analyze_category:
                time_sum_target_df = time_sum_target_df.reset_index()
                fig = px.bar(time_sum_target_df, x=analyze_time, y=CONST.EXPENCE, color=CONST.CATEGORY, barmode='relative')
            else:
                fig = px.line(time_sum_target_df, y=CONST.EXPENCE)
            
            fig.update_yaxes(tick0=0, dtick=target_y_dtick)
            fig.update_xaxes(tick0=1, dtick=1)
            fig.update_yaxes(exponentformat='none', showline=True, linecolor='lightgrey', linewidth=2)
            fig.update_xaxes(showline=True, linecolor='lightgrey', linewidth=2)
            # ズームとパンの設定
            fig.update_layout(xaxis=dict(rangeslider=dict(visible=True)), dragmode="pan") # dragmodeの選択肢:pan, select
            st.plotly_chart(fig)
        
        with compare_col:
            st.write(str(compare_year) + '年' )
            st.write('レコード数：' + str(len(compare_df)))
            st.dataframe(compare_df)
            st.write(analyze_time + '単位集計')
            st.dataframe(time_sum_compare_df)

            if analyze_category:
                time_sum_compare_df = time_sum_compare_df.reset_index()
                figC = px.bar(time_sum_compare_df, x=analyze_time, y=CONST.EXPENCE, color=CONST.CATEGORY, barmode='relative')
            else:
                figC = px.line(time_sum_compare_df, y=CONST.EXPENCE)
            
            figC.update_yaxes(tick0=0, dtick=compare_y_dtick)
            figC.update_xaxes(tick0=1, dtick=1)
            figC.update_yaxes(exponentformat='none', showline=True, linecolor='lightgrey', linewidth=2)
            figC.update_xaxes(showline=True, linecolor='lightgrey', linewidth=2)
            # ズームとパンの設定
            figC.update_layout(xaxis=dict(rangeslider=dict(visible=True)), dragmode="pan") # dragmodeの選択肢:pan, select
            st.plotly_chart(figC)
    
        st.write()
    else:
        st.sidebar.write("ファイルを選択するとメニューが表示されます。")

