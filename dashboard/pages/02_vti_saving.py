import datetime
import streamlit as st
# パッケージの上位フォルダを追加し、data_process.pyが見つかるようにする
# そのままでは上位階層のpythonファイルをインポートできない　ImportError: attempted relative import with no known parent package
import sys
sys.path.append('C:\\temp\\日本株分析\\dashboard\\dashboard')
from data_process import *
from consts import *

if 'asset_book' in st.session_state:
    
    # main.pyからのデータを受け取る
    asset_book = st.session_state['asset_book']
    im = st.session_state['im']
    year_df = st.session_state['year_df']
    yearmon_df = st.session_state['yearmon_df']
    daily_df = st.session_state['daily_df']
    start_year = st.session_state['start_year']
    asset_end_year = st.session_state['asset_end_year']

    # サイドバーに表示する選択肢の初期化
    year_list:list = list(range(start_year, asset_end_year))
    month_list:list = list(range(1, 13))

    mutual_funds = asset_book['取引履歴(円建・投信)']
    sell_funds = asset_book['取引履歴(円建・東証)']
    mutual_funds[CONST.BUY_SELL_KIND] = mutual_funds[CONST.PAYMENT].apply(lambda x : 1 if x >= 0 else -1)
    mutual_funds[CONST.BUY_SELL_UNIT] = mutual_funds[CONST.UNIT] * mutual_funds[CONST.BUY_SELL_KIND] 
    
    # SBI証券VTI投資信託データの加工
    sbi_mutual_funds = make_mutual_funds(mutual_funds,  \
                                         'ＳＢＩ・Ｖ・全米株式インデックス・ファンド', \
                                         'ＳＢＩ・Ｖ・全米株式インデックス・ファンド', \
                                         sell_funds)

    # 楽天証券VTI投資信託データの作成
    rakuten_mutual_funds = make_mutual_funds(mutual_funds, \
                                             '楽天・全米株式インデックス・ファンド（楽天・バンガード・ファンド（全米株式））/再投資型', \
                                             '楽天・全米株式インデックス・ファンド(楽天・VTI)', \
                                             sell_funds)
    # SBI証券VTI投資信託サマリーデータの作成
    sbi_summary_data, sbi_max_cumulative_payment = make_mutual_funds_summary_data(sbi_mutual_funds)

    # 楽天証券VTI投資信託サマリーデータの作成
    rakuten_summary_data, rakuten_max_cumulative_payment = make_mutual_funds_summary_data(rakuten_mutual_funds)
    
    # ページ設定
    set_config(im)
    st.markdown(CSS, unsafe_allow_html=True)
    st.markdown(HIDE_ST_STYLE, unsafe_allow_html=True)

    st.title('投資信託(VTI)')
    
    st.sidebar.title("メニュー")
    # サイドバーにアイテムを設置
    display_end_year:int = st.sidebar.selectbox('表示終了年', year_list, index=datetime.datetime.now().year - start_year)
    display_end_month:int = st.sidebar.selectbox('表示終了月', month_list, index=11)
    display_end_yearmon:str = str(display_end_year) + '-' + str(display_end_month).zfill(2) + '-01' 
    display_data_str:str = st.sidebar.selectbox('データを表示', ['する', 'しない'], index=0)      # カテゴリー：使用する
    display_data:bool = True if display_data_str == 'する' else False
    # y軸区切りは入金合計/4 最大値をグラフ間で合わせる
    target_y_max = max(rakuten_max_cumulative_payment, sbi_max_cumulative_payment)
    target_y_dtick = max(round(rakuten_max_cumulative_payment / 4, -3), round(sbi_max_cumulative_payment / 4, -3))

    # 画面配置
    rakuten_col, sbi_col = st.columns(2)
    with rakuten_col:

        #サマリーデータの表示
        st.write('楽天証券')
        st.dataframe(rakuten_summary_data, hide_index=True)

        # 楽天証券VTI投資信託グラフデータの作成
        rakuten_mutual_funds = make_mutual_funds_graph_data(rakuten_mutual_funds, daily_df, display_end_yearmon)

        fig = px.bar(rakuten_mutual_funds, x=CONST.YEARMON, y=CONST.CUMULATIVE_PAYMENT, range_y=[0, target_y_max], barmode='relative')
        fig.update_yaxes(tick0=0, dtick=target_y_dtick)
    
        # グラフの書式設定
        fig = graph_setting(fig, '楽天VTI取り崩し')
        st.plotly_chart(fig)
        if display_data:
            st.dataframe(rakuten_mutual_funds, hide_index=True)
    
    # SBI証券
    with sbi_col:
        # SBI証券VTI投資信託グラフデータの作成
        sbi_mutual_funds = make_mutual_funds_graph_data(sbi_mutual_funds, daily_df, display_end_yearmon)

        #サマリーデータの表示
        st.write('SBI証券')
        st.dataframe(sbi_summary_data, hide_index=True)

        # グラフの書式設定
        fig1 = px.bar(sbi_mutual_funds, x=CONST.YEARMON, y=CONST.CUMULATIVE_PAYMENT, range_y=[0, target_y_max], barmode='relative')
        fig1.update_yaxes(tick0=0, dtick=target_y_dtick)
        fig1 = graph_setting(fig1, 'SBIVTI取り崩し')
        st.plotly_chart(fig1)
        if display_data:
            st.dataframe(sbi_mutual_funds, hide_index=True)
else:
    st.write('not exists!!')