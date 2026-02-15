# -*- coding: utf-8 -*-
# 定数クラス

class CONST:
    YEAR = '年'
    YEARMON = '年月'
    MONTH = '月'
    DAY = '日'
    DATE = '日付'
    CATEGORY = 'カテゴリ'
    CATEGORY_DETAIL = 'カテゴリの内訳'
    INCOME = '収入'
    EXPENCE =  '支出'
    BUY_SELL_KIND = '売買区分'
    PAYMENT_WITHOUT_POINT = '受渡金額'
    PAYMENT = '受渡金額（ポイント含む）'
    UNIT = '口数'
    BUY_SELL_UNIT = '売買口数'
    CUMULATIVE_PAYMENT = '累積入金額'
    CUMULATIVE_UNIT = '累積口数'
    ROW_NUMBER = '行番号'
    WITH_DRAWAL = '出金'

class SESSION:
    IM = 'im'
    YEAR_DF = 'year_df'
    YEARMON_DF = 'yearmon_df'
    DAILY_DF = 'daily_df'
    START_YEAR = 'start_year'
    END_YEAR =  'end_year'
    ASSET_END_YEAR  = 'asset_end_year'
    ASSET_BOOK = 'asset_book'
    BUDGET_BOOK = 'budget_book'

class COUNTRY:
    JP = '日本'
    US = '米国'
    AU = 'オーストラリア'

class ASSET_KIND:
    STOCK = '株式'
    BOND = '債券'
    PRE_SEC = '優先証券'
    REIT = 'REIT'

class MUTUAL_FUND:
    CODE = '銘柄'
    SBI = 'ＳＢＩ・Ｖ・全米株式インデックス・ファンド'
    RAKUTEN = '楽天・全米株式インデックス・ファンド（楽天・バンガード・ファンド（全米株式））/再投資型'

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

CSS = f'''
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
