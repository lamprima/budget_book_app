# -*- coding: utf-8 -*-
# データを加工数る関数を定義
import pandas as pd
from consts import CONST

_="""
読み込むシート名を作成する
"""
def make_sheet_names(start_year, end_year) -> list[str]:
    sheet_names:list = []
    for i in range(start_year, end_year):
        sheet_names.append(str(i) + 'データ')
    
    return sheet_names

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
def preprocess_budget_data(df) -> pd.DataFrame:
    df = df.dropna(subset=[CONST.DATE])
    df[CONST.YEAR] = df[CONST.DATE].apply(lambda x : x.year).astype('int')
    df[CONST.MONTH] = df[CONST.DATE].apply(lambda x : x.month).astype('int')
    df[CONST.DAY] = df[CONST.DATE].apply(lambda x : x.day).astype('int')
    df[CONST.DATE] = df[CONST.DATE].apply(lambda x : x.strftime("%Y-%m-%d"))
    df = df.iloc[:, [0,6,7,8,1,2,4,5,3]]
    return df

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


