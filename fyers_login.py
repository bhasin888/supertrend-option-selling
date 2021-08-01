from fyers_api import accessToken, fyersModel
import pandas as pd
import datetime
import os
import sys
import webbrowser
import math
import key

api_k=key.api_k
api_s=key.api_s
filename = str(datetime.datetime.now().date()) + ' token' + '.txt'

def read_access_token_from_file():
	file = open(filename, 'r+')
	auth_token = file.read()
	file.close()
	return auth_token

def send_access_token_to_file(auth_token):
	file = open(filename, 'w')
	file.write(auth_token)
	file.close()

def get_login(api_k=api_k, api_s=api_s):
	global fyers,auth_token
	app_session = accessToken.SessionModel(api_k, api_s)
	response = app_session.auth()
	print("Logging into Fyers")
	if response["code"] != 200:
		print('problem with auth token')
		print(response)
		sys.exit()

	if filename not in os.listdir():
		print("you haven't logged it for today")
		#print("[*] Generate Request Token : ", fyers.login_url())
		auth_code = response["data"]["authorization_code"]
		app_session.set_token(auth_code)
		generateTokenUrl = app_session.generate_token()
		webbrowser.open(generateTokenUrl,new=1)
		auth_token=input("enter auth token here : ")
		send_access_token_to_file(auth_token)
		fyers = fyersModel.FyersModel()
		send_access_token_to_file(auth_token)

	elif filename in os.listdir():
		auth_token = read_access_token_from_file()
		fyers = fyersModel.FyersModel()
		print("You have already loggged in for today")


	return fyers,auth_token


def round_down(x, a=0.05):
    return math.floor(x / a) * a

def round_up(x, a=0.05):
    return math.ceil(x / a) * a

def strike_round(x, base=100):
    return base * round(x/base)


def get_active_sells():
    active_positions_sell  = dict((pos["id"],pos["sellAvg"]) for pos in fyers.positions(token = auth_token)['data']['netPositions']
                if  (pos['netQty'] < 0 ))
    return active_positions_sell

def get_active_sells_symbol():
    active_positions_sell  = dict((pos["symbol"],pos["sellQty"]) for pos in fyers.positions(token = auth_token)['data']['netPositions']
                if  (pos['netQty'] < 0 ))
    return active_positions_sell


def get_active_buys():
    active_positions_buy  = dict((pos["id"],pos["buyAvg"]) for pos in fyers.positions(token = auth_token)['data']['netPositions']
                if  (pos['netQty'] > 0 ))
    return active_positions_buy


def get_pending_orders():
    pending_orders = [
                order["id"] for order in fyers.orders(token = auth_token)['data']['orderBook']
                if  (order['status'] == 6 or order['status'] == 4)
        ]
    return pending_orders
#1 => Canceled, 2 => Traded / Filled, 3 => (Not used currently), 4 => Transit, 5 => Rejected, 6 => Pending

def LOT_SIZE(und):
    if und=='NIFTY 50':
        lot = 75
    elif und=='NIFTY BANK':
        lot= 25
    else:
        lot=0
    return lot

"""
def cancel_all_orders():
    for order in pending_order:
        cancel_id = kite.cancel_order(variety=order['variety'],
            order_id=order['order_id'],
            parent_order_id=order['parent_order_id'])
        print(order['tradingsymbol'],order['variety'],'cancelled', cancel_id)

def sq_off_all_positions():
    for pos in active_positions:
        if pos['quantity']<0:
            kite.place_order(exchange=kite.EXCHANGE_NSE,
                    tradingsymbol=pos['tradingsymbol'],
                    transaction_type=kite.TRANSACTION_TYPE_BUY,
                    quantity=-1*pos['quantity'],
                    order_type = kite.ORDER_TYPE_MARKET,
                    variety = kite.VARIETY_REGULAR,
                    product = kite.PRODUCT_MIS)
        elif pos['quantity']>0:
            kite.place_order(exchange=kite.EXCHANGE_NSE,
                    tradingsymbol=pos['tradingsymbol'],
                    transaction_type=kite.TRANSACTION_TYPE_SELL,
                    quantity=pos['quantity'],
                    order_type = kite.ORDER_TYPE_MARKET,
                    variety = kite.VARIETY_REGULAR,
                    product = kite.PRODUCT_MIS)
        print('sq_off', pos['tradingsymbol'] ,pos['quantity'])



def cancel_n_sq_off(underlying):
    for order in pending_order:
        if order['tradingsymbol'] == underlying :
            cancel_id = kite.cancel_order(variety=order['variety'],
                order_id=order['order_id'],
                parent_order_id=order['parent_order_id'])
            print('cancelled', cancel_id)

    for pos in active_positions:
        if pos['tradingsymbol'] == underlying:
            if pos['quantity']<0:
                kite.place_order(exchange=kite.EXCHANGE_NSE,
                        tradingsymbol=underlying,
                        transaction_type=kite.TRANSACTION_TYPE_BUY,
                        quantity=-1*pos['quantity'],
                        order_type = kite.ORDER_TYPE_MARKET,
                        variety = kite.VARIETY_REGULAR,
                        product = kite.PRODUCT_MIS)
            elif pos['quantity']>0:
                kite.place_order(exchange=kite.EXCHANGE_NSE,
                        tradingsymbol=underlying,
                        transaction_type=kite.TRANSACTION_TYPE_SELL,
                        quantity=pos['quantity'],
                        order_type = kite.ORDER_TYPE_MARKET,
                        variety = kite.VARIETY_REGULAR,
                        product = kite.PRODUCT_MIS)
            print('sq_off', underlying ,pos['quantity'])




def snap_data():
    sd = [
        order for order in kite.orders()
        if order['status'] == 'COMPLETE' and order['tradingsymbol'] in WATCHLIST
    ]
    snap = pd.DataFrame(sd)
    snap.to_csv('summary/summary '+datetime.datetime.now().strftime("%Y-%m-%d %H:%M")+'.csv')


 """
get_login()
