import datetime
import streamlit as st
import plotly.express as px
# パッケージの上位フォルダを追加し。data_process.pyが見つかるようにする
# そのままでは上位階層のpythonファイルをインポートできない　ImportError: attempted relative import with no known parent package
import sys
sys.path.append('C:\\temp\\日本株分析\\dashboard\\dashboard')
from data_process import *
from consts import *

if 'asset_book' in st.session_state:
    
    # main.pyからのデータを受け取る
    asset_book = st.session_state[SESSION.ASSET_BOOK]
    im = st.session_state['im']
    year_df = st.session_state['year_df']
    yearmon_df = st.session_state['yearmon_df']
    daily_df = st.session_state['daily_df']
    start_year = st.session_state['start_year']
    end_year = st.session_state['end_year']
    asset_end_year = st.session_state['asset_end_year']
    jpx_divide_df = st.session_state['jpx_divide_df']

    # サイドバーに表示する選択肢の初期化
    year_list:list = list(range(start_year, asset_end_year))
    month_list:list = list(range(1, 13))

    # データフレームからデータを取得



    


    # 楽天証券VTI投資信託データの作成

    # SBI証券VTI投資信託サマリーデータの作成


    # 楽天証券VTI投資信託サマリーデータの作成

    
    # ページ設定
    set_config(im)
    st.markdown(CSS, unsafe_allow_html=True)
    st.markdown(HIDE_ST_STYLE, unsafe_allow_html=True)

    st.title('JPX 配当金')
    
    st.sidebar.title("メニュー")
    # サイドバーに表示する選択肢の初期化
    year_list:list = list(range(start_year, end_year))
    year_list.insert(0, 0)
    year_count:int = len(year_list)

    # サイドバーにアイテムを設置
    target_year:int = st.sidebar.selectbox('対象年', year_list, index=year_count - 1)
    display_data_str:str = st.sidebar.selectbox('データを表示', ['する', 'しない'], index=0)      # カテゴリー：使用する
    display_data:bool = True if display_data_str == 'する' else False

    #サマリーデータの表示
    st.write('サマリー')
    jpx_year_divide_df = []
    jpx_year_divide_df = make_jpx_year_divide_df(jpx_divide_df, start_year, end_year) 
    jpx_summary_data = make_jpx_summary_data(jpx_year_divide_df)
    
    # アイテムの選択に応じて対象年、比較年のデータを並行に表示
    data_col, graph_col = st.columns(2)
    df = extract_year_jpx_summary_data(jpx_summary_data, target_year)
    with data_col:
        st.dataframe(df.drop('配当合計[￥]', axis=1), hide_index=True, use_container_width=True)

    with graph_col:
        fig = px.pie(df.drop('配当合計', axis=1), names='項目', values='配当合計[￥]', title=' ')
        st.plotly_chart(pie_graph_setting(fig), use_container_width=True)


    # 楽天証券VTI投資信託グラフデータの作成

    # y軸区切りは入金合計/4

    # グラフの書式設定

    if display_data:
        pass
    
    # SBI証券


else:
    st.write('not exists!!')