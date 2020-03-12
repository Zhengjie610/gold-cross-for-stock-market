from finance import testK as t


def setglobal(x,y,z):
    global stockdf
    stockdf=t.set_global_var(x,y,z)
    global cross_day_price
    cross_day_price=t.get_price_of_cross_day_()
    global index
    index=t.get_cross_day_index()


#print(index)
#print(cross_day_price)
#print(t.get_cross_day_index())
#print(len(cross_day_price),len(t.get_cross_day_index()))


def get_xdayLater_index(x):

    index=[ i-x for i in t.get_cross_day_index()]
    return index


#一个是获取交叉日X天后的开盘价，一个是收盘价，两个可以相等，但是收盘价必须等于或者晚于开盘价的日期
def get_OpenPrice_after_x_day(x):
    price=[]

    p=stockdf.iloc[get_xdayLater_index(x)]['open']
    for i in p:
        price.append(i)

    return price

def get_Close_price_afterx_xday(x):
    #x=x-1#第三天，而不是+3天
    Close=get_xdayLater_index(x)
    ClosePrice=[]
    Price=stockdf.iloc[get_xdayLater_index(x)]['close']
    for i in Price:
        ClosePrice.append(i)

    return ClosePrice

def get_date():
    day=stockdf.iloc[index]['trade_date']
    return day

def get_o_c_dic(fromday,today):
    open = get_OpenPrice_after_x_day(fromday)
    Close = get_Close_price_afterx_xday(today)
    Dictionary = dict(zip(open, Close))
    return Dictionary


def get_Prentage_of_two_Price(fromday,today):

    open=get_OpenPrice_after_x_day(fromday)
    Close=get_Close_price_afterx_xday(today)
    Dictionary=dict(zip(open,Close))
    prc=[]
    for buy,sell in Dictionary.items():
        prentage=round(sell/buy-1,2)
        prc.append(prentage)


    return prc
def poscount(x,y):

    count=0
    for i in get_Prentage_of_two_Price(x,y):
        if i>0:
            count=count+1
    return count



#print(get_OpenPrice_after_x_day(1),get_Close_price_afterx_xday(3))

def getsum(x,y):
    print(get_o_c_dic(x,y))
    print(get_Prentage_of_two_Price(x,y))

    print(len(get_Prentage_of_two_Price(x,y)))
    print(poscount(x,y))
    print('上涨比例： ',poscount(x,y)/len(get_Prentage_of_two_Price(x,y)))

#setglobal('000858.sz','20120101','20190411')
#getsum(1,2)
#print(stockdf)


from finance import sz50

for i,v in sz50.get_code_list().items():
    setglobal(i+'.sh','20120101','20190411')
    print('###############',v)
    getsum(1,5)




#print(get_date())

#def Buy_on_xDay_laterWithOpen_Price():
    ###


#print(x)


#print(stockdf)


#交叉点当日无法买入，交叉点第二天后买入第3天收盘卖出，如果交叉点是1月1日，最快1月2日开盘买入，1月3号卖出




