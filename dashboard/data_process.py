# -*- coding: utf-8 -*-
# データを加工数る関数を定義
import pandas as pd
import streamlit as st
import plotly.express as px
import json
from typing import Tuple
from consts import CONST

def get_excel_read_setting(json_path)-> list[str]:
    # JSONファイルを読み込む
    f = open(json_path, 'r', encoding='UTF-8')
    data = f.read()
    excel_read_setting = json.loads(data) 
    f.close()
    
    sheet_name_list:list = []
    usecols_list:list = []
    header_list:list = []
    for d in excel_read_setting["excel_read_setting"]:
        sheet_name_list.append(d["sheet_name"])
        usecols_list.append(d["usecols"])
        header_list.append(d["header"])
    
    return sheet_name_list, usecols_list, header_list

def set_config(im):
    
    st.set_page_config(
        page_title="家計簿アプリ",
        #page_icon="🧊",
        page_icon=im,
        layout="wide",
        initial_sidebar_state="expanded",
    )

_="""
プログレスバーに表示するメッセージを作成する
"""
def make_progress_message(progress_count, progress_number, tool_name, sheet_name) -> str:
    
    message = '処理済み ' + str(int((progress_count / progress_number) * 100)) + '% ' + tool_name + ' ' + sheet_name + 'シート取得完了'
    return message

_="""
プログレスバーの下に表示する完了メッセージを作成する
"""
def make_progress_complete_message(sheet_name) -> str:
    
    message = '*****' + sheet_name + 'シート取得完了 *****'
    return message

_="""
読み込むシート名を作成する
"""
def make_sheet_names(start_year, end_year) -> list[str]:
    sheet_names:list = []
    for i in range(start_year, end_year):
        sheet_names.append(str(i) + 'データ')
    
    return sheet_names

_="""
資産運用データをグラフ化するための時系列データフレームを作成して返す
"""
def make_df_for_asset(start_year, asset_end_year) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    
    daily_index = pd.date_range(start=str(start_year) + '-01-01', end=str(asset_end_year) + '-12-31', freq='D')

    # データの例（すべて0で初期化）
    data = [1] * len(daily_index)

    # データフレームを作成
    df = pd.DataFrame(data, index=daily_index, columns=['value'])

    df[CONST.YEAR] = df.index.map(lambda x : x.year).astype('int')
    df[CONST.YEARMON] = df.index.map(lambda x : str(x.year) + '-' + str(x.month)).astype('str')
    df[CONST.MONTH] = df.index.map(lambda x : x.month).astype('int')
    df[CONST.DAY] = df.index.map(lambda x : x.day).astype('int')
    df.reset_index(inplace= True)
    df = df.rename(columns={'index': CONST.DATE})
    
    year_df = df.drop_duplicates(subset=CONST.YEAR)
    yearmon_df = df.drop_duplicates(subset=CONST.YEARMON)

    return year_df, yearmon_df, df

_="""
対象年からシート名を作成する
"""
def make_sheet_name(target_year) -> str:
    sheet_name:str = str(target_year) + 'データ'
    
    return sheet_name

_="""
家計簿データの列から一意な値のリストを作成する
"""
def make_unique_value_list(df_dict, col_name) -> list[str]:
    tmp_list:list = []
    unique_value_list:list = []
    
    # 家計簿データのループ
    for key in df_dict:
        # unique()はユニークな要素の値の一覧をNumPy配列ndarrayで返す
        # ndarrayはtolist()メソッドでPythonの組み込み型のリストlistに変換できる
        tmp_list = df_dict[key][col_name].unique().tolist()
        
        # 家計簿データのカテゴリーを調べて一意な値なら追加する
        for value in tmp_list:
            if value not in unique_value_list:
                unique_value_list.append(value)
        
        unique_value_list.append('')

    return unique_value_list

_="""
欠損データを削除して、年・月・日列を追加する
"""
def add_YYYYMMDD_data(df, date_column_name) -> pd.DataFrame:
    df = df.dropna(subset=[date_column_name])
    df[CONST.YEAR] = df[date_column_name].apply(lambda x : x.year).astype('int')
    df[CONST.MONTH] = df[date_column_name].apply(lambda x : x.month).astype('int')
    df[CONST.DAY] = df[date_column_name].apply(lambda x : x.day).astype('int')
    df[CONST.DATE] = df[date_column_name].apply(lambda x : x.strftime("%Y-%m-%d"))
    
    return df

