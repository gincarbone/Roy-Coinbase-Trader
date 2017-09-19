import time
import json
import sys, getopt
import datetime
from botindicators import BotIndicators
from cfg import period, pair, lengthOfMA, strategy, market_fees, min_profit_margin, webserver, graphical, buy_limit, buy_sell_amount, ignore_signals_after
from cfg import RSI_top_lim, RSI_down_lim

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
	#tbuys = client.get_buys()
	buys = []
	sells = []
	prices = []
	signals = []
	args = []
	transactions_plot = []
	fibo = BotIndicators()
	buy_count = 0

	#print(account)

	
	print ('Trading As:         %s (%s)' % (user['name'], user['email']))
	#print ('Starting Balance:   $%s (%s BTC @ $%s/BTC)' % (balance['EUR'], balance['BTC'], self.get_price()))
	print (account)
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

		#self.sync_buys_sells_operations()


		while True:
			try:
				if idloop < lengthOfMA:
					idloop = idloop + 1

				if strategy == "classic": 
					self.classic_strategy()
				elif strategy == "combined":
					self.MACD_RSI_Strategy(idloop)
				time.sleep(int(period))

			except KeyboardInterrupt:
				print("Bye")
				if webserver:
					WebServer.stop_Webserver()
				sys.exit()

	def MACD_RSI_Strategy(self, idloop):
		vectorEMAS_AMAF_MACD = []
		MACD = 0
		MACD_point = 0

		RSI_point = 0

		#lastprice = self.get_price(pair)
		lastprice = self.get_sell_price(pair) # use sell price instead of spot_price for more precise value
		buyprice = self.get_buy_price(pair)
		sellprice = self.get_sell_price(pair)

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

			MACD_point = MACD[-1]
			
		RSI = self.fibo.rsiFunc(self.prices)	

		RSI_point = RSI[-1] 

		print ("Date: ",str(dataDate),"  Pair: ",str(pair)," Price: ",str(lastprice)," BUY: ", buyprice, "SELL: ", sellprice ," EMA: ",str(currentMovingAverage)," MACD: ",str(MACD_point), " RSI: ", RSI_point)

		if len(self.args) > 27:
			
			transactions_plot = self.findSignals(self.args, RSI, MACD)

			if graphical:
				self.fibo.plot3(self.args, self.prices, self.signals,emaSlow, emaFast, MACD, RSI, transactions_plot)

		if len(self.args) == lengthOfMA:
			self.prices.pop(0)
			self.args.pop(0)

		#if len(self.signals) > int(ignore_signals_after): 
				#self.signals.pop(0)
				#print("************************** SIGNALS POPPED *******************************" )

		if len(self.signals) > 0 and len(self.args) > ignore_signals_after and self.signals[0][0] < self.args[-(ignore_signals_after)][0]: 
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

	@property
	def account(self):
		return [acct for acct in self.client.get_accounts()['data'] if acct['balance']['currency'] == 'BTC'][0]

	@property
	def balance(self):
		return {
			self.account['balance']['currency']:        float(self.account['balance']['amount']),
			self.account['native_balance']['currency']: float(self.account['native_balance']['amount']),
		}

	def get_price(self,pair):
		return float(self.client.get_spot_price(currency_pairo =pair)['amount'])

	def get_price_LTC(self):
		print (self.client.get_spot_price(currency_pair = pair))

	def get_buy_price(self, pair):
		return float(self.client.get_buy_price(currency_pair = pair)['amount'])

	def get_sell_price(self, pair):
		return float(self.client.get_sell_price(currency_pair = pair)['amount'])

	def buy(self, amount):
		buy_obj = self.account.buy(amount, 'EUR')
		self.buys.append(buy_obj)
		with open("transactions/BUY_Report", "a") as buyfile:
			buyfile.write(sell_obj+"\n")
			buyfile.close()		

	def sell(self, amount):
		sell_obj = self.account.sell(amount, 'EUR')
		self.sells.append(sell_obj)
		with open("transactions/SELL_Report", "a") as sellfile:
			sellfile.write(sell_obj+"\n")
			sellfile.close()


	def localbuy(self, date, amount, price):
		buy_obj = json.dumps({'date': date,'amount': amount, 'price': price})
		self.buys.append(buy_obj)
		self.transactions_plot.append([date, float(price), "BUY"]) 
		with open("www/report.csv", "a") as myfile:
			myfile.write("BUY,"+ date+","+str(amount)+","+str(price)+","+str(price*amount)+"\n")
			myfile.close()
		with open("www/index.html", "a") as htmlreport:
			htmlreport.write("<br> BUY Operation at: " + date +" <b>amount:</b> "+str(amount)+" <b> buy price:</b>"+str(price)+"  <b>total:</b> "+str(price*amount)+"\n")
			htmlreport.close()


	def localsell(self,date, amount, price):
		sell_obj = json.dumps({'date': date, 'amount': amount, 'price': price})
		self.sells.append(sell_obj)
		self.transactions_plot.append([date, float(price), "BUY"]) 
		with open("www/report.csv", "a") as myfile:
			myfile.write("SELL,"+ str(date)+","+str(amount)+","+str(price)+","+str(price*amount)+"\n")
			myfile.close()
		with open("www/index.html", "a") as htmlreport:
			htmlreport.write("<br> SELL Operation at: " + date +" <b>amount:</b> "+str(amount)+" <b> sell price:</b>"+str(price)+"  <b>total:</b> "+str(price*amount)+"\n")
			htmlreport.close()

	def sync_buys_sells_operations(self):
		json_buys = self.client.get_buys()
		print(json_buys)
		'''
		for idx, gdax_buy in enumerate(self.buys):
			resp = json.loads(buy)
			if percent((float(sellprice)-(float(resp['price'])-float(market_fees)),buyprice)) > 0:
				print("GAIN %:", float(sellprice)-(float(buyprice)-float(market_fees)))
				return True
			else:
				return False
		'''


	def get_buy_count(self):
		print("pre buy count")
		global buy_count
		buy_count = len(self.buys)
		print("after buy count")
		return buy_count

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

		dataDate = datetime.datetime.now().strftime('%H:%M:%S')
		
		lastprice = prices[-1]
		buyprice = buyprices[-1]
		sellprice = sellprices[-1]
		#TODO controllare i signals del periodo predecedente 
		#TODO vendere anche senza nessun signal se il prezzo raggiunge il target
		if MACD[-1] > 0 and MACD[-2] < 0 and MACD[-3] < 0:
			self.signals.append([date[-1],float(lastprice),"buy", "MACD"])
			print("Date: " + str(dataDate) + " *** MACD *** BUY SIGNAL INTERCEPTED @ " + str(buyprice))

		if MACD[-1] < 0 and MACD[-2] > 0 and MACD[-3] > 0:
			self.signals.append([date[-1],float(lastprice),"sell", "MACD"])
			print("Date: " + str(dataDate) + " *** MACD *** SELL SIGNAL INTERCEPTED @ " + str(sellprice)) 

		#if RSI[-1] < RSI_down_lim:
		if RSI[-1] < 50:
			self.signals.append([date[-1],float(lastprice),"buy", "RSI"])
			print("Date: " + str(dataDate) + " *** RSI *** BUY SIGNAL INTERCEPTED @ " + str(buyprice))
		#elif RSI[-1] > RSI_top_lim:
		elif RSI[-1] > 50:
			self.signals.append([date[-1],float(lastprice),"sell", "RSI"])
			print("Date: " + str(dataDate) + " *** RSI *** SELL SIGNAL INTERCEPTED @ " + str(sellprice))

		if len(self.signals) > 1:
			# if we have 2 according signals of buy 
			if self.signals[-1][2] == "buy" and self.signals[-2][2] == "buy":
				#and if the 2 signals according for MACD and RSI
				if self.signals [-1][3] == "RSI" and self.signals [-2][3] == "MACD":
					if len(self.buys) < buy_limit: 
						print("Executing BUY")
						self.localbuy(self.args[0][-1],buy_sell_amount,buyprice)
		
				elif self.signals [-1][3] == "MACD" and self.signals [-2][3] == "RSI":
					if len(self.buys) < buy_limit:
						print("Executing BUY")
						self.localbuy(self.args[0][-1],buy_sell_amount,buyprice)
				
				elif self.signals [-1][3] == "RSI" and self.signals [-2][3] == "RSI":
						self.signals.pop(-2)
			# if we have 2 according signals of sell 
			elif self.signals[-1][2] == "sell" and self.signals[-2][2] == "sell":
				#and if the 2 signals give the same result from MACD and RSI
				if self.signals [-1][3] == "RSI" and self.signals [-2][3] == "MACD":
					#check if we are rich :) 
					if self.gainCheck(sellprice):
						self.localsell(self.args[0][-1],buy_sell_amount,sellprice)
	
					else: 
						print("SELL double signal, BUT gain is not good")
				elif self.signals [-1][3] == "MACD" and self.signals [-2][3] == "RSI":
					#check if we are rich :) 
					if self.gainCheck(sellprice):
						self.localsell(self.args[0][-1],buy_sell_amount,sellprice)
	
				elif self.signals [-1][3] == "RSI" and self.signals [-2][3] == "RSI":
					self.signals.pop(-2)
			# only 1 signal but hard conditions 
			elif self.signals[-1][2] == "buy" and self.signals [-1][3] == "RSI" and (MACD[-1] > 0):
				if len(self.buys) < buy_limit: 
					self.localbuy(self.args[0][-1],buy_sell_amount,buyprice)

				else:
					print("Date: " + str(dataDate) + "BUY limit reached")
			else:
				print("Date: " + str(dataDate) + " BUY signal and SELL signal discording. HOLD POSITION... ")
		print(self.transactions_plot)
		return self.transactions_plot

	def percent(self, part, whole):
		return 100 * float(part)/float(whole)

	def percentage(self, percent, whole):
		return (percent * whole) / 100.0

	def gainCheck(self, sellprice):

		for idx, buy in enumerate(self.buys):
			resp = json.loads(buy)
			if self.percent((float(sellprice)-(float(resp['price'])-float(market_fees))-float(percentage(min_profit_margin,float(resp['price'])))),float(resp['price'])) > 0:
				return True
			else:
				Print ("SELL ABORTED: SellPrice:", float(sellprice), " BUY Price:", float(resp['price']), " Gain:", float(sellprice)-(float(resp['price'])-float(market_fees)-float(percentage(min_profit_margin,float(resp['price']))), "% Target: ", float(percentage(min_profit_margin,float(resp['price']))), "%" ))
				return False

t = RoyTrader(api_key, api_secret)
