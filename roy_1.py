import time
import json
import sys, getopt
import datetime
from botindicators import BotIndicators
from cfg import period, pair, lengthOfMA, strategy, market_fees, min_profit_margin, webserver, graphical

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.animation as animation
from matplotlib.dates import strpdate2num
import numpy as np
from coinbase.wallet.client import Client
import WebServer as WebServer

from secrets import api_key, api_secret

# TRADING BOT PYTHON 3 COMPLIANT AND OOB 
# coinbase client.py need a bugfix
# /usr/local/lib/python3.5/dist-packages/coinbase/wallet/client.py
'''
def get_spot_price(self, **params):
	"""https://developers.coinbase.com/api/v2#get-spot-price"""
	if 'currency_pair' in params:
		currency_pair = params['currency_pair']
	else:
		currency_pair = 'BTC-USD'
	response = self._get('v2', 'prices', currency_pair, 'spot', data=params)
	return self._make_api_object(response, APIObject)
'''

class RoyTrader():
	
	client = Client(api_key, api_secret)
	user = client.get_current_user()
	account = client.get_accounts()
	buys = []
	sells = []
	prices = []
	signals = []
	args = []
	fibo = BotIndicators()

	#print(account)
	
	print ('Trading As:         %s (%s)' % (user['name'], user['email']))
	#print ('Starting Balance:   $%s (%s BTC @ $%s/BTC)' % (balance['EUR'], balance['BTC'], get_price()))

	def __init__(self, api_key, api_secret):
		#coinbase
		#poloniex

		self.startTrading()

	def startTrading(self):
		#prices = []
		currentMovingAverage = 0;
		startTime = False
		endTime = False
		historicalData = False
		tradePlaced = False
		typeOfTrade = False
		dataDate = ""
		orderNumber = ""

		market_fees = 0.15          # coinbase per-transaction fee in dollars
		min_profit_margin = 2.0     # minimum price increase before we sell out
	
		MACD = 0


		if webserver:
			WebServer.init_Webserver()
			WebServer.start_Webserver()
		
		idloop = 0

		while True:
			try:
				if idloop < lengthOfMA:
					idloop = idloop + 1

				if strategy == "classic": 
					self.classic_strategy()
				elif strategy == "MACD":
					self.MACD_Strategy(idloop)
				time.sleep(int(period))

			except KeyboardInterrupt:
				print("Bye")
				if webserver:
					WebServer.stop_Webserver()
				sys.exit()

	def MACD_Strategy(self, idloop):
		vectorEMAS_AMAF_MACD = []
		MACD = 0
		MACD_point = 0

		RSI_point = 0

		lastprice = self.get_price(pair)
		buyprice = self.get_buy_price()
		sellprice = self.get_sell_price()

		currentMovingAverage = 0
		previousPrice = 0
		emaSlow = 0 
		emaFast = 0
		dataDate = datetime.datetime.now().strftime('%H:%M:%S')

		#RSI = self.fibo.rsiFunc(self.prices)
		if len(self.args)>1:
			currentMovingAverage = sum(self.prices) / float(len(self.prices))
		#elif len(self.args)>12: #emaFast condition

		#elif len(self.args)>14: #RSI condition

		appendLine = datetime.datetime.now(),lastprice,buyprice,sellprice,previousPrice, 2
		self.args.append(appendLine)
		self.prices.append(float(lastprice))

		if len(self.args) > 26: 
		
			vectorEMAS_AMAF_MACD = self.fibo.MACD(self.prices)

			emaSlow = vectorEMAS_AMAF_MACD[0]
		
			emaFast = vectorEMAS_AMAF_MACD[1]
		
			MACD = vectorEMAS_AMAF_MACD[2]

			MACD_point = MACD[0]
			
		RSI = self.fibo.rsiFunc(self.prices)	

		RSI_point = RSI[0] 

		print (idloop," Date: ",str(dataDate)," Period: ",str(period),"  coppia: ",str(pair)," Price: ",str(lastprice)," BUY: ", buyprice, "SELL: ", sellprice ," EMA: ",str(currentMovingAverage)," MACD: ",str(MACD_point), " RSI: ", RSI_point)

		if len(self.args) > 27:
			
			self.findSignals(self.args, RSI, MACD)

			if graphical:
				self.fibo.plot3(self.args, self.prices, self.signals,emaSlow, emaFast, MACD, RSI)

		if len(self.args) == lengthOfMA:
			self.prices.pop(0)
			self.args.pop(0)

		if len(self.signals) > 0: 
			#print("data first signal:", self.signals[0][0])
			#print("data first args:", self.args[0][0])
			if self.signals[0][0] < self.args[0][0]:
				self.signals.pop(0)
				print("************************** SIGNALS POPPED *******************************" )


	@property
	def get_account(self):
		return [acct for acct in self.client.get_accounts()['data'] if acct['balance']['currency'] == 'BTC'][0]

	@property
	def get_balance(self):
		return {
			account['balance']['currency']:        float(account['balance']['amount']),
			account['native_balance']['currency']: float(account['native_balance']['amount']),
		}

	def get_price(self,pair):
		return float(self.client.get_spot_price(currency_pairo =pair)['amount'])

	def get_price_LTC(self):
		print (self.client.get_spot_price(currency_pair =pair))

	def get_buy_price(self):
		return float(self.client.get_buy_price(currency_pair =pair)['amount'])

	def get_sell_price(self):
		return float(self.client.get_sell_price(currency_pair =pair)['amount'])

	def buy(self, amount):
		buy_obj = self.account.buy(amount, 'EUR')
		self.buys.append(buy_obj)

	def sell(self, amount):
		sell_obj = self.account.sell(amount, 'EUR')
		self.sells.append(sell_obj)

	def localbuy(self, amount, price):
		buy_obj = json.dumps({'date': str(datetime.datetime.now()),'amount': amount, 'price': price})
		self.buys.append(buy_obj)
		with open("www/report.csv", "a") as myfile:
			myfile.write("BUY," + str(datetime.datetime.now()) +","+str(amount)+","+str(price)+","+str(price*amount)+"\n")
			myfile.close()

	def localsell(self, amount, price):
		sell_obj = json.dumps({'date': str(datetime.datetime.now()), 'amount': amount, 'price': price})
		self.sells.append(sell_obj)
		with open("www/report.csv", "a") as myfile:
			myfile.write("SELL," + str(datetime.datetime.now()) +","+str(amount)+","+str(price)+","+str(price*amount)+"\n")
			myfile.close()

	def bytedate2num(self, fmt):
		def converter(b):
			return mdates.strpdate2num(fmt)(b.decode('ascii'))
		return converter
	
	def bytespdate2num(self, fmt, encoding='utf-8'):
		strconverter = mdates.strpdate2num(fmt)
		def bytesconverter(b):
			s = b.decode(encoding)
			return strconverter(s)
		return bytesconverter


	def findSignals(self, args, RSI, MACD):

		date = [x[0] for x in args] 
		prices = [x[1] for x in args] 
		buyprices = [x[2] for x in args]
		sellprices = [x[3] for x in args]
		
		lastprice = prices[-1]
		buyprice = buyprices[1]
		sellprice = sellprices[-1]

		if MACD[-1] > 0 and MACD[-2] < 0 and MACD[-3] < 0 and MACD[-4] < 0:
			self.signals.append([date[-1],float(lastprice),"buy", "MACD"])
			print(str(date[-1]) + " *** MACD *** BUY SIGNAL INTERCEPTED @ " + str(lastprice))

		if MACD[-1] < 0 and MACD[-2] > 0 and MACD[-3] > 0 and MACD[-4] > 0:
			self.signals.append([date[-1],float(lastprice),"sell", "MACD"])
			print(str(date[-1]) + " *** MACD *** SELL SIGNAL INTERCEPTED @ " + str(lastprice)) 


		if RSI[-1] < 20 and RSI[-2] > 20 and RSI[-3] > 20 and RSI[-4] > 20:
			self.signals.append([date[-1],float(lastprice),"buy", "RSI"])
			print(str(date[-1]) + " *** RSI *** BUY SIGNAL INTERCEPTED @ " + str(lastprice))
		elif RSI[-1] > 80 and RSI[-2] < 80 and RSI[-3] < 80 and RSI[-4] < 80:
			self.signals.append([date[-1],float(lastprice),"sell", "RSI"])
			print(str(date[-1]) + " *** RSI *** SELL SIGNAL INTERCEPTED @ " + str(lastprice))


		buycountsRSI = 0
		buycountsMACD = 0
		sellcountsRSI = 0
		sellcountsMACD = 0

		for idx, sign in enumerate(self.signals):
			
			if sign[2] == "buy":
				if sign[3] == "RSI":
					buycountsRSI = buycountsRSI + 1
				if sign[3] == "MACD":
					buycountsMACD == buycountsMACD + 1
			if sign[2] == "sell":
				if sign[3] == "RSI":
					buycountsRSI = sellcountsRSI + 1
				if sign[3] == "MACD":
					buycountsMACD == sellcountsMACD + 1

			if buycountsMACD + buycountsRSI ==2: 
				self.localbuy(2,buyprice)

			if sellcountsMACD + sellcountsRSI == 2 and gainCheck(sellprice):
				self.localsell(2,sellprice)

	def percent(self, part, whole):
		return 100 * float(part)/float(whole)

	def percentage(self, percent, whole):
		return (percent * whole) / 100.0

	def gainCheck(self, sellprice):

		for idx, buy in enumerate(self.buys):
			resp = json.loads(buy)
		
			if percent((float(sellprice)-(float(resp['price'])-float(market_fees)),buyprice)) > 0:
				print("GAIN %:", float(sellprice)-(float(buyprice)-float(market_fees)))
				return True
			else:
				return False

t = RoyTrader(api_key, api_secret)
