from pyecharts import Kline
import tushare as ts
import pandas as pd
import numpy as np


def get_history_k(stokc_code,start_date,end_date):
    set_pd()
    token= "f6d71793866c5344bca04edc60e861fb0ccfa83d337e30357b171cb4"
    ts.set_token(token)
    pro = ts.pro_api()
    stock_data = pro.daily(ts_code=stokc_code, start_date=start_date, end_date=end_date)
    stock_data=stock_data.sort_values('trade_date', ascending=True)

    return stock_data

def set_pd():
    pd.set_option('display.max_columns', 10000000)
    pd.set_option('display.width', 10000000)
    pd.set_option('display.max_colwidth', 1000000)
    pd.set_option("display.max_rows",1000000)


def get_mean_list():
    ma_list = [5, 10, 20]
    return ma_list

def get_mean(day,id,dayfrom,dayto):
    close = get_history_k(id,dayfrom,dayto)['close']
    #for ma in get_mean_list():
    moving_avg = close.rolling(day).mean()
    #print(moving_avg)
    #print(close)
    return moving_avg


#get_mean(5)
#get_mean(3)
#
# def add_col():
#     #print(get_history_k('000858.SZ','20190301','20190402')['close'])
#     close=get_history_k('000858.SZ','20190301','20190402')['close']
#     #close=pd.concat([close, pd.DataFrame(columns=list('DE'))])
#
#     print(close)


def concat_ma10_ma5(three,five,ten,id,dayfrom,dayto):
    close=get_history_k(id,dayfrom,dayto)[['trade_date','open','close','change']]
    close = close.assign(M3=get_mean(three, id, dayfrom, dayto))
    close=close.assign(M5=get_mean(five,id,dayfrom,dayto))
    close = close.assign(M10=get_mean(ten,id,dayfrom,dayto))
    return close
    #print(close)

#'600519.sh','20020101','20190403'


def get_3_5_10(stock,dayfrom,to):
    return concat_ma10_ma5(3,5,10,stock,dayfrom,to).sort_values('trade_date',ascending=False)

#print(get_3_5_10())
def check_M5_over_thanM10(stock,dayfrom,to):
    df=get_3_5_10(stock,dayfrom,to).head(len(get_3_5_10(stock,dayfrom,to))-9)
    df['MA5>MA10']=np.where(df['M5']>df['M10'],'yes','no')
    return df

def set_global_var(stock,dayfrom,to):
    global stockdf
    stockdf=check_M5_over_thanM10(stock,dayfrom,to)
    return stockdf


#stock=set_global_var('600519.sh','20020101','20190403')

def get_stored_data():
    return stockdf


def compare():
    print(get_stored_data())
    lenth=len(get_stored_data()['MA5>MA10'])
    df=get_stored_data()['MA5>MA10']
    for i in range(0,lenth-1):
        if df[i]=='yes' and df[i+1]=='no':
            print('the gold cross on ',get_stored_data()['trade_date'][i+1])
        if df[i+1]=='yes' and df[i]=='no':
            print('the dead cross on',get_stored_data()['trade_date'][i+1])

def return_gold_index():
    #print(get_stored_data())
    lenth=len(get_stored_data()['MA5>MA10'])
    df=get_stored_data()['MA5>MA10']
    gold_list=[]
    for i in range(0,lenth-1):
        if df[i]=='yes' and df[i+1]=='no':
            gold_list.append(i+1)
    return gold_list

def get_price_of_cross_day_():
    index = get_cross_day_index()
    cross_day_price = []
    for i in get_stored_data().iloc[index]['close']:
        cross_day_price.append(i)
    return cross_day_price


def get_cross_day_index():
    index=index = [i - 1 for i in check_gold_cross_up()]
    return index





def return_dead_index():
    #print(get_stored_data())
    lenth = len(get_stored_data()['MA5>MA10'])
    df = get_stored_data()['MA5>MA10']
    dead_list=[]
    for i in range(0, lenth - 1):
        if df[i + 1] == 'yes' and df[i] == 'no':
            dead_list.append(i+1)
    return dead_list

def check_gold_cross_up():
    return return_gold_index()


#print(get_stored_data())

def get_day1_index():
    day1=[i-2 for i in check_gold_cross_up()]
    return day1

def get_day2_index():
    day2 = [i - 3 for i in check_gold_cross_up()]
    return day2

def get_dayx_index(x):
    dayx=[i - x for i in check_gold_cross_up()]
    return dayx