_="""
投資信託データを作成する
"""
def make_mutual_funds(mutual_funds, brand_name, brand, sell_funds) -> pd.DataFrame:
    # 楽天証券VTI投資信託データを抽出
    mutual_funds = mutual_funds.query('銘柄名 == "' + brand_name + '"')
    # 累積の口数を計算
    mutual_funds[CONST.CUMULATIVE_UNIT] = mutual_funds[CONST.BUY_SELL_UNIT].cumsum()
    # 累積の入金額を計算
    mutual_funds[CONST.CUMULATIVE_PAYMENT]= mutual_funds[CONST.PAYMENT].cumsum()
    # 売却履歴から楽天証券VTI投資信託データを抽出
    sell_funds = sell_funds.query('銘柄 == "' + brand + '"')
    # 不要な列を削除
    sell_funds = sell_funds.drop(["銘柄コード","数量","取引","受渡日","費用", "取得/新規年月日","取得/新規金額","費用+徴収額+地方税"], axis=1) 
    # データフレームをマージ（約定日で結合）
    mutual_funds = pd.merge(mutual_funds, sell_funds, left_on='国内約定日', right_on='約定日', how='left')

    return mutual_funds

_="""
投資信託サマリーデータを作成する グラフのY軸用に入金合計も返す
"""
def make_mutual_funds_summary_data(mutual_funds) -> pd.DataFrame:
    max_cumulative_payment =  mutual_funds[CONST.CUMULATIVE_PAYMENT].max()
    now_cumulative_payment =  mutual_funds.iloc[-1][CONST.CUMULATIVE_PAYMENT]
    profit_without_tax = mutual_funds['損益金額（税引後）'].sum(skipna=True)
    withdrawal_df = mutual_funds[[CONST.BUY_SELL_KIND, '受渡金額（ポイント含む）']]
    withdrawal_df = withdrawal_df[withdrawal_df['受渡金額（ポイント含む）']<0].sum()

    withdrawal = profit_without_tax - withdrawal_df.sum()

    summary_data = pd.DataFrame({'入金合計':['¥' +'{:,.0f}'.format(max_cumulative_payment)], \
                                 '入金残額':['¥' +'{:,.0f}'.format(now_cumulative_payment)], \
                                 '実現損益':['¥' +'{:,.0f}'.format(profit_without_tax)], \
                                 '出金合計':['¥' +'{:,.0f}'.format(withdrawal)]})

    return summary_data, max_cumulative_payment

_="""
VTI投資信託グラフ用データを作成する
"""
def make_mutual_funds_graph_data(mutual_funds, daily_df, display_end_yearmon) -> pd.DataFrame:
    mutual_funds = pd.merge(daily_df, mutual_funds,  left_on=CONST.DATE, right_on='国内約定日', how='left')
    # 累積列は集計しなおすためいったん削除する
    mutual_funds = mutual_funds.drop(CONST.CUMULATIVE_UNIT, axis=1)
    mutual_funds = mutual_funds.drop(CONST.CUMULATIVE_PAYMENT, axis=1)

    # 集計後に時系列の順が崩れるのでインデックスを作っておく
    mutual_funds[CONST.ROW_NUMBER] = mutual_funds['value'].cumsum()
    yearmon_sort_df = mutual_funds[[CONST.YEARMON, CONST.DATE, CONST.ROW_NUMBER]]
    mutual_funds = mutual_funds.drop(CONST.ROW_NUMBER, axis=1)
    yearmon_sort_df = yearmon_sort_df.drop_duplicates(subset=CONST.YEARMON)
    # 年月で集計
    mutual_funds = mutual_funds.groupby(CONST.YEARMON).sum(numeric_only=True)
    # ソート用データフレームとマージ
    mutual_funds = pd.merge(mutual_funds, yearmon_sort_df, on=CONST.YEARMON)
    # データのソート
    mutual_funds = mutual_funds.sort_values(CONST.ROW_NUMBER)
    mutual_funds = mutual_funds.drop(['value', CONST.YEAR, CONST.MONTH, CONST.DAY, CONST.ROW_NUMBER], axis=1)
    # 累積の口数を計算
    mutual_funds[CONST.CUMULATIVE_UNIT] = mutual_funds[CONST.BUY_SELL_UNIT].cumsum()
    # 累積の入金額を計算
    mutual_funds[CONST.CUMULATIVE_PAYMENT]= mutual_funds[CONST.PAYMENT].cumsum()
    mutual_funds = mutual_funds[mutual_funds[CONST.DATE] <= display_end_yearmon]
    mutual_funds[CONST.WITH_DRAWAL] = mutual_funds.apply(lambda row : -row[CONST.PAYMENT] + row['損益金額（税引後）'] if row[CONST.PAYMENT] < 0 else 0, axis=1)

    mutual_funds = mutual_funds.drop([CONST.PAYMENT_WITHOUT_POINT, \
                                      CONST.BUY_SELL_UNIT, CONST.DATE, \
                                      CONST.BUY_SELL_KIND,'損益金額'], axis=1) 
    
    mutual_funds = mutual_funds.rename(columns={CONST.PAYMENT: '受渡金額'})

    return mutual_funds

