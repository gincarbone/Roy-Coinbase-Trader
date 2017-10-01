## Roy Trader
Roy is a Crypto Trading BOT able to operate on crypto currencies on the CoinBase market. The BOT makes buying and selling transactions and uses financial indicators such as EMA, MACD and RFI to predict market trends.
The BOT carries out real financial transactions. Beware of how it is used!
## How It Works
Roy uses algorithms and financial metrics to automatically execute buying and selling assets in crypto currencies. It is entirely developed in Python3.
Roy can activate a webserver on the machine where it is run. Going to http://localhost/index.html displays a chart with price variations, the RSI index, the MACD index, and the signals intercepted by the SW.
For security reasons, at this time the operation is limited to a simulation. The BUY and SELL functions are present, but LOCAL_BUY and LOCAL_SELL are used to perform non-real money.
## Financial Metrics Used
The implemented financial part allows you to evaluate currency price variations and predict bull or bear trends through the combined use of <b>MACD</b> and <b>RSI</b> financial indicators.
## Trading Strategies
The operating mode of the algorithm is to detect price signals through the use of moving averages. In particular, the signals are combined while waiting for the same sign according to the algorithm of the financial analysis below:
http://www.noafx.com/5_4-RSI-MACD-combined.php
## Code and roadmap
Some parts of the code are not written in an elegant manner and certainly need improvements, but it works perfectly. Anyone who wants to participate in the project by improving it and integrating it with these parts:

- support for other markets as well as Coinbase (bittrex es.)
- improvement of the components that represent the charts
- Improvement of Routines for Advanced Trend Forecasts
- telegram notifications of signals and operations
## Installation
Prerequisites and libraries: 

git clone https://github.com/gincarbone/roy

pip3 install -r requirements.txt

## Screens
<img align="center" width="600" height="300" src="http://www.marcelloincarbone.it/wp-content/uploads/2017/09/Console1.jpg">
Console 
<img align="center" width="600" height="400" src="http://www.marcelloincarbone.it/wp-content/uploads/2017/09/chart1.png">
Charts

## Offer me an Italian Coffee
these are the digital addresses to make a small offer and support the project. Thank you. 

BTC = 17fYA4hB6BDikGSqcyYjC3dCnU56bjeN2J  

ETH = 0xdc66Bbf32580d358e3eC021A20B51a09AFeB993e  

LTC = LgzpfTNJjjmqP2mcpkJNYeR4HYupU4BFTP


