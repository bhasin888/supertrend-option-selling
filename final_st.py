"""
Project: automated script for fyers suptrend option sell
Author: puneet bhasin
Version: 1.0.0
"""

# library
import time
import re
import math
from datetime import datetime, timedelta
#from tabulate import tabulate
from dateutil.relativedelta import relativedelta
import pandas as pd
import fyers_login
import indicators
from truedata import td_obj

################ take input #######################################
while True:
    try:
        HOLIDAYS = int(input('off days : '))
        break
    except:
        print("not valid...enter an integer value!")
while True:
    try:
        TRADE_0920 = int(input('enter 09:20 tarde : '))
        break
    except:
        print("not valid...enter 1 for YES 0 for NO")
while True:
    try:
        LOT_MULT = int(input('enter start lots : '))
        break
    except:
        print("not valid...enter integer value")


################## ENTER VALUES HERE ###########################################
TODAY=datetime.today()
LAST_THRS=indicators.LastThInMonth(TODAY.year,TODAY.month)
EXP=(TODAY + timedelta( (3-TODAY.weekday()) % 7 )).date()
if LAST_THRS==EXP:
    THRS=(TODAY + timedelta( (3-TODAY.weekday()) % 7 )).strftime('%y%b').upper()
else:
    THRS = str((TODAY + timedelta( (3-TODAY.weekday()) % 7 )).year -2000)+ \
            str((TODAY + timedelta( (3-TODAY.weekday()) % 7 )).month)+ \
            str((TODAY + timedelta( (3-TODAY.weekday()) % 7 )).day).zfill(2)

THRS_TD=(TODAY + timedelta( (3-TODAY.weekday()) % 7 )).strftime('%y%m%d')
if TODAY.weekday()==0:  #monday
    SL_MULT=0.5
    TGT=0.5
elif TODAY.weekday()==1: #tuesday
    SL_MULT=0.5
    TGT=0.6
elif TODAY.weekday()==2: # wednesday
    SL_MULT=0.5
    TGT=0.75
elif TODAY.weekday()==3: # thrsday
    SL_MULT=1
    TGT=0.95
elif TODAY.weekday()==4:    # friday
    SL_MULT=0.5
    TGT=0.4
else:
    SL_MULT=0
    TGT=0


EXIT_TIME = datetime.now().replace(hour=15, minute=0, second=0, microsecond=0)
ENTRY_TIME = datetime.now().replace(hour=9, minute=20, second=0, microsecond=0)
ENTRY_TIME2 = datetime.now().replace(hour=9, minute=25, second=0, microsecond=0)
DATA_DAYS=2+HOLIDAYS
# change both watchlists
#TEST_MARGIN=0
WATCHLIST= {'NIFTY BANK':TRADE_0920} #,'NIFTY 50':TRADE_0920
TRD_NAME = {'NIFTY 50':'NIFTY', 'NIFTY BANK':'BANKNIFTY'}
HEDGE={'NIFTY 50':1000, 'NIFTY BANK':2000}

#LOT_MULT=1
CANDLE_SIZE='5 mins'
C_ROUND=int(CANDLE_SIZE.split()[0])
#TRADE_0920 =  0
""" #####valid values candle size ###########
tick
1 min
2 mins
3 mins
5 mins
10 mins
15 mins
30 mins
60 mins
EOD

############ valid value duration ##############
D = Days
W = Weeks
M = Months
Y = Years
 """


PERIOD= 10
MULTIPLIER= 3


###################################################################################################

def data_downloader(script, interval=CANDLE_SIZE, delta=DATA_DAYS):
    """ downloads historic dta from truedata """
    data = td_obj.get_historic_data(script, start_time=datetime.now()-\
        relativedelta(days=delta),bar_size=interval)
    df = pd.DataFrame(data)
    return df

def slm_tgt_ord():
    """ placing SLM order """
    ord5=fyers.place_orders(
            token = auth_token,
            data = {
            "symbol" : "NSE:"+TRD_NAME[name]+THRS+str(st_strike)+PUTCALL,
            "qty" : QTY,
            "type" : 3, #2 means market order,3 slm
            "side" : 1, # 1 is buy -1 is sell
            "productType" : "INTRADAY",
            "limitPrice" : 0,
            "stopPrice" : math.ceil(td_obj.get_historic_data(TRD_NAME[name]+\
                THRS_TD+str(st_strike)+PUTCALL, duration='1 D',\
                    bar_size=CANDLE_SIZE)[-1]['c']*(1+SL_MULT)),
            "disclosedQty" : 0,
            "validity" : "DAY",
            "offlineOrder" : "False",
            "stopLoss" : 0,
            "takeProfit" : 0
            }
            )
    time.sleep(1)
    # target order
    ord6=fyers.place_orders(
            token = auth_token,
            data = {
            "symbol" : "NSE:"+TRD_NAME[name]+THRS+str(st_strike)+PUTCALL,
            "qty" : QTY,
            "type" : 3, #2 means market order,3 slm
            "side" : 1, # 1 is buy -1 is sell
            "productType" : "INTRADAY",
            "limitPrice" : math.ceil(td_obj.get_historic_data(TRD_NAME[name]+THRS_TD+str(st_strike)\
                +PUTCALL, duration='1 D',bar_size=CANDLE_SIZE)[-1]['c']*(1-TGT)),
            "stopPrice" : 0,
            "disclosedQty" : 0,
            "validity" : "DAY",
            "offlineOrder" : "False",
            "stopLoss" : 0,
            "takeProfit" : 0
            }
            )
    print(ord5)
    print(ord6)
    time.sleep(1)