#获取黄金交叉后1天跌的计数
def get_ng_count_day1():
    day1_change=get_stored_data()[['trade_date','change']].iloc[get_day1_index()]
    array_of_ng_day1=day1_change['change'].values.flatten()
    print(array_of_ng_day1)
    count=sum(n < 0 for n in array_of_ng_day1)
    return count
#获取黄金交叉后2天跌的计数
def get_ng_count_day2():
    day1_change=get_stored_data()[['trade_date','change']].iloc[get_day2_index()]
    array_of_ng_day1=day1_change['change'].values.flatten()
    print(array_of_ng_day1)
    count=sum(n < 0 for n in array_of_ng_day1)
    return count

#获取黄金交叉后一天的价格
def prentage_of_ng_days():
    lenth=len(check_gold_cross_up())

    print(lenth)



#print(get_stored_data())

#获取黄金交叉前一天的价格
def price_of_day0():
    day0=[]
    for i in get_stored_data().iloc[return_gold_index()]['close']:
        day0.append(i)
    return day0
    #print(day0)

def get_day0_date():
    day0 = []
    for i in get_stored_data().iloc[return_gold_index()]['trade_date']:
        day0.append(i)
    return day0

def get_day1_price():
    day1 = []
    for i in get_stored_data().iloc[get_day1_index()]['close']:
        day1.append(i)
    return day1
#获取不通日期的价格指数
def get_day2_price():
    day2list=[]
    for i in get_stored_data().iloc[get_day2_index()]['close']:
        day2list.append(i)
    #print(day1_0list)
    return day2list


def get_dayx_price(day):
    day2list=[]
    for i in get_stored_data().iloc[get_dayx_index(day)]['close']:
        day2list.append(i)
    #print(day1_0list)
    return day2list

def get_dayx_data(day):
    datelist = []
    for i in get_stored_data().iloc[get_dayx_index(day)]['trade_date']:
        datelist.append(i)
    # print(day1_0list)
    return datelist



def get_day_x_price_list(day):
    #print('交叉当日价格',price_of_day0())
    #print('交叉当日日期',get_day0_date())
    #print('交叉当日日期+价格',dict(zip(get_day0_date(), price_of_day0())))
    print('')
    #print('------------------------------------')
    #print(get_day1_price())
    #print(get_day2_price())
    #print('------------------------')
    #print('第%s后天的日期+价格'%day,)
    #print('第%s后天的日期+价格'%day,dict(zip(get_dayx_data(day),get_dayx_price(day))))
    #print('交叉%s日后日日期'%day, get_dayx_data(day))



def compare_day0_da1():
    count=0
    period=len(price_of_day0())
    for (day0,day1) in zip(price_of_day0(),get_day1_price()):
        if day1>day0:
            count=count+1


    print(count/period)

def compare_day0_day2():
    count = 0
    period = len(price_of_day0())
    for (day0, day1) in zip(price_of_day0(), get_day2_price()):
        if day1 > day0:
            count = count + 1
    print(count / period)

def compare_day0_dax(day):
    count = 0
    period = len(price_of_day0())

    for (day0, day1) in zip(price_of_day0(), get_dayx_price(day)):
        if day1 > day0:
            count = count + 1
    #print('第%d天后还保持涨价的的交叉总计%s'%(day,count))
    print('黄金交叉后第%s日后和交叉时涨率'%day,count / period)


def summarise(id,fromday,today):

    set_global_var(id,fromday,today)

    print(len(price_of_day0()))
    print('从 '+fromday,'到 '+today,'证券代号 '+id,'总黄金交叉日计数 %s 次'%len(price_of_day0()))
    print('------------------------------------')
    print('统计MA5和MA10黄金交叉后涨价率')
    #print('-----------------')
    for i in range(1,5):
        get_day_x_price_list(i) #第0天交叉和第X天比较
        #print('-----------------')
        compare_day0_dax(i)
    print('-----------------')
#set_global_var('600519.sh','20110101','20190409')

#print('交叉当日价格',price_of_day0())
#print('交叉当日日期',get_day0_date())



#summarise('600519.sh','20030101','20190410')
#print('\033[31m这是前景色1')


#print(get_stored_data())
#print(get_stored_data().iloc[get_day2_index()]['close'])


#print(get_history_k('600519.sh','20190101','20190410')['close'])


#print(get_ge_count_day1(),get_ge_count_day2())
