import pandas as pd
import openpyxl

# 첫 번째 시트 가져오기
df = pd.read_excel('excel_s1.xlsx', sheet_name=0, engine='openpyxl')
# print(df)
# print(df.head()) # 상위 5개
# print(df.tail()) # 하위 5개

df = pd.read_excel('excel_s1.xlsx', sheet_name=0, skiprows=[1])
# print(df.head()) # 상위 5개

df = pd.read_excel('excel_s1.xlsx', sheet_name=0, skiprows=[1], skipfooter=5)
# print(df.tail())

df = pd.read_excel('excel_s1.xlsx', header=0)
# print(df.head())
# print(list(df)) # 헤더만 리스트로 출력
print(list(df.columns.values))

# 전처리
# ^Unnamed: Unnamed로 시작하는 열
df=df.loc[:, ~df.columns.str.contains('^Unnamed')]
# na_values = '... => null