def enter_trade():
    """ enter trades leverage and sell """
    ord1=fyers.place_orders(
                        token = auth_token,
                        data = {
                        "symbol" : "NSE:"+TRD_NAME[name]+THRS+str(st_strike+\
                            (PE_MULT*HEDGE[name]))+PUTCALL,
                        "qty" : QTY,
                        "type" : 2, #2 means market order
                        "side" : 1, # 1 is buy -1 is sell
                        "productType" : "INTRADAY",
                        "limitPrice" : 0,
                        "stopPrice" : 0,
                        "disclosedQty" : 0,
                        "validity" : "DAY",
                        "offlineOrder" : "False",
                        "stopLoss" : 0,
                        "takeProfit" : 0
                        }
                        )
    print(ord1)
    time.sleep(1)

    ord2=fyers.place_orders(
                        token = auth_token,
                        data = {
                        "symbol" : "NSE:"+TRD_NAME[name]+THRS+str(st_strike)+PUTCALL,
                        "qty" : QTY,
                        "type" : 2, #2 means market order
                        "side" : -1, # 1 is buy -1 is sell #### -1 here
                        "productType" : "INTRADAY",
                        "limitPrice" : 0,
                        "stopPrice" : 0,
                        "disclosedQty" : 0,
                        "validity" : "DAY",
                        "offlineOrder" : "False",
                        "stopLoss" : 0,
                        "takeProfit" : 0
                        }
                        )
    print(ord2)
    time.sleep(1)

fyers=fyers_login.fyers
auth_token=fyers_login.auth_token
login_info=fyers.get_profile(token=auth_token)
print('*****************************************************************************************')
print('logged in for user id :'+login_info['data']['result']['user_id'] +' - '+\
    login_info['data']['result']['name'])
print('****************************************************************************************' )

avail_bal=list(t['equityAmount'] for t in fyers.funds(auth_token)['data']['fund_limit'] \
    if t['title']=='Available Balance')[0]
print('available balance = '+str(avail_bal))

