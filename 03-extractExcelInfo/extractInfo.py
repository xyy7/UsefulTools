from pprint import *

import pandas as pd

DEBUG = False

def save_demo(filename='output.xlsx'):
    names = ['a', 'b', 'c']
    scores = [99, 100, 55]
    result_excel = pd.DataFrame()
    result_excel["姓名"] = names
    result_excel["评分"] = scores
    # 写入excel
    result_excel.to_excel(filename)

def sort_demo(filename='output.xlsx'):
    names = ['ac','ab', 'aa','b', 'c']
    scores = [10, 60,60 ,100, 55]
    result_excel = pd.DataFrame()
    result_excel["姓名"] = names
    result_excel["评分"] = scores
    result_excel.sort_values(by=["评分","姓名"],inplace=True,ascending=True)
    result_excel.to_excel(filename)


def myRead(filename):
    sheet = pd.read_excel(filename)
    if DEBUG:
        print(sheet)
        # 打印每一行
        for val in sheet.values[:-2]:
            pprint(val)
        # 打印每一列
        for key in sheet.columns.values:
            pprint(sheet[key])
    pprint(sheet.columns.values)
    return sheet


def mySort(sheet,head=10):
    # 分组处理，然后合并
    grouped = sheet.groupby('科目名称',as_index=False)
    result_df = grouped.apply(lambda x: x.sort_values(by='项目支出', ascending=False).head(head))
    result_df.sort_values(by=["科目名称","凭证日期","项目支出"],inplace=True,ascending=True)
    if DEBUG:
        result_df.to_excel("sorted.xlsx")
    return result_df 


def mySave(sheet,filename):
    # 科目名称 => 支出类别
    # 凭证日期 => 付款凭证日期
    # 凭证编号 => 付款凭证编号
    # 项目支出 => 账面支出数、付款金额
    result_excel = pd.DataFrame()
    result_excel["凭证日期"] = sheet["凭证日期"]
    result_excel["凭证编号"] = sheet["凭证编号"]
    result_excel["摘要"] = sheet["摘要"]
    result_excel["支出类别"] = sheet["科目名称"]
    result_excel["主要成员"] = ['王旭'] * len(sheet["科目名称"])
    result_excel["审计认定数"] = [''] * len(sheet["科目名称"])
    result_excel["账面支出数"] = sheet["项目支出"]
    result_excel["付款凭证日期"] = sheet["凭证日期"]
    result_excel["付款凭证编号"] = sheet["凭证编号"]
    result_excel["付款金额"] = sheet["项目支出"]
    result_excel.to_excel(filename)
    return result_excel 


if __name__ == '__main__':
    DEBUG = True
    head = 100
    # save_demo()
    # sort_demo()

    sheet = myRead("F:\\szu18-onedrive\\OneDrive - email.szu.edu.cn\\学习笔记\\code\\UsefulTools\\03-extractExcelInfo\\(明细账)深科技创新（2020）230号_基2020N260三维全景视频感知与编码_all.xls")
    sheet = mySort(sheet,head)
    mySave(sheet,f"result_head{head}.xlsx")
