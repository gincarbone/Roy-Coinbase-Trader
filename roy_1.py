import json
import secrets
from coinbase.wallet.client import Client
from secrets import api_key, api_secret
import threading


class Trader(threading.Thread):

	empCount = 0
	def __init__(self, api_key, api_secret):
		self.client = Client(api_key, api_secret)
		self.user = self.client.get_current_user()
		print user 
	def displayCount(self):
		print "Total Employee %d" % Employee.empCount

	def displayEmployee(self):
		print "Name : ", self.name,  ", Salary: ", self.salaryel

	def getAccounts(self):
		accounts = client.get_accounts()
		print("Account:" + accounts)

t = Trader(api_key, api_secret)


	