_="""
特定の時間粒度で集計して返す
指定された時間列以外は削除する
"""
def time_sum_budget_data(df, timecol, analyze_category: bool=False) -> pd.DataFrame:
    monthly_sum_df = df.copy()
    if analyze_category:
        monthly_sum_df = monthly_sum_df.groupby([timecol, CONST.CATEGORY]).sum(numeric_only=True)
    else:
        monthly_sum_df = monthly_sum_df.groupby(timecol).sum(numeric_only=True)

    if timecol == CONST.YEAR:
        monthly_sum_df = monthly_sum_df.drop(CONST.MONTH, axis=1)
        monthly_sum_df = monthly_sum_df.drop(CONST.DAY, axis=1)
    elif timecol == CONST.MONTH:
        monthly_sum_df = monthly_sum_df.drop(CONST.YEAR, axis=1)
        monthly_sum_df = monthly_sum_df.drop(CONST.DAY, axis=1)
    elif timecol == CONST.DAY:
        monthly_sum_df = monthly_sum_df.drop(CONST.YEAR, axis=1)
        monthly_sum_df = monthly_sum_df.drop(CONST.MONTH, axis=1)

    return monthly_sum_df

_="""
グラフ設定
"""
def graph_setting(fig, title_text): 

    #fig.update_xaxes(tick0=1, dtick=1)
    fig.update_yaxes(exponentformat='none', showline=True, linecolor='lightgrey', linewidth=2)
    fig.update_xaxes(showline=True, linecolor='lightgrey', linewidth=2)

    # ズームとパンの設定 x/y軸のテキスト色：白
    fig.update_layout(title_text=title_text, title_font_color='white', \
                      xaxis=dict(rangeslider=dict(visible=True), title=dict(font=dict(color='white')), tickfont=dict(color='white')), \
                      yaxis=dict(title=dict(font=dict(color='white')), tickfont=dict(color='white')), \
                      legend=dict(font=dict(color = 'white')), \
                      dragmode="pan", plot_bgcolor='black', \
                      paper_bgcolor='black') # dragmodeの選択肢:pan, select

    return fig


_="""
日本資産配当データに投資国、資産区分、銘柄コードの列を付与する
"""
def make_jpx_divide_df(master_df, jpx_divide_df):
    master_df = master_df.copy()
    jpx_divide_df = jpx_divide_df.copy()

    # 銘柄データの辞書を作る
    country_dict = dict(zip(master_df['銘柄名'], master_df['投資国']))
    asset_dict = dict(zip(master_df['銘柄名'], master_df['資産区分']))
    code_dict = dict(zip(master_df['銘柄名'], master_df['銘柄コード']))

    # 分類用の列を追加（存在しない銘柄名=配当所得税還付金として処理する）
    jpx_divide_df['銘柄コード'] = jpx_divide_df.apply(lambda row : code_dict.get(row['銘柄名'],"9999"), axis=1)
    jpx_divide_df['投資国'] = jpx_divide_df.apply(lambda row : country_dict.get(row['銘柄名'], "日本"), axis=1)
    jpx_divide_df['資産区分'] = jpx_divide_df.apply(lambda row : asset_dict.get(row['銘柄名'], "株式"), axis=1)

    return jpx_divide_df

