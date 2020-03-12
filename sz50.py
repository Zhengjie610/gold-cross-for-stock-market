import baostock as bs
import pandas as pd

    # 登陆系统
def get_code_list():

    lg = bs.login()

    # 获取上证50成分股
    rs = bs.query_sz50_stocks()
    # 打印结果集
    sz50_stocks = []
    while (rs.error_code == '0') & rs.next():
        # 获取一条记录，将记录合并在一起
        sz50_stocks.append(rs.get_row_data())
    result = pd.DataFrame(sz50_stocks, columns=rs.fields)
    # 结果集输出到csv文件
    result.to_csv("D:/sz50_stocks.csv", encoding="GB2312", index=False)
    code=result['code']
    name=result['code_name']

    #print(code)
    code_list=[]
    for i in code:
        code_list.append(i.split('sh.')[1])
    #print(code_list)
    name_list=[]

    for i in name:
        name_list.append(i)

    bs.logout()
    return dict(zip(code_list,name_list))

print(get_code_list())