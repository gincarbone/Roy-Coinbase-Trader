import numpy 
import os, re, sys, time, datetime, copy, shutil
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.animation as animation
from matplotlib.dates import DayLocator, HourLocator, MinuteLocator, DateFormatter, drange
import matplotlib.gridspec as gridspec
from cfg import period, pair, lengthOfMA, graphical
import matplotlib.ticker as mticker
import matplotlib
import pylab
import pandas as pd 
from datetime import datetime as dt

#matplotlib.rcParams.update({'font.size': 9})



#import trading-bot-coinbase as trading-bot-coinbase


class BotIndicators(object):
	fig = plt.figure()

	if graphical:
		fig.set_size_inches(10, 7)

		ax1 = plt.subplot2grid((6,1), (0,0), rowspan=1, colspan=1)	#MACD
		ax = plt.subplot2grid((6,1), (1,0), rowspan=4, colspan=1) 	#prices
		ax2 = plt.subplot2grid((6,1), (5,0), rowspan=1, colspan=1)	#RSI

		fig.subplots_adjust(hspace=0)
		plt.setp([a.get_xticklabels() for a in fig.axes[:-1]], visible=False)

		#grids prices
		ax.grid(True, linestyle=':', linewidth='0.5', color='black')
		ax.xaxis.set_major_locator(mticker.MaxNLocator(lengthOfMA))
		ax.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))
		ax.yaxis.label.set_color("g")
		ax.spines['bottom'].set_color("#000000")
		ax.spines['top'].set_color("#000000")
		ax.spines['left'].set_color("#000000")
		ax.spines['right'].set_color("#000000")
		ax.tick_params(axis='y', colors='k')
		ax.set_ylabel('Price')

		#grids MACD
		ax1.grid(True, linestyle=':', linewidth='0.5', color='black')
		ax1.xaxis.set_major_locator(mticker.MaxNLocator(lengthOfMA))
		ax1.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))
		ax1.yaxis.label.set_color("g")
		ax1.spines['bottom'].set_color("#000000")
		ax1.spines['top'].set_color("#000000")
		ax1.spines['left'].set_color("#000000")
		ax1.spines['right'].set_color("#000000")
		ax1.tick_params(axis='y', colors='k')
		ax1.set_ylabel('MACD')

		#grids RSI
		ax2.grid(True, linestyle=':', linewidth='0.5', color='black')
		ax2.xaxis.set_major_locator(mticker.MaxNLocator(lengthOfMA))
		ax2.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))
		ax2.yaxis.label.set_color("k")
		ax2.spines['bottom'].set_color("#000000")
		ax2.spines['top'].set_color("#000000")
		ax2.spines['left'].set_color("#000000")
		ax2.spines['right'].set_color("#000000")
		ax2.tick_params(axis='y', colors='k')
		ax2.set_ylabel('RSI')


	def __init__(self):
		signals = []
		pass
		

	def movingAverage(self, dataPoints, period):
		if (len(dataPoints) > 1):
			return sum(dataPoints[-period:]) / float(len(dataPoints[-period:]))

	def momentum (self, dataPoints, period=14):
		if (len(dataPoints) > period -1):
			return dataPoints[-1] * 100 / dataPoints[-period]

	def EMA(self, prices, period):
		x = numpy.asarray(prices)
		weights = None
		weights = numpy.exp(numpy.linspace(-1., 0., period))
		weights /= weights.sum()

		a = numpy.convolve(x, weights, mode='full')[:len(x)]
		a[:period] = a[period]
		return a

	def MACD(self, prices, nslow=26, nfast=12):

		emaslow = self.EMA(prices, nslow)
		emafast = self.EMA(prices, nfast)
		return emaslow, emafast, emafast - emaslow

	def MACD_advanced(self, prices, nslow=26, nfast=12):

		emaslow = self.EWMA(prices, nslow)
		emafast = self.EWMA(prices, nfast)
		return emaslow, emafast, emafast - emaslow


	def RSI (self, prices, period=14):
		deltas = numpy.diff(prices)
		seed = deltas[:period+1]
		up = seed[seed >= 0].sum()/period
		down = -seed[seed < 0].sum()/period
		rs = up/down
		rsi = numpy.zeros_like(prices)
		rsi[:period] = 100. - 100./(1. + rs)

		for i in range(period, len(prices)):
			delta = deltas[i - 1]  # cause the diff is 1 shorter
			if delta > 0:
				upval = delta
				downval = 0.
			else:
				upval = 0.
				downval = -delta

			up = (up*(period - 1) + upval)/period
			down = (down*(period - 1) + downval)/period
			rs = up/down
			rsi[i] = 100. - 100./(1. + rs)
		if len(prices) > period:
			return rsi
		else:
			return 50 # output a neutral amount until enough prices in list to calculate RSI

	
	def rsiFunc(self, prices, n=14):
		deltas = numpy.diff(prices)
		seed = deltas[:n+1]
		up = seed[seed>=0].sum()/n
		down = -seed[seed<0].sum()/n
		rs = up/down
		rsi = numpy.zeros_like(prices)
		rsi[:n] = 100. - 100./(1.+rs)

		for i in range(n, len(prices)):
			delta = deltas[i-1] # cause the diff is 1 shorter

			if delta>0:
				upval = delta
				downval = 0.
			else:
				upval = 0.
				downval = -delta

			up = (up*(n-1) + upval)/n
			down = (down*(n-1) + downval)/n

			rs = up/down
			rsi[i] = 100. - 100./(1.+rs)

		return rsi


	def plot(self, prices, emaSlow, emaFast):
		
		#z = [1.1, 1.2, 1.3]

		#times = pd.date_range('2015-10-06', periods=500, freq='5sec')
		try:
			os.remove("operate.png")
		except OSError:
			pass

		plt.xlabel("Data Time")
		plt.ylabel("Values")
		plt.title("A test graph")

		#plt.ion()
		#plt.clear()

		plt.figure(1)
		plt.subplot(211)
		plt.plot(prices)

		plt.subplot(212)
		plt.plot(emaSlow, 'b--')

		#plt.annotate('local max', xy=(2, 1), xytext=(3, 1.5),arrowprops=dict(facecolor='black', shrink=0.05),)

		plt.subplot(212)
		plt.plot(emaFast, 'r--')

		plt.xlabel("Data Time")
		plt.ylabel("Values")
		plt.title("A test graph")
		#plt.savefig("operate.png")
		plt.draw()
		plt.show()


	def plot2(self, prices, signals, emaSlow, emaFast, RSI):
		
		# PRICES
		self.ax.clear()
		self.ax.grid(True)
		self.ax.plot(prices)
		
		#if interpolation == "yes":
		#	x_smooth = np.linspace(prices.min(), prices.max(), 200)
		#	y_smooth = spline(prices, prices, x_smooth)


		#EMASLOW EMAFAST
		self.ax1.clear()
		self.ax1.grid(True)
		self.ax1.plot(emaSlow, 'r--')
		self.ax1.plot(emaFast, 'b-')
		

		# PLOT RSI
		#self.ax2.clear()
		self.ax2.plot((RSI), 'g--')
		
		for idx, a in enumerate (signals):
			if not a[3]:
				self.ax.annotate(a[2],
							xy=(idx, a[1]), xycoords='data',
							xytext=(-60, 30), textcoords='offset points',
							bbox=dict(boxstyle="round", fc="0.8"),
							arrowprops=dict(arrowstyle="->",facecolor='red',
											connectionstyle="angle,angleA=0,angleB=90,rad=10"))
			

		plt.draw()

		#plt.show()
		plt.savefig("www/operatorio.png")


	def plot3(self, stock, prices, signals, emaslow, emafast, MACD, RSI):
		

		
		date = [x[0] for x in stock] #converters={ 0: mdates.strpdate2num('%Y%m%d')} 
		closep = [x[1] for x in stock] #lastprice
		highp = [x[2] for x in stock]
		lowp = [x[3] for x in stock]
		openp = [x[5] for x in stock] #previousPric
		sellprice = [x[3] for x in stock]
		volume = [x[5] for x in stock] 
		
		
		#print("RSI ùùùùùùùùùùùùùùùùùùùùùùùù ", RSI)
		#print("MACD ùùùùùùùùùùùùùùùùùùùùùùùù ", MACD)
		#print("emaslow ùùùùùùùùùùùùùùùùùùùùùùùù ", emaslow)
		#print("prices ùùùùùùùùùùùùùùùùùùùùùùùù ", closep)

		#print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAMACD",len(MACD))


		#datetime.datetime.now(),lastprice,buyprice,sellprice,previousPrice,volume k=2,emaSlow, emaFast, MACD, RSI 
		try:
			# PRICES
			self.ax.clear()

			self.ax.grid(which='major', linestyle=':', linewidth='0.65', color='black')
			self.ax.grid(which='minor', linestyle=':', linewidth='0.5', color='black')
			xs = matplotlib.dates.date2num(date)
			hfmt = matplotlib.dates.DateFormatter('%H:%M:%S')
			self.ax.xaxis.set_major_formatter(hfmt)
			self.ax.plot(xs, closep, linewidth=1.5)

			#EMASLOW EMAFAST
			self.ax1.clear()
			self.ax1.grid(which='major', linestyle=':', linewidth='0.65', color='black')
			self.ax1.grid(which='minor', linestyle=':', linewidth='0.5', color='black')
			self.ax1.xaxis.set_major_formatter(hfmt)
			self.ax1.relim()
			self.ax1.autoscale_view(True,True,True)
			#print("EmaSlow:", emaslow)
			#print("EmaFast:", emafast)

			self.ax1.plot(xs,emaslow, 'r-', linewidth=1.4)
			self.ax1.plot(xs,emafast, 'g-', linewidth=1.4)
			#plt.ylabel('MACD')
			self.ax1.set_ylabel('MACD')

			# PLOT RSI
			self.ax2.clear()
			self.ax2.grid(which='major', linestyle=':', linewidth='0.65', color='black')
			self.ax2.grid(which='minor', linestyle=':', linewidth='0.5', color='black')
			rsiCol = '#c1f9f7'
			posCol = '#386d13'
			negCol = '#8f2020'
			self.ax2.axhline(80, color=negCol, linewidth=1.0, linestyle='--')
			self.ax2.axhline(20, color=posCol, linewidth=1.0, linestyle='--')
			self.ax2.set_yticks([20,80])
			#set min and max for function RSI
			self.ax2.set_ylim([0,100])
			self.ax2.xaxis.set_major_formatter(hfmt)

			#xs = matplotlib.dates.date2num(date)
			self.ax2.plot(xs,RSI, 'c-', linewidth=1.6, color='green')
			self.ax2.fill_between(xs, RSI, 80, where=(RSI>=80), facecolor=negCol, edgecolor=negCol, alpha=0.5, interpolate=True)
			self.ax2.fill_between(xs, RSI, 20, where=(RSI<=20), facecolor=posCol, edgecolor=posCol, alpha=0.5, interpolate=True)

			# RSI Label on the chart
			self.ax2.set_ylabel('RSI')
			#fill between max value and thresold
			#self.ax2.fill_between(RSI, 80, where=(RSI>=80), facecolor=negCol, edgecolor=negCol, alpha=0.5)
			#self.ax2.fill_between(RSI, 20, where=(RSI<=20), facecolor=posCol, edgecolor=posCol, alpha=0.5)
			
			for idx, a in enumerate (signals):
				xss = matplotlib.dates.date2num(a[0])
				#l = plt.axvline(x=xss, label='BUY!')
				#ax.axvline(x=xss, label='BUY!', linewidth=2.0, linestyle='--', color='red')
				#ax1.axvline(x=xss, label='BUY!', linewidth=2.0, linestyle='--', color='red')
				#ax2.axvline(x=xss, label='BUY!', linewidth=2.0, linestyle='--', color='red')
				'''
				self.ax.annotate(a[2],(xss,a[1]),
							xytext=(0.8, 0.9), textcoords='axes fraction',
							arrowprops=dict(facecolor='white', shrink=0.05),
							fontsize=14, color = 'g',
							horizontalalignment='right', verticalalignment='bottom')
				'''

				#self.ax.annotate(a[2],(xss,a[1]),
				#			xytext=(0.8, 0.9), textcoords='axes fraction',
				#			arrowprops=dict(facecolor='white', shrink=0.05),
				#			fontsize=14, color = 'g',
				#			horizontalalignment='right', verticalalignment='bottom')

				if a[3] == "MACD": 
					#l = plt.axvline(x=xss, label=a[2], linewidth=2.0, linestyle='--', color='red')
					self.ax.axvline(x=xss, label=a[2], linewidth=2.0, linestyle='--', color='red')
					self.ax1.axvline(x=xss, label=a[2], linewidth=2.0, linestyle='--', color='red')
				elif a[3] == "RSI":
					#l = plt.axvline(x=xss, label=a[2], linewidth=2.0, linestyle='--', color='red')
					self.ax.axvline(x=xss, label=a[2], linewidth=2.0, linestyle='--', color='green')
					self.ax2.axvline(x=xss, label=a[2], linewidth=2.0, linestyle='--', color='green')

					# draw a default vline at x=1 that spans the yrang


			plt.draw()
		#plt.show()
			plt.savefig("www/operatorio.png")
		except ValueError:
			print('Non-numeric data found in the file.')
			pass



	def plot_prices(self, prices):
		
		self.ax.clear()
		self.ax.plot(prices)

		plt.draw()
		#plt.show()
		plt.savefig("www/operatorio.png")

	def plot_annotation(self, text, x, y, color ):
		
		self.ax.annotate(text, xy=(x, y), xytext=(3, 1.5),arrowprops=dict(facecolor=color, shrink=0.05),)

		plt.draw()
		plt.savefig("www/operatorio.png")


		#ax.annotate('local max', xy=(2, 1), xytext=(3, 1.5), arrowprops=dict(facecolor='black', shrink=0.05) )


	def bytedate2num(self, fmt):
		def converter(b):
			return mdates.strpdate2num(fmt)(b.decode('ascii'))
		return converter

	def movingaverage(self,values,window):
		print("window")
		print(window)
		print("values")
		print(values)
		weigths = numpy.repeat(1.0, window)/window
		print("weigths")
		print(weigths)
		smas = numpy.convolve(values, weigths, 'valid')
		return smas # as a numpy array

	def ExpMovingAverage(self, values, window):
		weights = numpy.exp(numpy.linspace(-1., 0., window))
		weights /= weights.sum()
		a =  numpy.convolve(values, weights, mode='full')[:len(values)]
		a[:window] = a[window]
		return a

