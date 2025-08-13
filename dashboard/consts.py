# -*- coding: utf-8 -*-
# 定数クラス

class CONST:
    YEAR = '年'
    MONTH = '月'
    DAY = '日'
    DATE = '日付'
    CATEGORY = 'カテゴリ'
    CATEGORY_DETAIL = 'カテゴリの内訳'
    INCOME = '収入'
    EXPENCE =  '支出'

# 画面上部のスペースを消す設定
HIDE_ST_STYLE = """
                <style>
                body {
                    background-color: #2c3e50;
                    color: #ecf0f1;
                }
                #MainMenu {
                visibility: hidden;
                height: 0%;
                }
                header {
                visibility: hidden;
                height: 0%;
                }
                footer {
                visibility: hidden;
                height: 0%;
                }
				        .appview-container .main .block-container{
                            padding-top: 1rem;
                            padding-right: 3rem;
                            padding-left: 3rem;
                            padding-bottom: 1rem;
                        }  
                        .reportview-container {
                            padding-top: 0rem;
                            padding-right: 3rem;
                            padding-left: 3rem;
                            padding-bottom: 0rem;
                        }
                        header[data-testid="stHeader"] {
                            z-index: -1;
                        }
                        div[data-testid="stToolbar"] {
                        z-index: 100;
                        }
                        div[data-testid="stDecoration"] {
                        z-index: 100;
                        }
                </style>
"""