_="""
JPX配当データから一意の列のリストを作成して返す
"""
def make_unique_data_list(jpx_divide_df, column_name) -> list[str]:
    jpx_divide_df = jpx_divide_df.copy()
    unique_data_list = jpx_divide_df[column_name].unique().tolist()

    return unique_data_list

_="""
日本資産配当から各年/投資国/資産区分のレコードを抽出して返す
"""
def make_jpx_year_divide_df(jpx_divide_df, start_year, end_year) -> pd.DataFrame:
    jpx_divide_df = jpx_divide_df.copy()
    #jpx_divide_df.to_csv('c:\\temp\\jpx_divide_df.csv')
    country_list = make_unique_data_list(jpx_divide_df, '投資国')
    asset_kind_list = make_unique_data_list(jpx_divide_df, '資産区分')
    jpx_year_divide_df ={}
    divide_sum = 0
    for country in country_list:
        for asset_kind in asset_kind_list:
            for year in range(start_year, end_year):
                jpx_year_divide_df[(year, country, asset_kind)] = get_totalling_df(jpx_divide_df, year=year, country=country, asset_kind=asset_kind)
                divide_sum = divide_sum + jpx_year_divide_df[(year, country, asset_kind)]['入金額'].sum(skipna=True)

    return jpx_year_divide_df

_="""
日本資産配当からサマリーデータを作成する
"""
def make_jpx_summary_data(jpx_year_divide_df) -> pd.DataFrame:
    df = pd.DataFrame(columns=['年', '投資国', '資産区分', '配当合計[￥]'])
    divide_sum = 0

    # キー単位で配当金を集計したデータフレームを作成する
    for key in jpx_year_divide_df:
        year = key[0]
        country = key[1]
        asset_kind = key[2]
        divide_sum = jpx_year_divide_df[key]['入金額'].sum(skipna=True)
        df.loc[len(df)] = [year, country, asset_kind, divide_sum]

    df['項目'] = df.apply(lambda row : row['投資国'] + row['資産区分'], axis=1)
    df = df.drop(['投資国', '資産区分'],axis=1)
    df = df[['年', '項目', '配当合計[￥]']]

    return df

_="""
日本資産配当サマリーデータから年データを抽出する
jpx_summary_data:'年', '項目', '配当合計[￥]'
"""
def extract_year_jpx_summary_data(jpx_summary_data, year) -> pd.DataFrame:

    df = jpx_summary_data.copy()
    df = df.query('年 == ' + str(year)) 
    df = df.drop('年', axis=1)
    # 配当金合計が0の項目を除く
    df = df[df['配当合計[￥]'] != 0]
    # 配当金のフォーマットを変更
    df['配当合計'] = df.apply(lambda row : '¥' +'{:,.0f}'.format(row['配当合計[￥]']), axis=1)
    return df

_="""
集計
"""
def get_totalling_df(df, year:int =0, country:str ='', asset_kind:str ='') -> pd.DataFrame:
    df = df.copy()
    if year > 0:
        #df = df.groupby('年')
        df = df.query('年 == ' + str(year)) 
    if country != '':
        #df = df.groupby('投資国')
        df = df.query('投資国 == "' + country + '"')
    if asset_kind != '':
        #df = df.groupby('資産区分')
        df = df.query('資産区分 == "' + asset_kind + '"')
    return df

_="""
円グラフ設定
"""
def pie_graph_setting(fig): 

    fig.update_traces(textfont_color="white")  # ラベル文字色
    fig.update_layout(paper_bgcolor="black",   # 外側の背景
                      plot_bgcolor="black",    # グラフ部分の背景
                      font_color="white",       # タイトルや凡例の文字色
                      title_font_color="white",   # タイトルの文字色
                      legend_font_color="white",   # 凡例の文字色
                      width=320,
                      height=320,
                      margin=dict(l=10, r=20, t=40, b=20))
    return fig