print("check time entry")
while datetime.now()<EXIT_TIME:
    print("exec_time : "+str(datetime.now()))
    if LOT_MULT<=3:
        print("check lot_mult :"+str(LOT_MULT))
        try:
            #print (tabulate(pd.json_normalize(pending_order)[['symbol','qty']],
            #  tablefmt='psql', showindex=False)) """
            #print("working")
            #entry conditions start
            for name in WATCHLIST:
                #FETCH DATA
                df = data_downloader(name)
                st = indicators.SuperTrend(df = df, period = PERIOD, multiplier = MULTIPLIER, \
                    ohlc=['o', 'h', 'l', 'c'])
                st_val_prev = round(st.iloc[-2]['ST_'+str(PERIOD)+'_'+str(MULTIPLIER)], 1)
                st_dirn_last = st.iloc[-1]['STX_'+str(PERIOD)+'_'+str(MULTIPLIER)]
                st_dirn_prev = st.iloc[-2]['STX_'+str(PERIOD)+'_'+str(MULTIPLIER)]
                st_dirn_prev2 = st.iloc[-3]['STX_'+str(PERIOD)+'_'+str(MULTIPLIER)]
                PUTCALL = 'PE' if st_dirn_prev == 'up' else 'CE'
                PE_MULT = -1 if st_dirn_prev == 'up' else 1
                st_strike=fyers_login.strike_round(st_val_prev)
                l_time=st.iloc[-1]['time']
                currtime=(datetime.now().replace(microsecond=0, second=0))
                currtime_5=datetime.now().replace(microsecond=0, second=0, \
                    minute=fyers_login.round_down(currtime.minute,a=C_ROUND))
                print(currtime)
                print(df[-4:])

                # CHECK 0920 CONDITION
                print("check 0920")
                if WATCHLIST[name]== 1 and datetime.now() > ENTRY_TIME:
                    print("0920 condition met")
                    print("enter : "+"NSE:"+TRD_NAME[name]+THRS+str(st_strike)+PUTCALL)
                    print("leverage : " +"NSE:"+TRD_NAME[name]+THRS+\
                        str(st_strike+(PE_MULT*HEDGE[name]))+PUTCALL)

                    #enter trade
                    QTY= (fyers_login.LOT_SIZE(name)*LOT_MULT)
                    print('QTY '+str(QTY))
                    #LEVERAGE ORDER AND SELL ORDER
                    enter_trade()
                    # SET 0920 TRADE TO "no"
                    WATCHLIST[name]=0
                    #SLM AND TARGET ORDER BASED ON LAST CANDLE'S CLOSE
                    slm_tgt_ord()
                    # INCREASE LOT SIZE FOR NEXT TRADE
                    LOT_MULT+=1

                #CHECK FOR SUPERTREND CHNAGE
                print("check st change for entry")
                if currtime_5>l_time:
                    if st_dirn_last != st_dirn_prev and datetime.now() > ENTRY_TIME2:
                        print(name +' : super trend direction changed')
                        print(name +'enter new position')
                        print("enter : "+"NSE:"+TRD_NAME[name]+THRS+str(st_strike)+PUTCALL)
                        print("leverage : " +"NSE:"+TRD_NAME[name]+THRS+\
                            str(st_strike+(PE_MULT*HEDGE[name]))+PUTCALL)
                        #enter trade
                        QTY= (fyers_login.LOT_SIZE(name)*LOT_MULT)
                        print('QTY '+str(QTY))
                        #LEVERAGE ORDER AND SELL ORDER
                        if ("NSE:"+TRD_NAME[name]+THRS+str(st_strike)+PUTCALL \
                            not in fyers_login.get_active_sells_symbol()
                        #or fyers_login.get_active_sells_symbol()["NSE:"+TRD_NAME[name]+\
                        # THRS+str(st_strike)+PUTCALL]<(fyers_login.LOT_SIZE(name)*4)
                        ):
                            enter_trade()
                            #SLM AND TARGET ORDER BASED ON LAST CANDLE'S CLOSE
                            slm_tgt_ord()
                            # INCREASE LOT SIZE FOR NEXT TRADE
                            LOT_MULT+=1
            #entry conditions end
        except  Exception as e:
            print(f'error message 2 {e}')
    else:
        print("lots exceeded 3")
    active_positions_sell=fyers_login.get_active_sells()
    print(active_positions_sell)
    #print (tabulate(pd.json_normalize(pending_order)[['symbol','qty']],\
    #  tablefmt='psql', showindex=False)) """
    try:
        for id in active_positions_sell:
            df = data_downloader((id[:id.rindex('-')][4:re.search(r"\d", id).start()]+\
                THRS_TD+id[:id.rindex('-')][-7:]))
            st = indicators.SuperTrend(df = df, period = PERIOD, multiplier = MULTIPLIER,\
                    ohlc=['o', 'h', 'l', 'c'])
            st_dirn_last = st.iloc[-1]['STX_'+str(PERIOD)+'_'+str(MULTIPLIER)]
            st_dirn_prev = st.iloc[-2]['STX_'+str(PERIOD)+'_'+str(MULTIPLIER)]
            st_dirn_prev2 = st.iloc[-3]['STX_'+str(PERIOD)+'_'+str(MULTIPLIER)]
            l_time=st.iloc[-1]['time']
            currtime=(datetime.now().replace(microsecond=0, second=0))
            currtime_5=datetime.now().replace(microsecond=0, second=0, \
                minute=fyers_login.round_down(currtime.minute,C_ROUND))
            print(df[-4:])
            print("check st change for exit")
            if currtime_5>l_time:
                if st_dirn_prev != st_dirn_last and datetime.now() > ENTRY_TIME2:
                    print("exit condition met")
                    exit_1=fyers.exit_positions(
                        token = auth_token,
                        data = {
                        "id" : id
                        }
                        )
                    print(exit_1)

                    active_order  = dict((pos["id"],pos["status"]) \
                        for pos in fyers.orders(token = auth_token)['data']['orderBook']
                                    if(pos['symbol'] == id[:id.rindex('-')] and pos['status']==6 ))
                    print("active_order for cancel")
                    print(active_order)
                    for id in active_order:
                        fyers.exit_positions(token = auth_token,
                            data = {
                            "id" : id
                                }
                            )


    except  Exception as e:
        print(f'error message 2 {e}')


print('Time to exit')

active_positions_sell=fyers_login.get_active_sells()
active_positions_buy=fyers_login.get_active_buys()
#exit previous positions:
for id in active_positions_sell:
    fyers.exit_positions(token = auth_token,
        data = {
        "id" : id
            }
        )
time.sleep(1)

for id in active_positions_buy:
    fyers.exit_positions(token = auth_token,
        data = {
        "id" : id
            }
        )
print("Done of the Day "+ str(TODAY))
