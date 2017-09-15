# roy
Roy is a Crypto Trading BOT able to operate on crypto currencies on the CoinBase market. The BOT makes buying and selling transactions and uses financial indicators such as EMA, MACD and RFI to predict market trends.
The BOT carries out real financial transactions. Beware of how it is used!

The bot uses algorithms and financial metrics to automatically execute buying and selling assets in crypto currencies. Roy is entirely developed in Python3.

The implemented financial part allows you to evaluate currency price variations and predict bull or bear trends through the combined use of MACD and RSI financial indicators.

The operating mode of the algorithm is to detect price signals through the use of moving averages. In particular, the signals are combined while waiting for the same sign according to the algorithm of the financial analysis below:

http://www.noafx.com/5_4-RSI-MACD-combined.php

Some parts of the code are not written in an elegant manner and certainly need improvements, but it works perfectly. Anyone who wants to participate in the project by improving it and integrating it with these parts:

- support for other markets as well as Coinbase
- improvement of the components that represent the charts
- Improvement of Routines for Advanced Trend Forecasts
- telegram notifications of what happened

Roy can activate a webserver on the machine where it is run. Going to http: //localhost/index.html displays a chart with price variations, the RSI index, the MACD index, and the signals intercepted by the SW.

At this time the operation is limited to a simulation. The BUY and SELL functions are present, but LOCAL_BUY and LOCAL_SELL are used to perform non-real money 
