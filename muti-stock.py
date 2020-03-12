#from finance import sz50
from finance import testK as t
import tushare as ts
import pandas as pd

#
# sz50=sz50.get_code_list()
#
# for code,name in sz50.items():
#
#     print('##################分割符##########################')
#     print('')
#     print(str(code)+'.sh',name)

    #t.summarise(str(code)+'.sh','20190109','20190411')



stockdf=t.set_global_var('000858.sz','20190109','20190411')


# index=t.return_gold_index()
# day0=t.price_of_day0()
# dayx=t.get_dayx_price(3)
# print(day0,dayx)
# print(index)
# print(stockdf)
