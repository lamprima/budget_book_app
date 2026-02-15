import datetime
import streamlit as st
import plotly.express as px
# パッケージの上位フォルダを追加し。data_process.pyが見つかるようにする
# そのままでは上位階層のpythonファイルをインポートできない　ImportError: attempted relative import with no known parent package
import sys
sys.path.append('C:\\temp\\日本株分析\\dashboard\\dashboard')
from data_process import *
from consts import *

if 'budget_book' in st.session_state:
    
    # main.pyからのデータを受け取る
    budget_book = st.session_state['budget_book']
    im = st.session_state['im']
    year_df = st.session_state['year_df']
    yearmon_df = st.session_state['yearmon_df']
    daily_df = st.session_state['daily_df']
    start_year = st.session_state['start_year']
    end_year = st.session_state['end_year']

    # タイトル
    st.title('家計簿アプリ')
    st.sidebar.title("メニュー")

    # ページ設定
    set_config(im)
    st.markdown(CSS, unsafe_allow_html=True)
    st.markdown(HIDE_ST_STYLE, unsafe_allow_html=True)

    # サイドバーに表示する選択肢の初期化
    year_list:list = list(range(start_year, end_year))
    year_list.insert(0, 0)
    year_count:int = len(year_list)
    category_list = make_unique_value_list(budget_book, col_name=CONST.CATEGORY)
    category_count:int = len(category_list)
    category_detail_list = make_unique_value_list(budget_book,col_name=CONST.CATEGORY_DETAIL)
    category_detail_count:int = len(category_detail_list) 

    # サイドバーにアイテムを設置
    target_year:int = st.sidebar.selectbox('対象年', year_list, index=year_count - 1)
    compare_year:int = st.sidebar.selectbox('比較年', year_list, index=0)                               # 初期値は0（比較しない）
    analyze_time:str = st.sidebar.selectbox('分析断面', [CONST.YEAR, CONST.MONTH, CONST.DAY], index=1)  # 初期値は月 
    analyze_category_str:str = st.sidebar.selectbox('カテゴリーを使用', ['する', 'しない'], index=0)      # カテゴリー：使用する
    analyze_category:bool = True if analyze_category_str == 'する' else False

    if analyze_category:
        category:str = st.sidebar.selectbox('カテゴリー', category_list, index=len(category_list) - 1)                          # 初期値を空欄とする
        category_detail:str = st.sidebar.selectbox('カテゴリー内訳', category_detail_list, index=len(category_detail_list) - 1)  # 初期値を空欄とする

        # アイテムの選択に応じて対象年、比較年のデータを並行に表示
        target_col, compare_col = st.columns(2)

        target_df = budget_book[make_sheet_name(target_year)]
        time_sum_target_df = time_sum_budget_data(target_df, analyze_time, analyze_category)
        target_y_dtick = round(time_sum_target_df[CONST.EXPENCE].max() / 4, -3)
        if compare_year > 0:
            compare_df = budget_book[make_sheet_name(compare_year)]
            time_sum_compare_df = time_sum_budget_data(compare_df, analyze_time, analyze_category)
            compare_y_dtick = round(time_sum_compare_df[CONST.EXPENCE].max() / 4, -3) #Y軸の区切り単位

        #st.dataframe(year_df)
        #st.dataframe(yearmon_df)
        #st.dataframe(daily_df)

        with target_col:
            st.write(str(target_year) + '年' )
            if analyze_category:
                time_sum_target_df = time_sum_target_df.reset_index()
                fig = px.bar(time_sum_target_df, x=analyze_time, y=CONST.EXPENCE, color=CONST.CATEGORY, barmode='relative')
            else:
                fig = px.line(time_sum_target_df, y=CONST.EXPENCE)
            
            fig.update_yaxes(tick0=0, dtick=target_y_dtick)

            # グラフの書式設定
            fig = graph_setting(fig, '支出グラフ')
            st.plotly_chart(fig)
        if compare_year > 0:
            with compare_col:
                st.write(str(compare_year) + '年' )
                if analyze_category:
                    time_sum_compare_df = time_sum_compare_df.reset_index()
                    figC = px.bar(time_sum_compare_df, x=analyze_time, y=CONST.EXPENCE, color=CONST.CATEGORY, barmode='relative')
                else:
                    figC = px.line(time_sum_compare_df, y=CONST.EXPENCE)
            
                figC.update_yaxes(tick0=0, dtick=compare_y_dtick)
                # グラフの書式設定
                figC = graph_setting(figC, '支出グラフ')
                st.plotly_chart(figC)
    
            st.write()